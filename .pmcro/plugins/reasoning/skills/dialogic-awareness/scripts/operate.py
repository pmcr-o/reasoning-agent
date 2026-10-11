from __future__ import annotations
import argparse,json,sys,re
from pathlib import Path
PHASES=['ORCHESTRATE','PLAN','MAKE','CHECK','REFLECT']
REQUIRED=['frameId','I','cycleId','phase','speakerAgent','listenerAgent','speechAct','problemModel','intentHypothesis','intentDelta','epistemicState','rationaleSummary','awarenessDelta','dependencyRefs','evidenceRefs','authorityCeilingRef','evidenceStatus']
def load(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def validate(doc):
 if doc.get('schema')!='pmcro.dialogic-awareness/v1': raise ValueError('schema')
 if not doc.get('rawUtteranceRef'): raise ValueError('rawUtteranceRef')
 frames=doc.get('frames');
 if not isinstance(frames,list) or not frames: raise ValueError('frames')
 first=frames[0]
 if first.get('phase')!='ORCHESTRATE': raise ValueError('new root seed must begin at ORCHESTRATE')
 if first.get('speakerAgent')!='orchestrator': raise ValueError('first active identity must be orchestrator')
 if first.get('intentHypothesis',{}).get('version')!=0: raise ValueError('first intent hypothesis must be v0')
 ids=[]
 for f in frames:
  miss=[k for k in REQUIRED if k not in f]
  if miss: raise ValueError('missing '+','.join(miss))
  if f['phase'] not in PHASES: raise ValueError('phase')
  if f['speakerAgent']==f['listenerAgent'] and f['speechAct'] not in ['REFLECT','ASSERT_IDENTITY']: raise ValueError('self-address requires REFLECT/ASSERT_IDENTITY')
  I=f['I']
  for k in ['schema','iRef','entityRef','role','behavior','intentRef','lineageRootRef','parentIRef','objectIRefs','addressedIRef','authorityCeilingRef','metaDepth','consciousnessClaim']:
   if k not in I: raise ValueError('missing I.'+k)
  if I['schema']!='pmcro.i-context/v1' or I['entityRef']!=f['speakerAgent'] or I['role']!=f['phase'] or I['behavior']!=f['speechAct']: raise ValueError('I identity/behavior mismatch')
  if I['addressedIRef']!=f['listenerAgent'] or I['authorityCeilingRef']!=f['authorityCeilingRef'] or I['lineageRootRef']!=doc['rawUtteranceRef']: raise ValueError('I relation/lineage mismatch')
  if I['consciousnessClaim'] is not False: raise ValueError('I context cannot claim consciousness')
  if not isinstance(f['rationaleSummary'],str) or not f['rationaleSummary'].strip(): raise ValueError('rationaleSummary')
  if 'chain-of-thought' in f['rationaleSummary'].lower() or 'hidden reasoning' in f['rationaleSummary'].lower(): raise ValueError('rationaleSummary must be external explanation, not hidden reasoning')
  visible=' '.join([str(f.get('rationaleSummary','')),str(f.get('questionOrChallenge') or ''),str(f.get('problemModel',{}).get('statement','')),str(f.get('problemModel',{}).get('goal',''))])
  if re.search(r'(?i)\b(you|your|yours|thou|thee|thy|thine)\b',visible): raise ValueError('dialogic product must use I-to-I language')
  ids.append(f['frameId'])
 if len(ids)!=len(set(ids)): raise ValueError('duplicate frameId')
 known=set(ids)
 i_ids={f['I']['iRef'] for f in frames}
 for f in frames:
  I=f['I']
  if I['parentIRef'] and I['parentIRef'] not in i_ids: raise ValueError('unknown parent I')
  if any(x not in i_ids for x in I['objectIRefs']): raise ValueError('unknown object I')
  for d in f['dependencyRefs']:
   if d not in known: raise ValueError('unknown dependency '+d)
  r=f.get('responseToFrameRef')
  if r is not None and r not in known: raise ValueError('unknown responseToFrameRef '+r)

  ih=f['intentHypothesis'];delta=f['intentDelta']
  if not ih.get('sourceRefs') or doc['rawUtteranceRef'] not in ih['sourceRefs']: raise ValueError('intent hypothesis must reference raw utterance')
  if not (0 <= float(ih.get('confidence',-1)) <= 1): raise ValueError('intent confidence')
  if ih.get('version',-1) < 0: raise ValueError('intent version')
  if delta.get('parentFrameRef') is not None and delta['parentFrameRef'] not in known: raise ValueError('unknown intent parent')
 return True
def render(doc):
 lines=[f"RAW UTTERANCE: {doc['rawUtteranceRef']} (immutable)"]
 for f in doc['frames']:
  e=f['epistemicState']; a=f['awarenessDelta']; q=f.get('questionOrChallenge')
  ih=f['intentHypothesis'];delta=f['intentDelta']
  I=f['I']
  lines += ['',f"[{f['phase']}] I AM {f['speakerAgent']} -> I AM {f['listenerAgent']} ({f['speechAct']})",f"I-CONTEXT: {I['iRef']} | entity={I['entityRef']} | role={I['role']} | behavior={I['behavior']} | intent={I['intentRef']} | prior-I={I['parentIRef'] or '(root)'} | object-I={','.join(I['objectIRefs']) or '(none)'} | addressed-I={I['addressedIRef']} | meta={I['metaDepth']}",f"INTENT v{ih['version']}: {ih['statement']}",f"GOAL: {ih['goal']}",f"INTENT CONFIDENCE: {ih['confidence']:.2f}",f"PRESERVED: {'; '.join(ih['preservedConstraints']) or '(none)'}",f"AMBIGUOUS: {'; '.join(ih['ambiguities']) or '(none)'}",f"INTENT Î” CLEARER: {'; '.join(delta['clearer']) or '(none)'}",f"INTENT Î” ADDED/REVISED: {'; '.join(delta['added']) or '(none)'}",f"PROBLEM: {f['problemModel']['statement']}",f"GOAL: {f['problemModel']['goal']}",f"I KNOW: {'; '.join(e['known']) or '(none)'}",f"I DO NOT KNOW: {'; '.join(e['unknown']) or '(none)'}",f"UNCERTAINTY: {e['uncertainty']}",f"RATIONALE SUMMARY: {f['rationaleSummary']}"]
  if q: lines.append('ADDRESS: '+q)
  lines += [f"AWARENESS +: {'; '.join(a['learned']) or '(none)'}",f"AWARENESS ~: {'; '.join(a['revised']) or '(none)'}",f"STILL UNKNOWN: {'; '.join(a['stillUnknown']) or '(none)'}",f"DEPENDS ON: {', '.join(f['dependencyRefs']) or '(root)'}",f"EVIDENCE: {', '.join(f['evidenceRefs']) or '(none)'} [{f['evidenceStatus']}]",f"AUTHORITY CEILING: {f['authorityCeilingRef']}"]
 return '\n'.join(lines)+'\n'
def main():
 ap=argparse.ArgumentParser();sp=ap.add_subparsers(dest='op',required=True)
 for op in ['validate','render']:
  p=sp.add_parser(op);p.add_argument('--input',required=True)
 a=ap.parse_args();doc=load(a.input);validate(doc)
 if a.op=='validate': print(json.dumps({'status':'PASS','frames':len(doc['frames']),'rawUtteranceRef':doc['rawUtteranceRef']}))
 else: sys.stdout.write(render(doc))
if __name__=='__main__':main()
