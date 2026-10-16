# Assisted-v1: forensic verification and reproducibility

16 October 2026. Read-only independent audit; companion to [scientific analysis](scientific-analysis.md) and [complete trace ledger](exhaustive-trace-ledger.md). This is an analysis artifact, not the final course report or a change to the scientific contract.

## 1. What this verifier establishes

The executable audit below reads the canonical SQLite stores with `mode=ro&immutable=1`, reads archives in memory, and writes nothing. It uses Python's standard library, imports no experiment implementation, and never loads a model or tokenizer. Run it from the repository root. It independently reconstructs all natural episodes, scripted diagnostic views, strict actions, literal histories, scalar scores, world proposals, assignments, invocation seeds, costs and paired bootstrap calculations. It checks retained identities, exact exports and report projections. Repeated assertions check different persisted records; their count is not a count of independent statistical observations or a substitute for an implementation test suite.

The eight hardware calls have no scientific episode effects. The two deliberately padded, forced-length envelopes are checked separately from ordinary EOS-terminated scientific replies. Every worker uses local `cuda:0`; resident load UUIDs and `CUDA_VISIBLE_DEVICES` establish the two physical GPU mappings. The code does not infer historical authorization, filesystem transaction timing, GPU utilization, provider billing or unobserved hidden model states from a final snapshot.

## 2. Reproduction

Use Python 3.11 or newer. From the repository root, run this PowerShell command, which executes only the Python block in this new Markdown document:

```powershell
@'
from pathlib import Path
p = Path('docs/analysis/assisted-v1/forensic-reproducibility.md')
fence = chr(96) * 3
code = p.read_text(encoding='utf-8').split(fence + 'python\n', 1)[1].split('\n' + fence, 1)[0]
exec(compile(code, str(p), 'exec'))
'@ | python -B -
```

The default output is an assertion inventory, deviations, independently computed outcomes/effort, process totals and the historical comparison. Expected deviations are an empty list. No third-party statistical defaults are used: the primary and principal effort endpoints initialize separate `Random(2026101602)` streams, sample five paired worlds per owner/first-speaker stratum, and select zero-based sorted indices 250 and 9750 from 10,000 draws. Auxiliary bootstrap values are exposed by the helper only when explicitly invoked; the audit reports the two adopted endpoints.

## 3. Executable independent verifier

```python
from pathlib import Path
import json,sqlite3,collections,hashlib,zipfile,csv,io,math,statistics,random,re
R=Path('notebooks/run/assisted-v1'); L=R/'latest'; S=L/'source'
run=json.loads((L/'run.json').read_text(encoding='utf-8'))
worlds={w['id']:w for w in run['worlds']}
dbs=[]; calls=[]; attempts=[]; eps={}; metas=[]; sessions=[]
for i in range(2):
 c=sqlite3.connect((L/f'worker-{i}.sqlite').resolve().as_uri()+'?mode=ro&immutable=1',uri=True);c.row_factory=sqlite3.Row;dbs.append(c)
 metas.append({x['key']:json.loads(x['value']) for x in c.execute('select * from meta')})
 for x in c.execute('select * from calls'):
  d=dict(x);d['worker']=i;d['request']=json.loads(d['request']);d['outcome']=json.loads(d['outcome']) if d['outcome'] else None;calls.append(d)
 for x in c.execute('select * from attempts'):
  d=dict(x);d['worker']=i;d['evidence']=json.loads(d['evidence']) if d['evidence'] else None;attempts.append(d)
 for x in c.execute('select * from episodes'):eps[x['id']]=json.loads(x['state'])
 for x in c.execute('select * from sessions'):sessions.append(dict(worker=i,id=x['id'],evidence=json.loads(x['evidence'])))
bycall={c['id']:c for c in calls}
def out(x): print(json.dumps(x,ensure_ascii=True,default=str))

from copy import deepcopy
checks=collections.Counter(); anomalies=[]
def check(name,condition,detail=''):
 checks[name]+=1
 if not condition:anomalies.append([name,detail])
def canonical(x):return json.dumps(x,sort_keys=True,ensure_ascii=True,allow_nan=False,separators=(',',':'))
def seed(*x):return int.from_bytes(hashlib.sha256(canonical([run['config']['master_seed'],*x]).encode()).digest()[:8],'big')%2**63
def parse(c):
 o=c['outcome']
 if not o:return None,'unknown'
 if o.get('failure'):return None,'provider_failure'
 if o.get('truncated'):return None,'truncated_action'
 if o.get('framing_error'):return None,'malformed_action'
 def pairs(xs):
  d={}
  for k,v in xs:
   if k in d:raise ValueError()
   d[k]=v
  return d
 try:
  a=json.loads(o['raw_text'],object_pairs_hook=pairs,parse_constant=lambda _:(_ for _ in ()).throw(ValueError()))
  if type(a)!=dict or set(a)!={'message','submit','wait'}:raise ValueError()
  m,s,w=a['message'],a['submit'],a['wait']
  if m is not None and (type(m)!=str or not m.strip()) or s is not None and type(s)!=int or type(w)!=bool:raise ValueError()
  if w and (m is not None or s is not None) or not w and m is None and s is None:raise ValueError()
  if c['request']['control'] and (m is not None or s is None or w):raise ValueError()
  return a,None
 except (ValueError,TypeError):return None,'malformed_action'
def feedback(c):
 o=c['outcome']
 if o.get('failure'):return 'Call failed; no action was delivered.'
 if o.get('truncated'):return 'Invalid: output was truncated. Nothing was delivered.'
 try:a=json.loads(o['raw_text'])
 except ValueError:a={}
 if isinstance(a,dict) and set(a)=={'message','submit','wait'}:
  if a['wait'] is True and (a['message'] is not None or a['submit'] is not None):return 'Invalid: wait requires null message and null submit. Nothing was delivered.'
  if a['wait'] is False and a['message'] is None and a['submit'] is None:return 'Invalid: choose message, submit, both, or wait. Nothing was delivered.'
 return 'Invalid: output one JSON object with the required fields and types. Nothing was delivered.'
def newstate(w,ph,pref=None):
 h=deepcopy(pref['history']) if ph=='retain' else [[],[]]
 return dict(world=w['id'],phase=ph,history=h,turns=[0,0],submissions=[None,None],waiting=[False,False],next=w['first'],events=[],terminal=None,unused=None,regime=run['regime'],earlier_history_lengths=[len(x) for x in h] if ph=='retain' else [0,0])
def choose(s):
 if s['terminal']:return None
 av=[a for a in range(2) if s['submissions'][a] is None and s['turns'][a]<3 and not s['waiting'][a]]
 return s['next'] if s['next'] in av else av[0] if av else None
def apply(s,a,act,err,cid,fb=None):
 s=deepcopy(s)
 s['turns'][a]+=1;s['next']=1-a;s['events'].append(dict(call=cid,agent=a,action=act,error=err))
 if act is None:s['history'][a].append(dict(kind='feedback',text=fb))
 else:
  s['history'][a].append(dict(kind='own_action',action=deepcopy(act)))
  if act['message'] is not None:
   s['history'][1-a].append(dict(kind='received_message',sender=a,text=act['message']));s['waiting'][1-a]=False
  if act['submit'] is not None:s['submissions'][a]=act['submit']
  s['waiting'][a]=act['wait']
 if all(v is not None for v in s['submissions']):s['terminal']='both_submitted'
 elif choose(s) is None:s['terminal']='waiting_deadlock' if any(s['waiting'][a] and s['submissions'][a] is None and s['turns'][a]<3 for a in range(2)) else 'horizon_exhausted'
 if s['terminal']:s['unused']=[3-t for t in s['turns']]
 return s
def view(w,s,a):
 v=dict(agent=a,current_shard=deepcopy(w['original' if s['phase']=='prefix' else 'revised'][a]),visible_history=deepcopy(s['history'][a]),own_invocation=s['turns'][a]+1,partner_finished=s['submissions'][1-a] is not None,reopened=s['phase']!='prefix',earlier_history_length=s['earlier_history_lengths'][a])
 if v['reopened']:
  v['revision_notice']=dict(owner=w['owner'],record=w['row'])
  if a==w['owner']:v['revision_notice']['new_value']=w['after']
 return v
annex=(S/'docs/plans/i01-course-final-design-protocol-and-acceptance.md').read_text(encoding='utf-8')
fence=chr(96)*3
system=annex.split(fence+'text\n',1)[1].split('\n'+fence,1)[0]
control_system=annex.split(fence+'text\n')[2].split('\n'+fence,1)[0]
def render(v,control=False):
 if control:return [{'role':'system','content':control_system},{'role':'user','content':'Complete input: '+str(v['complete_input'])}]
 def hist(h):
  blocks=[]
  for x in h:
   if x['kind']=='own_action':
    a=x['action'];body='Your action:\nmessage='+('null' if a['message'] is None else a['message'])+'\nsubmit='+('null' if a['submit'] is None else str(a['submit']))+'; wait='+str(a['wait']).lower()
   elif x['kind']=='received_message':body=f"From agent {x['sender']}:\n{x['text']}"
   else:body='Environment feedback:\n'+x['text']
   blocks.append('BEGIN VISIBLE ENTRY\n'+body+'\nEND VISIBLE ENTRY')
  return '\n'.join(blocks) or '(no visible entries)'
 notice=v.get('revision_notice')
 n='No source-change notice in this phase.'
 if notice:
  n=f"Environment event: the following record changed before this phase began.\nChanged owner (agent identity): {notice['owner']}\nChanged record (index only): {notice['record']}"
  if 'new_value' in notice:n+='\nReplacement value for your record: '+str(notice['new_value'])
 b=v['earlier_history_length'];h=v['visible_history']
 phase='reopened after an environment source change' if v['reopened'] else 'initial'
 body=f"You are agent {v['agent']}. Your partner is agent {1-v['agent']}.\nThis phase: {phase}.\nYour invocation: {v['own_invocation']}/3.\nPartner finished: {str(v['partner_finished']).lower()}. This is status only; no value is disclosed.\n\n"
 body+='VISIBLE HISTORY: EARLIER PHASE\n'+hist(h[:b])+'\n\nVISIBLE HISTORY: THIS PHASE\n'+hist(h[b:])+'\n\nENVIRONMENT SOURCE NOTICE\n'+n+'\n\nCURRENT AUTHORITATIVE PRIVATE SHARD\n'
 body+='\n'.join(f'record {i}: {x}' for i,x in enumerate(v['current_shard']))
 body+='\n\nChoose one legal action for the current phase. Return only the JSON object.'
 if v.get('diagnostic_directive'):body+='\n'+v['diagnostic_directive']
 return [{'role':'system','content':system},{'role':'user','content':body}]
combos=[(0,'retain'),(0,'clear'),(1,'retain'),(1,'clear')]
assigned={}
for st in range(4):
 a=combos+[combos[st]];random.Random(seed('assignment',st//2,st%2)).shuffle(a);assigned[st]=a
for w in worlds.values():
 values=sum(w['original'],[]);rev=sum(w['revised'],[])
 check('truth_original',max(values)==w['original_truth'],w['id'])
 check('truth_revised',max(rev)==w['revised_truth'],w['id'])
 differences=[(a,j) for a in range(2) for j in range(20) if w['original'][a][j]!=w['revised'][a][j]]
 check('edit',differences==[(w['owner'],w['row'])] and values.count(max(values))==1 and w['before']==max(values) and -1000<=w['after']<max(rev),w['id'])
 rng=random.Random(seed(w['id'],'world'));rc=dict(nonunique_maximum=0,remaining_at_floor=0,owner_block=0)
 for pn in range(1,1001):
  x=[[rng.randint(-1000,1000) for _ in range(20)] for _ in range(2)];flat=sum(x,[]);mx=max(flat)
  if flat.count(mx)!=1:rc['nonunique_maximum']+=1;continue
  sec=max(v for v in flat if v!=mx)
  if sec<=-1000:rc['remaining_at_floor']+=1;continue
  if mx not in x[w['owner']]:rc['owner_block']+=1;continue
  y=deepcopy(x);row=x[w['owner']].index(mx);y[w['owner']][row]=rng.randint(-1000,sec-1);break
 check('world_regeneration',x==w['original'] and y==w['revised'] and pn==w['proposals'] and rc==w['rejections'],w['id'])
 i=w['index'];s=i%4
 check('owner_first',w['owner']==s//2 and w['first']==s%2,w['id'])
 if w['group']=='main':device,pol=assigned[s][i//4]
 elif w['group']=='pilot':device,pol=[(0,'retain'),(1,'retain'),(0,'clear'),(1,'clear')][s]
 else:device,pol=s%2,None
 check('assignment',w['device']==device and w['treatments']==([] if pol is None else [pol,'clear' if pol=='retain' else 'retain']),w['id'])
 for ph in ['prefix','recovery']:
  check('seed_schedule',w['seeds'][ph]==[[seed(w['id'],ph,a,k) for k in range(3)] for a in range(2)],w['id']+'/'+ph)
 check('control_seeds',w['control_seeds']=={p:seed(w['id'],'control',p) for p in ['original','revised']},w['id'])
reconstructed={};callrows=[];covered=set()
for w in worlds.values():
 if w['group']=='qualification':continue
 for ph in ['prefix','retain','clear']:
  eid=w['id']+'/'+ph;s=newstate(w,ph,reconstructed.get(w['id']+'/prefix'))
  for event in eps[eid]['events']:
   cid=event['call'];c=bycall[cid];covered.add(cid);a=event['agent'];act,err=parse(c)
   check('eligible_actor',choose(s)==a,cid)
   check('call_identity',cid==f"{eid}/agent-{a}/invocation-{s['turns'][a]}" and c['episode']==eid,cid)
   v=view(w,s,a)
   check('permitted_view',v==c['request']['view'],cid)
   check('rendered_messages',render(v)==c['request']['messages'],cid)
   check('invocation_seed',c['request']['seed']==w['seeds']['prefix' if ph=='prefix' else 'recovery'][a][s['turns'][a]],cid)
   check('event_action',event['action']==act and event['error']==err,cid)
   check('scientific_committed',c['effect_committed']==1,cid)
   local=max(v['current_shard']);truth=w['original_truth' if ph=='prefix' else 'revised_truth']
   raw=json.loads(c['outcome']['raw_text'])
   callrows.append(dict(id=cid,world=w['id'],group=w['group'],phase=ph,agent=a,invocation=v['own_invocation'],local=local,truth=truth,action=act,raw_action=raw,error=err,partner_finished=v['partner_finished'],local_refutable=bool(act and act['submit'] is not None and act['submit']<local),obsolete=bool(ph!='prefix' and act and act['submit']==w['original_truth']),correct=bool(act and act['submit']==truth),visible_messages=sum(x['kind']=='received_message' for x in v['visible_history']),view=v))
   s=apply(s,a,act,err,cid,feedback(c) if err else None)
  check('final_checkpoint',s==eps[eid],eid);reconstructed[eid]=s
for c in calls:
 if '/control-' not in c['id']:continue
 wid,mode=c['id'].split('/');w=worlds[wid];ph='original' if 'original' in mode else 'revised';covered.add(c['id'])
 v={'complete_input':sum(w[ph],[])};a,err=parse(c);gold=max(v['complete_input'])
 check('control_view',c['request']['view']==v,c['id'])
 check('control_render',c['request']['messages']==render(v,True),c['id'])
 check('control_seed',c['request']['seed']==w['control_seeds'][ph],c['id'])
 check('control_checkpoint',eps[c['id']]==dict(correct=int(a is not None and a['submit']==gold),error=err,submissions=[a['submit'] if a else None],terminal='control_completed'),c['id'])
 check('scientific_committed',c['effect_committed']==1,c['id'])
for label,ix,actor in [('D00',0,0),('D01',1,1),('D02',3,1),('D03',2,0)]:
 w=worlds[f'qualification-{ix:02d}'];s=newstate(w,'prefix');mx=[max(x) for x in w['original']]
 if label in ['D01','D02']:
  s=apply(s,1,dict(message=f'My local maximum is {mx[1]}.',submit=None,wait=False),None,f'scripted/{label}/0')
  s=apply(s,0,dict(message=f'My local maximum is {mx[0]}.',submit=w['original_truth'],wait=False),None,f'scripted/{label}/1')
  if label=='D02':
   s=apply(s,1,dict(message=None,submit=w['original_truth'],wait=False),None,f'scripted/{label}/2');s=newstate(w,'retain',s)
 if label=='D03':s=newstate(w,'clear')
 v=view(w,s,actor)
 if label=='D00':v['diagnostic_directive']='Interface check: send only the message ready. Do not submit or wait.';expected='ready'
 elif label=='D03':v['diagnostic_directive']="Local-source check: send only your current shard's maximum as decimal message text. Do not submit or wait.";expected=str(max(w['revised'][actor]))
 else:expected=w['revised_truth' if label=='D02' else 'original_truth']
 cid=w['id']+'/diagnostic-'+label;c=bycall[cid];act,err=parse(c);covered.add(cid)
 passed=bool(act and ((act['message'] is not None and act['message'].strip()==expected and act['submit'] is None and not act['wait']) if label in ['D00','D03'] else act['submit']==expected and not act['wait']))
 check('diagnostic_view',c['request']['view']==v,cid)
 check('diagnostic_render',c['request']['messages']==render(v),cid)
 check('diagnostic_seed',c['request']['seed']==seed(w['id'],'diagnostic',label),cid)
 check('diagnostic_checkpoint',eps[cid]==dict(action=act,diagnostic=label,error=err,expected=expected,passed=passed,scripted_fixture=True,submissions=[act['submit'] if act else None],terminal='diagnostic_completed'),cid)
 check('scientific_committed',c['effect_committed']==1,cid)
for c in calls:
 o=c['outcome'];a=[a for a in attempts if a['call_id']==c['id']]
 check('single_attempt',len(a)==1 and a[0]['number']==1 and a[0]['worker']==c['worker'],c['id'])
 check('attempt_evidence',len(a)==1 and a[0]['evidence']==o and a[0]['status']=='completed' and a[0]['finished_at'] is not None,c['id'])
 check('raw_outcome',o is not None and (c['request'].get('envelope') or o['raw_text']==o['visible_text']) and o['failure'] is None and o['framing_error'] is None and o['thinking'] is None,c['id'])
 check('termination',o['termination'] in ['eos','length'] and o['generated_tokens']==len(o['token_ids']),c['id'])
 check('input_vector',len(c['request']['input_ids'])==o['input_tokens']==len(c['request']['attention_mask']) and set(c['request']['attention_mask'])=={1} and o['input_tokens']<=8192,c['id'])
 check('backend_seed',all(o['backend'][k]==c['request']['seed'] for k in ['seed','cpu_seed','cuda_seed']),c['id'])
 cache=o['backend']['cache']
 check('fresh_cache',cache['initial_empty'] and cache['disposed_after_call'] and cache['same_call_cache'],c['id'])
 check('placement',o['backend']['device']=='cuda:0',c['id'])
 check('headroom',o['backend']['observed_free_min_bytes']>=1610612736,c['id'])
 if not c['id'].startswith('hardware/'):
  check('covered_scientific_call',c['id'] in covered,c['id'])
  check('source_device',c['worker']==worlds[c['id'].split('/')[0]]['device'],c['id'])
conversations=[json.loads(x) for x in (L/'reports/conversations.jsonl').read_text(encoding='utf-8').splitlines()]

def score(eid):
 w=worlds[eid.split('/')[0]];s=eps[eid];truth=w['original_truth' if eid.endswith('/prefix') else 'revised_truth']
 return int(s['submissions']==[truth,truth])
def cost(eid):
 cc=[c for c in calls if c['episode']==eid]
 return dict(calls=len(cc),ready=sum(c['outcome']['ready_seconds'] for c in cc),dispatch=sum(c['outcome']['dispatch_seconds'] for c in cc),input=sum(c['outcome']['input_tokens'] for c in cc),generated=sum(c['outcome']['generated_tokens'] for c in cc),messages=sum(bool(parse(c)[0] and parse(c)[0]['message'] is not None) for c in cc))
worldrows=[]
for w in worlds.values():
 if w['group']=='qualification':continue
 row={k:w[k] for k in ['id','group','owner','first','device','treatments','original_truth','revised_truth']}
 for ph in ['prefix','retain','clear']:
  eid=w['id']+'/'+ph;e=eps[eid];row[ph]=dict(success=score(eid),submissions=e['submissions'],terminal=e['terminal'],turns=e['turns'],**cost(eid))
 row['control']=eps[w['id']+'/control-revised-direct']['correct'];worldrows.append(row)
main=[r for r in worldrows if r['group']=='main']
def boot(field):
 strata=[[r['clear'][field]-r['retain'][field] for r in main if r['owner']==o and r['first']==f] for o in range(2) for f in range(2)]
 rng=random.Random(2026101602);d=sorted(sum(rng.choice(v) for v in strata for _ in range(5))/20 for _ in range(10000))
 return dict(mean=statistics.mean(r['clear'][field]-r['retain'][field] for r in main),low=d[250],high=d[9750],constant=[i for i,v in enumerate(strata) if len(set(v))==1])
phase_stats={}
own_re=re.compile(r'\bMy (?:new )?(?:(?:local|shard) )?max(?:imum)? is (-?\d+)',re.I)
peer_re=re.compile(r'\bYour (?:new )?(?:(?:local|shard) )?max(?:imum)? is (-?\d+)',re.I)
claimrows=[]
for x in callrows:
 a=x['action'];m=a['message'] if a else None;w=worlds[x['world']]
 own=[int(v) for v in own_re.findall(m or '')];peer=[int(v) for v in peer_re.findall(m or '')]
 claims=dict(call=x['id'],own=own,own_truth=x['local'],own_wrong=any(v!=x['local'] for v in own),peer=peer,peer_truth=max(w['original' if x['phase']=='prefix' else 'revised'][1-x['agent']]),notice_row_own_value=w['revised'][x['agent']][w['row']])
 claimrows.append(claims)
for group in ['pilot','main']:
 for ph in ['prefix','retain','clear']:
  rr=[r for r in worldrows if r['group']==group];cr=[x for x in callrows if x['group']==group and x['phase']==ph];ee=[eps[r['id']+'/'+ph] for r in rr]
  aa=[x for x in cr if x['action']];subs=[x for x in aa if x['action']['submit'] is not None]
  claims=[c for c in claimrows if any(c['call']==x['id'] for x in cr)]
  repeats=0;triple_agents=0
  for e in ee:
   for agent in range(2):
    mm=[v['action']['message'] for v in e['events'] if v['agent']==agent and v['action'] and v['action']['message'] is not None]
    repeats+=len(mm)-len(set(mm))
    triple_agents+=int(len(mm)==3 and len(set(mm))==1)
  phase_stats[group+'/'+ph]=dict(episodes=len(rr),success=sum(r[ph]['success'] for r in rr),calls=len(cr),illegal=len(cr)-len(aa),messages=sum(x['action']['message'] is not None for x in aa),actions=dict(collections.Counter('both' if x['action']['message'] is not None and x['action']['submit'] is not None else 'message_only' if x['action']['message'] is not None else 'submit_only' if x['action']['submit'] is not None else 'wait' for x in aa)),terminal=dict(collections.Counter(e['terminal'] for e in ee)),submissions=len(subs),correct_submissions=sum(x['correct'] for x in subs),local_refutable=sum(x['local_refutable'] for x in subs),obsolete=sum(x['obsolete'] for x in subs),agreement=sum(e['submissions'][0] is not None and e['submissions'][0]==e['submissions'][1] for e in ee),wrong_agreement=sum(e['submissions'][0] is not None and e['submissions'][0]==e['submissions'][1] and r[ph]['success']==0 for e,r in zip(ee,rr)),no_submission=sum(e['submissions']==[None,None] for e in ee),duplicate_messages=repeats,exact_triple_message_agents=triple_agents,own_claim_calls=sum(bool(c['own']) for c in claims),wrong_own_claim_calls=sum(c['own_wrong'] for c in claims),**{key:sum(r[ph][key] for r in rr) for key in ['ready','dispatch','input','generated']})

# Verify retained package and each declared identity without extracting or writing.
integrity=json.loads((L/'integrity.json').read_text())
for rel,record in integrity['files'].items():
 p=L/rel
 check('integrity_member',p.is_file() and p.stat().st_size==record['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==record['sha256'],rel)
with zipfile.ZipFile(R/'latest.zip') as z:
 zn=[n for n in z.namelist() if not n.endswith('/')]
 check('zip_names',set(zn)=={p.relative_to(L).as_posix() for p in L.rglob('*') if p.is_file()},'latest.zip')
 for n in zn:check('zip_bytes',z.read(n)==(L/n).read_bytes(),n)
 check('zip_crc',z.testzip() is None,'latest.zip')
release=json.loads((S/'source-release.json').read_text())
for rel,rec in release['files'].items():
 p=S/rel;check('release_member',p.stat().st_size==rec['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==rec['sha256'],rel)
for rel,sha in run['source_identity'].items():check('run_source_identity',hashlib.sha256((S/rel).read_bytes()).hexdigest()==sha,rel)
with zipfile.ZipFile(next(S.glob('*.whl'))) as z:
 for p in (S/'recovery').rglob('*.py'):
  rel=p.relative_to(S).as_posix();check('wheel_source',z.read(rel)==p.read_bytes(),rel)
for i,c in enumerate(dbs):
 check('sqlite_integrity',c.execute('pragma integrity_check').fetchall()[0][0]=='ok',i)
 check('binding',metas[i]['binding']['manifest']==run,i)
# Complete conversation export equality.
for x in conversations:
 if x['record_type']=='episode_checkpoint':
  original=dbs[x['slot']].execute('select state from episodes where id=?',(x['id'],)).fetchone()
  check('export_episode',original is not None and original[0]==x['state'],x['id'])
 else:
  original=dict(dbs[x['slot']].execute('select * from calls where id=?',(x['id'],)).fetchone())
  expected=original|dict(slot=x['slot'],record_type='call')
  check('export_call',x==expected,x['id'])
check('export_coverage',len(conversations)==len(calls)+len(eps),'jsonl')
# Native rendered text can be checked without loading the tokenizer.
for c in calls:
 r=c['request']
 expected=''.join('<|im_start|>'+m['role']+'\n'+m['content']+'<|im_end|>\n' for m in r['messages'])+'<|im_start|>assistant\n<think>\n\n</think>\n\n'
 check('native_text_framing',r['rendered']==expected,c['id']) if not r.get('envelope') else check('forced_envelope',len(r['input_ids'])==8192 and c['outcome']['generated_tokens']==512 and c['outcome']['truncated'] and c['outcome']['termination']=='length',c['id'])
 if not r.get('envelope'):
  check('terminal_suffix',c['outcome']['backend']['raw_suffix_text']==c['outcome']['raw_text']+'<|im_end|>' and c['outcome']['token_ids'][-1]==248046 and not c['outcome']['truncated'],c['id'])
# A-B-A requests and saved generations match on each resident worker.
for i in range(2):
 a=bycall[f'hardware/state-{i}-A1'];b=bycall[f'hardware/state-{i}-A2']
 check('ABA_request',a['request']==b['request'],i)
 check('ABA_output',a['outcome']['token_ids']==b['outcome']['token_ids'] and a['outcome']['raw_text']==b['outcome']['raw_text'],i)
# Frozen scientific settings are identical for all ordinary requests.
settings=[c['request']['settings'] for c in calls if not c['request'].get('envelope')]
check('settings_constant',all(x==settings[0] for x in settings),'all ordinary calls')
# Recorded physical order, admission timestamps and device serialization.
for w in worlds.values():
 if w['group']=='qualification':continue
 seq=[]
 for ph in ['prefix']+w['treatments']+(['control-original-direct','control-revised-direct'] if w['group']=='pilot' else ['control-revised-direct']):
  aa=sorted((a for a in attempts if bycall[a['call_id']]['episode']==w['id']+'/'+ph),key=lambda a:a['admitted_at'])
  check('phase_call_order',bool(aa),w['id']+'/'+ph);seq+=aa
 check('world_physical_order',[a['admitted_at'] for a in seq]==sorted(a['admitted_at'] for a in seq),w['id'])
for i in range(2):
 aa=sorted([a for a in attempts if a['worker']==i],key=lambda a:a['admitted_at'])
 check('device_nonoverlap',all(a['finished_at']<=b['admitted_at'] for a,b in zip(aa,aa[1:])),i)
# Input overlap against all locally available historical manifests and archives.
exposed=set();source_inputs=[]
for p in sorted(Path('notebooks/run').glob('*/latest/run.json')):
 if p==L/'run.json':continue
 old=json.loads(p.read_text(encoding='utf-8'))
 ww=old.get('worlds',[])
 for w in ww:
  for ph in ['original','revised']:exposed.add(canonical(w[ph]))
 source_inputs.append((p.as_posix(),len(ww)))
for p in sorted(Path('notebooks/run').glob('*/latest.zip')):
 if p==R/'latest.zip':continue
 with zipfile.ZipFile(p) as z:
  names=[n for n in z.namelist() if n=='run.json' or n.endswith('/run.json')]
  for n in names:
   old=json.loads(z.read(n));ww=old.get('worlds',[])
   for w in ww:
    for ph in ['original','revised']:exposed.add(canonical(w[ph]))
   source_inputs.append((p.as_posix()+':'+n,len(ww)))
seen=set()
for w in worlds.values():
 for ph in ['original','revised']:
  k=canonical(w[ph]);check('input_disjoint',k not in seen and k not in exposed,w['id']+'/'+ph);seen.add(k)
# Notebook sequence and source equality (only the user parameter cell may differ).
nb=json.loads(next(R.glob('*.ipynb')).read_text(encoding='utf-8'))
packnb=json.loads((S/'notebooks/i01_course_kaggle.ipynb').read_text(encoding='utf-8'))
nbcode=[c for c in nb['cells'] if c['cell_type']=='code']
check('notebook_execution_sequence',[c['execution_count'] for c in nbcode]==list(range(1,38)),'37 cells')
check('notebook_errors',not any(o['output_type']=='error' for c in nbcode for o in c.get('outputs',[])),'all outputs')
notebook_source_differences=[i for i,(a,b) in enumerate(zip(nb['cells'],packnb['cells'])) if a['cell_type']!=b['cell_type'] or ''.join(a['source'])!=''.join(b['source'])]
check('notebook_cells',len(nb['cells'])==len(packnb['cells']),'cell count')

import ast
native=next(ast.literal_eval(n.value) for n in ast.parse((S/'recovery/i01/checks.py').read_text(encoding='utf-8')).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='NATIVE' for t in n.targets))
native_revised=deepcopy(native);native_revised[0][12]=100
exposed.update([canonical(native),canonical(native_revised)])
check('input_native_disjoint',not seen.intersection({canonical(native),canonical(native_revised)}),'native example')
check('input_separation_receipt',len(exposed)==metas[0]['input_separation']['distinct_exposed_inputs']==60,'60 exposed ordered inputs')
for ss in sessions:
 ld=ss['evidence']['load']
 check('physical_device',ld['cuda_visible_devices']==str(ss['worker']) and ld['cuda_device_uuid']==ss['evidence']['host']['gpus'][ss['worker']]['uuid'].removeprefix('GPU-'),ss['worker'])
check('physical_uuid_distinct',sessions[0]['evidence']['load']['cuda_device_uuid']!=sessions[1]['evidence']['load']['cuda_device_uuid'],'two T4 devices')

csv.field_size_limit(10000000)
report=json.loads((L/'reports/analysis.json').read_text(encoding='utf-8'))
def csv_value(x):return '' if x is None else canonical(x) if isinstance(x,(dict,list)) else str(x)
for p in (L/'reports').glob('*.csv'):
 rows=list(csv.DictReader(p.open(encoding='utf-8')))
 key={'plotting-data':'costs','plotting-outcomes':'worlds'}.get(p.stem,p.stem)
 expected=([dict(category=k,worlds=v) for k,v in report['summary']['paired_counts'].items()] if p.stem=='paired-results' else report[key])
 check('csv_projection',rows==[{k:csv_value(v) for k,v in r.items()} for r in expected],p.name)
for name,table in [('episodes','episodes'),('traces','calls'),('sessions','sessions'),('annotations','annotations')]:
 expected=[]
 for i,db in enumerate(dbs):expected += [dict(x,slot=i) for x in db.execute('select * from '+table)]
 check('analysis_raw_'+name,report[name]==expected,name)
check('analysis_manifest',report['manifest']==run,'analysis.json')
for row in report['worlds']:
 w=worlds[row['id']]
 for key in ['group','owner','first','original_truth','revised_truth']:check('world_report',row[key]==w[key],w['id']+'/'+key)
 for ph in ['prefix','retain','clear']:
  e=eps.get(w['id']+'/'+ph)
  check('world_score_report',row[ph]==(score(w['id']+'/'+ph) if e else None),w['id']+'/'+ph)
  check('world_checkpoint_report',row[ph+'_terminal']==(e['terminal'] if e else None) and row[ph+'_submissions']==(e['submissions'] if e else None),w['id']+'/'+ph)
 for ph in ['original','revised']:
  for mode in ['direct','thinking']:
   eid=w['id']+'/control-'+ph+'-'+mode
   act,_=parse(bycall[eid]) if eid in bycall else (None,None)
   expected=int(bool(act and act['submit']==max(sum(w[ph],[])))) if eid in bycall else None
   check('control_report',row['control_'+ph+'_'+mode]==expected,eid)
for row in report['costs']:
 eid=row['world']+'/'+row['phase'];c=cost(eid)
 for key,target in [('calls','calls'),('input_tokens','input'),('generated_tokens','generated'),('ready_seconds','ready'),('observed_seconds','dispatch'),('messages','messages')]:
  check('cost_report',row[key]==c[target],eid+'/'+key)
 check('cost_coverage_report',row['complete'] is True and row['attempts_unknown_ready_seconds']==0 and row['attempts_unknown_observed_seconds']==0,eid)
for row in report['paired_costs']:
 r=next(r for r in main if r['id']==row['world'])
 for key,field in [('ready_seconds','ready'),('calls','calls'),('generated_tokens','generated'),('input_tokens','input'),('messages','messages')]:
  check('paired_cost_report',row['retain_'+key]==r['retain'][field] and row['clear_'+key]==r['clear'][field] and row['clear_minus_retain_'+key]==r['clear'][field]-r['retain'][field],r['id']+'/'+key)
for row in report['policy_costs']:
 wid=row['world'];ph=row['policy'];r=next(r for r in worldrows if r['id']==wid)
 check('logical_policy_cost',row['logical_prefix_calls']==r['prefix']['calls'] and row['recovery_calls']==r[ph]['calls'] and row['logical_end_to_end_calls']==r['prefix']['calls']+r[ph]['calls'] and row['post_revision_ready_seconds']==r[ph]['ready'],wid+'/'+ph)
for row in report['validation_details']:
 c=bycall[row['call']];act,err=parse(c)
 check('validation_report',row['legal_action']==(act is not None) and row['json_valid'] and row['schema_valid'] and row['error']==err and row['recorded'] and row['committed'] and row['runtime_safe'] and not row['admission_blocking'],c['id'])
for row in report['attempt_validation']:
 c=bycall[row['call']];act,err=parse(c)
 check('attempt_validation_report',row['legal_action']==(act is not None) and row['json_valid'] and row['schema_valid'] and row['error']==err and row['recorded'],c['id'])
for row in report['protocol_compliance']:
 cc=[c for c in calls if c['id'].split('/')[0].startswith(row['group']+'-') and c['episode'].split('/')[1]==row['phase']]
 check('compliance_report',row['registered_calls']==row['recorded_calls']==row['committed_calls']==row['json_valid']==row['schema_valid']==len(cc) and row['legal_actions']==sum(parse(c)[0] is not None for c in cc) and row['unknown_calls']==row['admission_blocking']==0,row['group']+'/'+row['phase'])
for row in report['process_outcomes']:
 ph=row['phase'];ps=phase_stats['main/'+ph];cr=[x for x in callrows if x['group']=='main' and x['phase']==ph]
 expected=dict(intended_episodes=20,intended_agent_slots=40,terminal_episodes=20,unknown_episodes=0,both_submitted=ps['terminal'].get('both_submitted',0),agreement=ps['agreement'],wrong_agreement=ps['wrong_agreement'],present_submissions=ps['submissions'],known_absent_submissions=40-ps['submissions'],locally_refutable_submissions=ps['local_refutable'],episodes_with_illegal_model_action=len({x['world'] for x in cr if x['error']}),episodes_with_failed_call=0,obsolete_submissions=0,obsolete_worlds=0,terminal_reasons=ps['terminal'],unknown_submission_slots=0)
 for k,v in expected.items():check('process_report',row[k]==v,ph+'/'+k)
# Independent observable failure labels and exact call scopes.
failures={}
for eid,e in eps.items():
 if 'diagnostic' in eid:continue
 w=worlds[eid.split('/')[0]];ph=eid.split('/')[1];truth=w['original_truth' if ph=='prefix' or ph=='control-original-direct' else 'revised_truth']
 labels={}
 if e['terminal'] in ['horizon_exhausted','waiting_deadlock']:labels[e['terminal']]=[v['call'] for v in e['events']]
 wrong=[v['call'] for v in e.get('events',[]) if v['action'] and v['action']['submit'] is not None and v['action']['submit']!=truth]
 if 'control' in eid and e['submissions'][0]!=truth:wrong=[eid]
 if wrong:labels['wrong_submission']=wrong
 bad=[v['call'] for v in e.get('events',[]) if v['error']]
 if bad:labels['malformed_action']=bad
 for label,refs in labels.items():failures[(eid,label)]=refs
check('failure_report_coverage',set(failures)=={(r['episode'],r['label']) for r in report['failure_analysis']},'all failure labels')
for r in report['failure_analysis']:check('failure_exact_refs',failures[(r['episode'],r['label'])]==r['calls'],r['episode']+'/'+r['label'])
summary=report['summary']
expected=dict(intended_worlds=20,known_pairs=20,attempts=356,contingency=0,hard_limit=500,in_flight=0,campaign_attempts=356,prior_attempts=0,remaining_attempt_allowance=144,correct_prefix_denominator=10,unknown_prefixes=0,retain_successes=2,clear_successes=3,original_team_successes=10,main_revised_control_successes=18,main_revised_control_unknown=0,physical_input_tokens_observed=sum(c['outcome']['input_tokens'] for c in calls),generated_tokens_observed=sum(c['outcome']['generated_tokens'] for c in calls),physical_ready_seconds_observed=sum(c['outcome']['ready_seconds'] for c in calls),physical_dispatch_seconds_observed=sum(c['outcome']['dispatch_seconds'] for c in calls),missingness_bounds=[.05,.05],correct_prefix_mean=None,correct_prefix_interval=None)
for k,v in expected.items():check('summary_report',abs(summary[k]-v)<1e-9 if type(v)==float else summary[k]==v,k)
for key,field in [('interval','success'),('principal_effort_interval','ready')]:
 b=boot(field)
 check('bootstrap_report',summary[key]['low']==b['low'] and summary[key]['high']==b['high'] and summary[key]['constant_strata']==[],key)
check('primary_point',summary['clear_minus_retain']==boot('success')['mean'],'main success')
check('effort_point',abs(summary['principal_effort_clear_minus_retain_seconds']-boot('ready')['mean'])<1e-12,'main effort')

# Independent re-walk of the historical Course-7 state machine.
C7=Path('notebooks/run/course-7-working/latest')
c7run=json.loads((C7/'run.json').read_text(encoding='utf-8'));c7w={w['id']:w for w in c7run['worlds']}
c7calls={};c7eps={};c7attempts=[]
for i in range(2):
 c=sqlite3.connect((C7/f'worker-{i}.sqlite').resolve().as_uri()+'?mode=ro&immutable=1',uri=True);c.row_factory=sqlite3.Row
 for x in c.execute('select * from calls'):
  d=dict(x);d['worker']=i;d['request']=json.loads(d['request']);d['outcome']=json.loads(d['outcome']);c7calls[d['id']]=d
 for x in c.execute('select * from episodes'):c7eps[x['id']]=json.loads(x['state'])
 for x in c.execute('select * from attempts'):
  d=dict(x);d['evidence']=json.loads(d['evidence']);c7attempts.append(d)
c7phase={};c7re={}
for w in c7w.values():
 for ph in ['prefix','retain','clear']:
  eid=w['id']+'/'+ph
  if eid not in c7eps:continue
  s=dict(world=w['id'],phase=ph,history=deepcopy(c7re[w['id']+'/prefix']['history']) if ph=='retain' else [[],[]],turns=[0,0],submissions=[None,None],waiting=[False,False],next=w['first'],events=[],terminal=None,unused=None)
  for ev in c7eps[eid]['events']:
   cc=c7calls[ev['call']];a,err=parse(cc)
   check('c7_actor',choose(s)==ev['agent'],ev['call'])
   check('c7_action',a==ev['action'] and err==ev['error'],ev['call'])
   s=apply(s,ev['agent'],a,err,ev['call'],'Previous action invalid; no action delivered.' if err else None)
  check('c7_checkpoint',s==c7eps[eid],eid);c7re[eid]=s
for ph in ['prefix','retain','clear']:
 es=[(w,c7eps[w['id']+'/'+ph]) for w in c7w.values() if w['group']=='main']
 cc=[c for c in c7calls.values() if c['id'].startswith('main-') and c['episode'].endswith('/'+ph)]
 ss=[(w,s) for w,s in es if s['submissions']==[w['original_truth' if ph=='prefix' else 'revised_truth']]*2]
 c7phase[ph]=dict(success=len(ss),success_worlds=[w['id'] for w,s in ss],calls=len(cc),illegal=sum(parse(c)[0] is None for c in cc),messages=sum(bool(parse(c)[0] and parse(c)[0]['message'] is not None) for c in cc),ready=sum(c['outcome']['ready_seconds'] for c in cc),input=sum(c['outcome']['input_tokens'] for c in cc),generated=sum(c['outcome']['generated_tokens'] for c in cc),terminal=dict(collections.Counter(s['terminal'] for w,s in es)),obsolete_worlds=sum(w['original_truth'] in s['submissions'] for w,s in es) if ph!='prefix' else 0)
c7science=[c for c in c7calls.values() if not c['id'].startswith('hardware/')]
c7mainctrl=[s for e,s in c7eps.items() if e.startswith('main-') and e.endswith('/control-revised-direct')]
c7summary=dict(phases=c7phase,physical=len(c7attempts),science=len(c7science),team=sum('/agent-' in c['id'] for c in c7science),illegal=sum(parse(c)[0] is None for c in c7science),scalar_main_correct=sum(s['correct'] for s in c7mainctrl),ready_difference=(c7phase['clear']['ready']-c7phase['retain']['ready'])/20,settings=next(iter(c7calls.values()))['request']['settings']['generation'],seed=c7run['config']['master_seed'])

out({'assertions':sum(checks.values()),'checks':dict(checks),'anomalies':anomalies,'main_bootstrap':boot('success'),'effort_bootstrap':boot('ready'),'phase_stats':phase_stats,'course7':c7summary})
assert not anomalies, anomalies

```

## 4. Executed verification result and scope

The full standard-library verifier was executed locally against the supplied artifacts, without importing the packaged experiment or loading a model. **10,953 assertions passed; the deviation list was empty.** This count includes 206 historical Course-7 action checks and 69 historical natural checkpoint comparisons, in addition to the new run. It is a count of record comparisons, not independent experiments.

| Evidence class | Coverage independently checked |
|---|---|
| New worlds and scientific schedule | All 28 saved worlds; 56 actual inputs; independent proposals, edits, rejection counters, truth, assignment and seed regeneration |
| Natural protocol trajectory | All 308 natural team replies; 72 exact final states and literal histories |
| Scalar and supplied-view fixtures | All 36 scalar controls; all four diagnostics, including reachable scripted history and predicates |
| Attempt durability | All 356 call outcomes equal their sole completed first-attempt evidence; 348 scientific effects committed |
| Conversation JSONL | 356 exact raw call rows and 112 exact episode-state strings |
| SQLite | Both `PRAGMA integrity_check` results are `ok`; both exact manifest bindings agree |
| Portable snapshot | ZIP CRC check; all 179 file members match the extracted tree byte-for-byte |
| Existing integrity manifest | All 178 declared file sizes and SHA-256 values agree; the manifest itself is the remaining ZIP member |
| Packaged release | All 111 declared release members match; all 50 executed source identity entries match |
| Wheel/source parity | All 46 packaged Python files under `recovery/` equal their wheel members |
| Reports | All 21 CSVs match their declared JSON projections; independent outcomes, costs, process coverage, validation and exact failure-call references agree |
| Native visible text | All 354 ordinary rendered requests match the native text framing; two forced envelopes checked separately |
| Runtime bounds | Every saved input vector length, output vector length, seed triplet, local device index, cache flag and measured headroom checked |
| Notebook | 37 consecutive code execution counts, zero error outputs, identical cell sources to packaged notebook |
| Historical comparison | All 206 natural Course-7 actions and 69 checkpoints re-walked with historical feedback semantics |

Floating-point sums are compared with absolute tolerance \(10^{-9}\) seconds where accumulation order differs. Scientific outcomes, raw bytes, requests, seeds, histories, action legality, integer/token counts and intervals are exact comparisons. The aggregate ready-time difference caused by alternative summation order is below a picosecond and is not a material report discrepancy.

Supplementary read-only checks established that each of the 356 raw response strings appears with correct JSON string escaping in both the TXT export and the HTML export after HTML entity decoding. A direct search for an unescaped response would miss most entries because these surfaces preserve replies as nested JSON strings. The JSONL row equality is the stronger structural check; the other formats are presentation copies, not independent evidence.

The expanded snapshot has no companion WAL/SHM files. The SQLite files are standalone consistent backup artifacts, opened immutable/read-only. The current connections never run an update, checkpoint, worker, inference routine or report writer.

### 4.1 What was not rerun

The packaged CPU/native verification suites, tokenizer measurement, GPU headroom probes, weight download validation and actual generation are historical evidence. Their retained results and relevant implementation are inspected; this audit does not re-execute them. In particular:

- The native selfcheck receipt reports a conservative 7,634-token input bound, a limit of 8,192 and a direct resident bound of 8,704 including output reserve.
- Saved feedback token counts and adversarial literal-history measurements support release admission. This audit independently checks ordinary rendered text and token-vector lengths but does not retokenize using a freshly loaded native tokenizer.
- The runtime adapter reconstructs the entire request, including tokenization/settings/seed, inside the resident process and rejects mismatches before generation. The final saved records and installed-source receipt corroborate this path; the audit does not claim to have repeated that live check.
- No model parameters or numerical output scores are reproduced now. The 19,329,302,519-byte snapshot is represented by historical file/digest receipts, not included model weights in this 62.7 MB run folder.
- No external user-authorization conversation, paid allocation receipt or independently observed GPU utilization log is present.

## 5. Authority and source inspection

Scientific authority is [the root specification](../../../PROJECT_SPECIFICATION.md), especially §12 and its overriding assisted amendment §12.1. The executed packaged copy agrees byte-for-byte. Its incorporated [annex](../../../notebooks/run/assisted-v1/latest/source/docs/plans/i01-course-final-design-protocol-and-acceptance.md) governs literal wording and algorithms. The [final design](../../../notebooks/run/assisted-v1/latest/source/docs/plans/i01-course-final-experimental-design.md) supplies rationale. Root and packaged `AGENTS.md` agree on preservation, scientific boundaries and evidence quality.

Some design/annex headers retain their prospective “not adopted” wording from before adoption; root §12.1 explicitly incorporates them. Similarly README/implementation handoff statements about unrun GPU gates describe the software-release checkpoint, while the supplied new run empirically establishes later execution. These dated statements are not evidence that the supplied outcomes are unexecuted. They are preserved rather than edited in this documentation-only task.

The key packaged execution surfaces inspected are:

| Source surface | Inspected scientific/engineering responsibility |
|---|---|
| `recovery/i01/core.py` | Exact world generator, assignment and identity-derived seeds; strict parser; actor eligibility; terminal states; retention boundaries; permitted views; literal renderer; diagnostic constructors/predicates |
| `recovery/i01/workflow.py` | Initialization/source capture; exact precommitted plan; request/call path; raw persistence before effects; natural/control/diagnostic phases; state/headroom/pilot/main gates; fixed batches; forecast; export and shutdown |
| `recovery/i01/store.py` | Manifest/slot binding; explicit WAL/FULL connection; transactions; exact request registration; raw/effect commits; one admission owner; scoped ceilings and unresolved spending |
| `recovery/i01/policy.py` | Separate JSON/schema/action validity; public rejection feedback; runtime/admission distinction; protocol qualification; objective pilot usefulness |
| `recovery/i01/inference.py` | Frozen direct settings; native renderer; no input truncation; intentional synthetic envelope padding; exact request rebuild; memory observation; fresh-state engine interface |
| `recovery/i01/process.py`, `runtime.py` | Isolated resident processes, physical-device visibility, startup/import isolation, bounded execution and shutdown |
| `recovery/i01/report.py`, `ui.py` | Intended populations, bootstrap order, effort, compliance/process/failure references, fixed casebook and conversation presentation |
| `recovery/i01/archive.py` | Quiescent backup, file identities, export integrity and source attachment |
| `recovery/inference.py`, `t4_attention.py` | Reviewed text-only backend, quantization, numerical/cache reporting and custom T4 attention dependencies |
| Notebook/CLI/client/setup surfaces | Thin finite action orchestration, installed-source identity, receipts and export inspection |
| Packaged assisted tests and retained verification JSON | Intended CPU/native boundary checks; treated as historical software evidence |

The source release records commit `d95bb01223590bb889d4612199662266ce78968d` and one untracked planning file, `docs/plans/i01-course-design-approval-decision.md`, at packaging. The exact release manifest/file identities, not a claim that every workspace file was committed, bind the executed source. Dependencies and model weights are explicitly excluded from the source-only release. The retained installed receipt states `installed_source_matches=true` and supplies all 50 source identities; current source/wheel checks support that record.

### 5.1 Durability, replay and isolation: evidence versus inference

`Store.raw` refuses a second durable outcome and commits the outcome with the attempt's completion record. `Store.effects` requires a saved outcome and atomically updates state plus the effect flag. Exact registration rejects a changed episode/request string. The workflow returns a saved outcome before any new dispatch and recomputes branch-local effects. The final state and attempt evidence are compatible with these guarantees.

All observed calls are first attempts. No infrastructure retry, reload, timeout, pause/restore tail, unresolved-spending reconciliation or controller crash appears in this campaign. Thus no empirical claim is made that those failure paths were exercised here. The equal A1/A2 checks and per-call fresh-cache diagnostics are bounded evidence; they cannot rule out every possible unrecorded backend state.

No cross-arm continuation response is reused. Matching recovery invocation seeds are intentional coupling, while each arm's requests and effects are independently retained. The sole physical sharing is the original prefix. Source/privacy and action-order assertions reconstruct every next view from that same branch's prior legal events.

## 6. Notebook and checkpoint inventory

The notebook has 75 total cells: 37 code cells plus 38 Markdown cells. The table uses zero-based notebook cell indices and recorded UTC execution times. “No error outputs” refers to Jupyter error objects; library warnings or `[ERROR]`-prefixed documentation messages inside stderr are separately reviewed below.

| Code execution | Notebook cell | Finite action / source | Busy UTC | Idle UTC |
|---:|---:|---|---|---|
| 1 | 2 | `RUN_DIR = "/kaggle/working/i01-assisted-study"` | 2026-10-16T14:16:26.094102Z | 2026-10-16T14:16:26.104387Z |
| 2 | 4 | `from pathlib import Path` | 2026-10-16T14:16:26.106035Z | 2026-10-16T14:16:26.792406Z |
| 3 | 6 | `study.configure_session(remaining_minutes=SESSION_REMAINING_MINUTES,` | 2026-10-16T14:16:26.793481Z | 2026-10-16T14:16:26.803231Z |
| 4 | 8 | `study.install_runtime();` | 2026-10-16T14:16:26.805129Z | 2026-10-16T14:19:23.501392Z |
| 5 | 10 | `study.start_new();` | 2026-10-16T14:19:23.502451Z | 2026-10-16T14:19:29.292245Z |
| 6 | 12 | `study.check_implementation();` | 2026-10-16T14:19:29.293266Z | 2026-10-16T14:19:43.150940Z |
| 7 | 14 | `study.download_weights();` | 2026-10-16T14:19:43.151913Z | 2026-10-16T14:22:24.788879Z |
| 8 | 16 | `study.load_models();` | 2026-10-16T14:22:24.789831Z | 2026-10-16T14:23:59.177642Z |
| 9 | 18 | `study.plan_execution();` | 2026-10-16T14:23:59.178844Z | 2026-10-16T14:24:02.067523Z |
| 10 | 20 | `study.check_readiness();` | 2026-10-16T14:24:02.070108Z | 2026-10-16T14:24:19.824783Z |
| 11 | 22 | `study.qualify_direct();` | 2026-10-16T14:24:19.825742Z | 2026-10-16T14:24:41.932488Z |
| 12 | 24 | `study.inspect_qualification(mode="direct");` | 2026-10-16T14:24:41.933390Z | 2026-10-16T14:24:42.079797Z |
| 13 | 26 | `study.check_headroom();` | 2026-10-16T14:24:42.080830Z | 2026-10-16T14:26:59.804633Z |
| 14 | 28 | `study.run_diagnostics();` | 2026-10-16T14:26:59.805570Z | 2026-10-16T14:27:27.011609Z |
| 15 | 30 | `study.save_checkpoint(verify=True);` | 2026-10-16T14:27:27.012733Z | 2026-10-16T14:27:30.127326Z |
| 16 | 32 | `study.run_pilot(1);` | 2026-10-16T14:27:30.128224Z | 2026-10-16T14:29:30.646491Z |
| 17 | 34 | `study.check_pilot(1);` | 2026-10-16T14:29:30.647694Z | 2026-10-16T14:29:33.685600Z |
| 18 | 36 | `study.run_pilot(2);` | 2026-10-16T14:29:33.686643Z | 2026-10-16T14:31:03.983196Z |
| 19 | 38 | `study.check_pilot(2);` | 2026-10-16T14:31:03.984323Z | 2026-10-16T14:31:07.173039Z |
| 20 | 40 | `study.run_pilot(3);` | 2026-10-16T14:31:07.174082Z | 2026-10-16T14:32:16.617961Z |
| 21 | 42 | `study.check_pilot(3);` | 2026-10-16T14:32:16.619042Z | 2026-10-16T14:32:19.956715Z |
| 22 | 44 | `study.run_pilot(4);` | 2026-10-16T14:32:19.957666Z | 2026-10-16T14:33:36.043408Z |
| 23 | 46 | `study.check_pilot(4);` | 2026-10-16T14:33:36.044512Z | 2026-10-16T14:33:39.386658Z |
| 24 | 48 | `study.admit_main();` | 2026-10-16T14:33:39.387668Z | 2026-10-16T14:33:43.324200Z |
| 25 | 50 | `study.run_main_batch(1);` | 2026-10-16T14:33:43.325142Z | 2026-10-16T14:36:43.867439Z |
| 26 | 52 | `study.run_main_batch(2);` | 2026-10-16T14:36:43.868603Z | 2026-10-16T14:38:28.167617Z |
| 27 | 54 | `study.run_main_batch(3);` | 2026-10-16T14:38:28.168594Z | 2026-10-16T14:39:59.341618Z |
| 28 | 56 | `study.run_main_batch(4);` | 2026-10-16T14:39:59.345471Z | 2026-10-16T14:41:54.460055Z |
| 29 | 58 | `study.run_main_batch(5);` | 2026-10-16T14:41:54.461091Z | 2026-10-16T14:43:48.277640Z |
| 30 | 60 | `study.run_main_batch(6);` | 2026-10-16T14:43:48.278868Z | 2026-10-16T14:45:33.276698Z |
| 31 | 62 | `study.run_main_batch(7);` | 2026-10-16T14:45:33.277711Z | 2026-10-16T14:47:27.896753Z |
| 32 | 64 | `study.run_main_batch(8);` | 2026-10-16T14:47:27.897842Z | 2026-10-16T14:50:36.905020Z |
| 33 | 66 | `study.run_main_batch(9);` | 2026-10-16T14:50:36.906028Z | 2026-10-16T14:52:20.634315Z |
| 34 | 68 | `study.run_main_batch(10);` | 2026-10-16T14:52:20.635366Z | 2026-10-16T14:54:07.644724Z |
| 35 | 70 | `study.build_report();` | 2026-10-16T14:54:07.645873Z | 2026-10-16T14:54:16.360116Z |
| 36 | 72 | `study.save_checkpoint(verify=True);` | 2026-10-16T14:54:16.361030Z | 2026-10-16T14:54:24.556890Z |
| 37 | 74 | `study.finish_session();` | 2026-10-16T14:54:24.557939Z | 2026-10-16T14:54:41.757145Z |


The final portable boundary is `controller-close`, created at 2026-10-16 14:54:36.023166 UTC with 356 attempts. There are exactly two canonical stores, no alternate outcome store, no unexplained backup-glob accumulation, and no missing prescribed natural/control/diagnostic episode. Metadata records 53 successful exports, a maximum measured export duration 7.088498 s and last measured duration 6.488668 s. An export may contain the previous timing record because timing is recorded after the ZIP is written; these measurements should not be mistaken for 53 supplied archives.

The terminal episode inventory is:

| Type / terminal reason | Count |
|---|---:|
| Scalar control completed | 36 |
| Supplied-view diagnostic completed | 4 |
| Both agents submitted | 42 |
| Horizon exhausted | 26 |
| Waiting deadlock | 4 |
| **All durable episode rows** | **112** |

The three natural terminal classes total 72 and include pilot and main phases. A terminal record means procedural settlement; “both submitted” does not mean correct. No hardware probe fabricates a scientific episode row. All 356 calls have durable outcomes, and the scientific 348 have committed effects; the eight hardware rows intentionally have `effect_committed=0`.

### 6.1 Exact main effort by world

Every value below sums actual calls/attempts in the canonical episode; all costs are known. Prefix costs are physically shared once and excluded from these post-revision numbers.

| World | Retain calls | Clear calls | Retain ready s | Clear ready s | Clear−retain s | Retain / clear success |
|---|---:|---:|---:|---:|---:|---|
| main-00 | 6 | 4 | 41.743992 | 21.447708 | -20.296283 | 0 / 1 |
| main-01 | 3 | 5 | 24.398167 | 24.740218 | 0.342051 | 1 / 0 |
| main-02 | 3 | 5 | 23.343868 | 29.231035 | 5.887167 | 1 / 0 |
| main-03 | 4 | 6 | 29.373065 | 33.229143 | 3.856078 | 0 / 0 |
| main-04 | 4 | 5 | 25.173202 | 28.371294 | 3.198092 | 0 / 0 |
| main-05 | 4 | 3 | 23.659775 | 17.300879 | -6.358896 | 0 / 0 |
| main-06 | 6 | 5 | 35.565056 | 31.911261 | -3.653795 | 0 / 0 |
| main-07 | 6 | 6 | 33.735356 | 37.174511 | 3.439154 | 0 / 0 |
| main-08 | 6 | 4 | 39.169575 | 23.722245 | -15.447330 | 0 / 0 |
| main-09 | 3 | 4 | 22.195672 | 25.233017 | 3.037346 | 0 / 0 |
| main-10 | 6 | 3 | 35.492498 | 19.081588 | -16.410910 | 0 / 0 |
| main-11 | 3 | 6 | 21.139247 | 36.707406 | 15.568158 | 0 / 0 |
| main-12 | 6 | 6 | 33.727384 | 28.843291 | -4.884092 | 0 / 0 |
| main-13 | 4 | 2 | 26.685220 | 16.393167 | -10.292054 | 0 / 0 |
| main-14 | 4 | 5 | 25.103680 | 32.761410 | 7.657730 | 0 / 0 |
| main-15 | 6 | 4 | 33.423748 | 23.945233 | -9.478515 | 0 / 1 |
| main-16 | 5 | 2 | 42.135935 | 15.106966 | -27.028969 | 0 / 0 |
| main-17 | 3 | 4 | 18.207589 | 20.729763 | 2.522174 | 0 / 0 |
| main-18 | 3 | 4 | 16.879426 | 30.567120 | 13.687694 | 0 / 0 |
| main-19 | 6 | 2 | 37.625362 | 16.617657 | -21.007705 | 0 / 1 |


## 7. Receipts, logs, figures and report interpretation

### 7.1 Setup and runtime receipts

The receipt directory contains the historical native/scripted selfcheck plus one setup session (`7785ff79-9fb0-47c3-bedf-b47406d709af`). Every receipt file is in the hash inventory below.

| Receipt | Evidence / limit |
|---|---|
| `selfcheck.json` | Passed scripted mathematics/state/durability/budget/input-separation checks and native tokenizer bounds; zero model attempts |
| `environment.json` | Isolated runtime identity, source/lock/wheel identities, paths, versions and 174.928104 s setup duration |
| `host.json` | Linux/Python host, two Tesla T4 names/UUIDs, driver 580.178.04 and writable/free filesystem observations |
| `dependency-install.json` | Pinned installation transaction metadata and environment record |
| `installed.json` | Package versions, installed-source match and all 50 source identity entries |
| `metadata.json` | Metadata/tokenizer assets, checkpoint revision and snapshot paths before weights |
| `weights.json` | Twelve checkpoint/metadata files and digests; total 19,329,302,519 bytes, including four Safetensors shards |
| `pip-bootstrap-wheel.json` | Verified pip 26.2.1 wheel identity and source URL |
| `startup.json` | Isolated `-I -S` startup, site processing disabled, hook not automatically imported, explicit site paths |

The two resident session rows give successful model loads with no missing, unexpected or mismatched parameter keys; actual tensor devices are local `cuda:0`, with physical device mapping 0/1 and distinct UUIDs. Weight dtype/device dictionaries document the chosen quantized/FP16 load and selected FP32 buffers. They are stored measurements, not a new local inspection of live tensors.

`receipts/controller-stderr.log` has 1,267 lines. Its error/warning matches include Transformers documentation-signature messages for `loss`/`logits`, bitsandbytes/PyTorch future warnings, and unavailable fast-path notices. The two documentation `[ERROR]` messages per model load are not exceptions or failed calls. No traceback or failed scientific outcome accompanies them. The selected recurrent fast path is false in both load receipts. No unsupported causal explanation of task errors is inferred from those startup warnings.

The ten setup logs cover venv creation, pip bootstrap, isolation acceptance, dependency installation, project installation, installed metadata, metadata download, startup, dependency consistency and weight download. They show successful installation and `No broken requirements found`; the two download logs include unauthenticated-Hub rate-limit warnings. These warnings concern access/performance and do not show altered model outputs. No secrets are needed or exposed in the analysis.

### 7.2 All report surfaces

All 21 CSV files are structurally compared to the saved `analysis.json` projection; independent canonical checks then establish the substantive values rather than relying on that internal agreement.

| Report surface | Role and interpretation |
|---|---|
| `worlds.csv`, `plotting-outcomes.csv` | All 28 worlds; qualification natural phases are unplanned, not failed; main/pilot scores independently verified |
| `paired-results.csv` | Counts only present paired categories; the absent both/unknown categories are zero and must be shown explicitly when reporting |
| `costs.csv`, `plotting-data.csv` | 72 natural episode cost rows; every attempt included, with complete effort coverage |
| `paired_costs.csv` | Twenty same-world recovery differences, including input/output/calls/time/messages |
| `policy_costs.csv` | 48 pilot/main policy rows; logical prefix sharing, not extra physical execution |
| `attempts.csv` | All 356 physical admissions/outcomes, settings, seeds, device/PID, token/time measures |
| `qualification_controls.csv` | Eight planned qualification scalar outcomes; distinct from main recovery |
| `diagnostics.csv` | Four fixture targets, legal actions and exact pass predicates; no aggregate gate |
| `pilot_checks.csv` | Four complete durable pilot scopes and health checks; “passed” is not recovery correctness |
| `validation_details.csv`, `attempt_validation.csv` | 348 scientific calls/attempts; syntax/schema/action legality separately represented |
| `protocol_compliance.csv`, `attempt_compliance.csv` | Fifteen group/phase strata with behavior-dependent call denominators |
| `process_outcomes.csv` | Three main-phase rows, intended forty-agent-slot coverage and terminal/agreement/refutation/obsolete metrics |
| `failure_analysis.csv` | 63 overlapping episode/label rows with exact offending-call or episode-context references; not 63 independent failures |
| `casebook.csv` | Six deterministic categories; four present, two absent; human review remains pending |
| `sessions.csv` | Two resident load/process-close records |
| `annotations.csv` | Empty; no historical human annotations |
| `prior_spending.csv` | Empty for this independently initialized campaign, distinct from the separately noted historical 45 attempts |
| `analysis.json` | Rich combined reconstruction; raw row fields independently matched to SQLite |
| `overview.md`, `overview.html` | Generated narrative/displays; claims checked against canonical results and their definitions |
| `conversations.jsonl`, `.txt`, `.html` | Canonical field copies and human-readable presentations, not additional independent observations |

The empty CSVs contain two bytes rather than fabricated zero-valued annotation or prior-spending rows. Their emptiness is a meaningful absence of recorded review/prior charges, not missing main outcomes.

The 63 failure-label rows comprise 29 episode labels for wrong submission, 26 for horizon exhaustion, four for waiting deadlock and four for malformed action. The malformed count is affected episodes, not six offending calls. The wrong-submission labels include the two wrong scalar controls. Labels overlap and span pilot/main/control scopes; they cannot be summed as exclusive causal shares.

`overview`'s human-review and gate fields retain their actual pending/completed distinctions. This AI-assisted audit does not retroactively set any review flag or alter its original prose. A reader should use the new independent analysis for methodology/results claims and the raw rows for verification.

### 7.3 All eight figure pairs, visually inspected

Both PNGs and SVGs are hashed. All eight PNGs were opened and visually read; SVG names/text/inputs were inspected with the report source and CSV/JSON values. No new image was generated or old image edited.

| Figure | Verified plotted quantity | Reporting caution |
|---|---|---|
| `paired-outcomes` | Both 0, retain-only 2, clear-only 3, neither 15, unknown 0 | Twenty paired worlds; do not infer equivalence from low counts |
| `qualification-outcomes` | Eight correct direct controls | Explicitly qualification, not a main recovery result |
| `qualification-effort` | 18.838417 ready seconds and 128 generated tokens, 8/8 raw outcomes | Excludes pilot/main and hardware envelope cost |
| `recovery-ready_seconds` | Twenty retained/clear pairs; correct outcomes use circles, failures crosses | Mean/interval needs canonical paired calculations; small quick failures can look efficient |
| `recovery-calls` | 91 retained versus 85 clear calls across worlds | Early termination is not necessarily desirable |
| `recovery-generated_tokens` | 3,411 versus 3,194 | Input and output costs differ; input history cost is omitted from this particular plot |
| `failure-labels` | Episode/label counts 29 wrong, 26 horizon, 4 deadlock, 4 malformed | Mixed stages and overlapping labels; not causal failure attribution |
| `termination-coverage` | 42 both-submitted, 26 horizon, 4 deadlock, 36 controls, 4 diagnostics | Mixes all 112 episode types; “completed control” does not certify correctness |

The recovery plots use displayed world positions 1–20; position 1 corresponds to ID `main-00` and position 20 to `main-19`. Their generic legend symbols are supplemented by the title's circle/cross convention; a policy-colored cross is still an unsuccessful episode. All unknown-cost omissions are vacuous here because coverage is complete. For later report export, a new caption should retain scope, denominators, outcome markers and the indexing convention rather than silently reinterpret an existing figure.

## 8. Artifact identity and complete run-folder inventory

The starting folder contains **181 files, 62,660,773 bytes**, including the final ZIP and executed notebook. The ZIP contains 179 files and expands exactly to `latest/`. Paths below are relative to `notebooks/run/assisted-v1/`; each size and SHA-256 was calculated from the actual current bytes.

This inventory is an analysis record of existing artifacts, not a new experiment identity system or a second outcome database. It reuses the supplied artifact paths and allows the preserved snapshot to be recognized independently.

| Relative path | Bytes | SHA-256 |
|---|---:|---|
| `latest.zip` | 4129815 | `5dd5ba2af2a2b85df32f4d0fdd2e6e58105e4649dfc5ba2737f129624dd278c3` |
| `latest/integrity.json` | 28876 | `c979b8228a632d55086a687303e89b8bebd5cef38f334dc90f38e07ff92ce200` |
| `latest/receipts/controller-stderr.log` | 156465 | `2d9a3c685faa1b91fedb0344a3b8acc6100d707894f4b27ccceec26631d1ba44` |
| `latest/receipts/selfcheck.json` | 92454 | `9327a329582539fcab1142ffed3f12aef0d90af28648dfc72ef3db3d1082848c` |
| `latest/receipts/setup/7785ff79-9fb0-47c3-bedf-b47406d709af/bootstrap-pip.log` | 267 | `ddfbd3d4b29160ff983092fa2eea25bacd850bc4517e473c3b7e8aa38b1775c3` |
| `latest/receipts/setup/7785ff79-9fb0-47c3-bedf-b47406d709af/dependencies.log` | 27989 | `af3b54888ef93689fea54f5b0a3072e186d6d51c141f80fc3a726d869ac00dc7` |
| `latest/receipts/setup/7785ff79-9fb0-47c3-bedf-b47406d709af/dependency-install.json` | 1187181 | `e4ecb26bce93b73b6ac4d250be4fb1636c2c6f6ad042b4424b44b09deb66e218` |
| `latest/receipts/setup/7785ff79-9fb0-47c3-bedf-b47406d709af/environment.json` | 15067 | `5feeb03056e33d02f5b3169ec00119aec0568c249321e44a62347ee0c17afd47` |
| `latest/receipts/setup/7785ff79-9fb0-47c3-bedf-b47406d709af/host.json` | 994 | `315cfb15ec800393c51c8823341eeae5e1b086ee4e860dc71ca6b0211e7dd3b2` |
| `latest/receipts/setup/7785ff79-9fb0-47c3-bedf-b47406d709af/installed.json` | 7804 | `6df7f0f21290b0a5255ca55b3563895df465effd6e2577908bc16ba9c88401fb` |
| `latest/receipts/setup/7785ff79-9fb0-47c3-bedf-b47406d709af/installed.log` | 7824 | `c25465b8454de2fa509dd3a8407412e5a27a9200815af3cf26aeb9eae2a4ec98` |
| `latest/receipts/setup/7785ff79-9fb0-47c3-bedf-b47406d709af/metadata-command.log` | 2584 | `fe1a0253f6797bc4c374f64ada8c5351c3342454e94ffca8318c704ec941a455` |
| `latest/receipts/setup/7785ff79-9fb0-47c3-bedf-b47406d709af/metadata.json` | 1420 | `e54cb2634628cabafaf3e2c1181d87a337b138e64f8ef09cff1b23228e7f66ae` |
| `latest/receipts/setup/7785ff79-9fb0-47c3-bedf-b47406d709af/pip-bootstrap-wheel.json` | 338 | `dcb61b3df68779b0139b5db87c1bb2852063f1fe1567976787f29bc018c7919c` |
| `latest/receipts/setup/7785ff79-9fb0-47c3-bedf-b47406d709af/pip-check.log` | 50 | `7ec09312d4d4a1a3c07d19cd6b9c01cdaf0b3f714362e8bc56b3a8d0ae91ebed` |
| `latest/receipts/setup/7785ff79-9fb0-47c3-bedf-b47406d709af/pip-isolation.log` | 61 | `9ac004ab333646cb8b33b5cbded84912e8fa3a4be885054163fecdd4331c5575` |
| `latest/receipts/setup/7785ff79-9fb0-47c3-bedf-b47406d709af/project.log` | 237 | `1f6d625b5e7000d69d1ed8d0ea598fbd1e2ec3f6a2c0ece6929ec61318b6b072` |
| `latest/receipts/setup/7785ff79-9fb0-47c3-bedf-b47406d709af/startup.json` | 905 | `6befac2db86ea6a7a5c8d899c4867f1554be440690ca40f4c5a9ddb99269df81` |
| `latest/receipts/setup/7785ff79-9fb0-47c3-bedf-b47406d709af/startup.log` | 855 | `b66ddfd392e056d4bd45d048449fb0daf2d4d8c957b6dadcecedd175a4dcdc2c` |
| `latest/receipts/setup/7785ff79-9fb0-47c3-bedf-b47406d709af/venv.log` | 15 | `000d57778d77b1c8786eedfb938aabfc27b5364329f7b71ec68df17963507dc0` |
| `latest/receipts/setup/7785ff79-9fb0-47c3-bedf-b47406d709af/weights-command.log` | 3698 | `efc394cf48975f805cd8599814bca7d8e33dc077f3c6e8e947c724eaf4fd3db2` |
| `latest/receipts/setup/7785ff79-9fb0-47c3-bedf-b47406d709af/weights.json` | 2106 | `7c634fcfba30016703e053d90fea0667fcd4902fd3fa023ac9661266d390139c` |
| `latest/reports/analysis.json` | 14975407 | `2424684dcbb974018f886cba6bf4cb851998362a79f8d38afb54bdde1db8a77c` |
| `latest/reports/annotations.csv` | 2 | `7eb70257593da06f682a3ddda54a9d260d4fc514f645237f5ca74b08f8da61a6` |
| `latest/reports/attempt_compliance.csv` | 630 | `d0220e96b4ac46cf1445a1d21695107e3ce08487585f1d6d70a4451f2b433fcb` |
| `latest/reports/attempt_validation.csv` | 30521 | `ff485bf4424daa49c8c536223d6012ae40b55e2e58e2a519ff9103527f9f6393` |
| `latest/reports/attempts.csv` | 3694073 | `1e9f3af0e12abdd043770dea17a3a393bfaa70fe26889efdf9deafc12507b1e3` |
| `latest/reports/casebook.csv` | 3103 | `e46945f42d962ad7ab571e0e9c03dbec3f15793507a52de6570b5085fe0930f9` |
| `latest/reports/conversations.html` | 2999665 | `87ab6060edb739382d27e81724ecc4c390edbd13dc28842c2daf1b1a710fe94c` |
| `latest/reports/conversations.jsonl` | 9044073 | `786971053ea770a266d9780dc3619708877d44af8e57200da9894d39654d111a` |
| `latest/reports/conversations.txt` | 2512140 | `72b429a102dd723c9b5a7b6c69bf1fb7f19829471f6091cfd24005ad7c137bc9` |
| `latest/reports/costs.csv` | 7602 | `a43bab8eefb7023d422fba0a8bb3653b1b81b09077780db4115183c7695ea342` |
| `latest/reports/diagnostics.csv` | 1435 | `4c6534f3cfe2ecf4f3e69acd16d459829e4c1e61793177211abc0f64b4fd62c0` |
| `latest/reports/failure_analysis.csv` | 14919 | `eb2fd494a826491667ba40dc75a4766602042bfcf4efa14436f3bfc4d87b6d92` |
| `latest/reports/figures/failure-labels.png` | 49409 | `67d55442bc97a00734789cd163122594a8ed28261a3c1d4570577b873fc95380` |
| `latest/reports/figures/failure-labels.svg` | 34227 | `73f68905536c842f55cb211ebe2da97caccf389447336000605d6960f5a2e07e` |
| `latest/reports/figures/paired-outcomes.png` | 36652 | `f02425591e921ea700fe1ab32ca1c5303cb222402cc1534029873e308be3f9bc` |
| `latest/reports/figures/paired-outcomes.svg` | 29091 | `2411136e2d447a0100f87feea522259c7853454112e0d4b61a0d8d3468fbdef2` |
| `latest/reports/figures/qualification-effort.png` | 57515 | `6cfad00c628873416ddcfa6a1862f6b46b8baee5d5da09d91308a4c26d48dc0f` |
| `latest/reports/figures/qualification-effort.svg` | 39377 | `59a393992c04afc4354ffcd1a0c941f52653020272d3053a8846d00990bc1682` |
| `latest/reports/figures/qualification-outcomes.png` | 47894 | `7f6c2d676aa6905d0f11995f19199da3c18e1d2b979fe084820bcfe74d9dbcc6` |
| `latest/reports/figures/qualification-outcomes.svg` | 33439 | `8fd6681cdaec8e215f512ae28d0b1791faeb3a1dfb3f8afd1c405ff7c65e7a36` |
| `latest/reports/figures/recovery-calls.png` | 56774 | `2f82578cfb62703a8fa881e1f4219a9c8e72c554b9d18ca245b34087e7afee2b` |
| `latest/reports/figures/recovery-calls.svg` | 51665 | `f21d89277701ea059e8931b016815aff00cbc0cff3a7ace712b82b919424a9ae` |
| `latest/reports/figures/recovery-generated_tokens.png` | 70287 | `79d68d934340c550fefccc5248796725e07ce1aa0ff462aae120d9edc7ff7c9f` |
| `latest/reports/figures/recovery-generated_tokens.svg` | 53101 | `93c325477b9dd4091a5776be101d2c3a75920ceb977299fffaf14be4d2ec2fd5` |
| `latest/reports/figures/recovery-ready_seconds.png` | 64587 | `679570d6e5756825c1e24b8e92aff51af54f621f8dc2578ede7f68829330270d` |
| `latest/reports/figures/recovery-ready_seconds.svg` | 50103 | `053b69e1dc70ba2aa17e559c44f4a71c65d1adc56bce0b9d68ea2201d5afd560` |
| `latest/reports/figures/termination-coverage.png` | 43115 | `cd0d4cb31d7511d2a58fb4c4164df35b8780d0515aa16e6acbc0ba8100218fbf` |
| `latest/reports/figures/termination-coverage.svg` | 31205 | `24790dcee3c4d9934811726c80139a7bd3e321c8051eb1ac7b98434a28627a54` |
| `latest/reports/overview.html` | 1283044 | `74a50567ce20c7a54fdc764c580ad8d8a4c403943ea9aa4dc9f5f3fd4057c3a2` |
| `latest/reports/overview.md` | 976613 | `1722954f74a1f49144d3b7e758e1f29b139f566eab54bc26ea11d2b70c1c12ee` |
| `latest/reports/paired_costs.csv` | 2638 | `e1cfc3e0eda95d546a4837e55a18bd12d2d43be2a9c6bbea1e6eddc664ba905c` |
| `latest/reports/paired-results.csv` | 54 | `0827071fca58daa7554ffe03a2477ce07eb9389678b8b7e187eb36fc066df878` |
| `latest/reports/pilot_checks.csv` | 1270 | `2edc338edf305f97c49d05060b1f56e8e856f0b1e5edee8e16ec3871732beb0f` |
| `latest/reports/plotting-data.csv` | 7602 | `a43bab8eefb7023d422fba0a8bb3653b1b81b09077780db4115183c7695ea342` |
| `latest/reports/plotting-outcomes.csv` | 4209 | `1db6cf5d066a27ac482dfc3ba9bd001939db77a3e3559ff3eeb894f70f66f765` |
| `latest/reports/policy_costs.csv` | 4849 | `edf6d42c73ef88cfdc7beafbe0c79587d24a6eb2d8bf56c92e5766e19e412ddc` |
| `latest/reports/prior_spending.csv` | 2 | `7eb70257593da06f682a3ddda54a9d260d4fc514f645237f5ca74b08f8da61a6` |
| `latest/reports/process_outcomes.csv` | 1076 | `835183de533e76b3157de0455de092cecbe4a8e04552d3bdbaf478957846e005` |
| `latest/reports/protocol_compliance.csv` | 780 | `e4cb70c066dcc7f46ec975ea9f41d8e1273c917fd5fb252868eefcd804c508f9` |
| `latest/reports/qualification_controls.csv` | 1245 | `65ec7b0197a0ca8a0e430cbe7c68d6f93743c258f93f98af068f9e62b7fc7d30` |
| `latest/reports/sessions.csv` | 437773 | `fd936a2e0401b07c9ed1068b1ce50622445cb9d87fcffe895d68cf89aa2f7410` |
| `latest/reports/validation_details.csv` | 47396 | `cb82f0782e5cf4e546351ae95c6b0bac5165f3e5e33aadaed0739c39405077e3` |
| `latest/reports/worlds.csv` | 4209 | `1db6cf5d066a27ac482dfc3ba9bd001939db77a3e3559ff3eeb894f70f66f765` |
| `latest/run.json` | 77997 | `c69b4b40bd77b4908c4280ce74539656348a82f838c91e6f9aa57101a1a03e04` |
| `latest/source/AGENTS.md` | 5298 | `eada811d4c6505f22a80fcdc95e776a27bb616b3fe87355163085fbe38491b39` |
| `latest/source/configs/i01-course-assisted.json` | 1119 | `9439d1ad7638cd1561c0b262bce1e54cfe5da01d818b880b78f394fc2d7bd9b1` |
| `latest/source/configs/i01-course.json` | 1085 | `89e91b0e69f8f0851083e5016020b30c1d0b635dc5a00f142f9955bdd60c9a23` |
| `latest/source/configs/i01-runtime.lock` | 38059 | `5b1d91aa431a39ff725cfe4314706fe7a854af85a6e3ea492dd22d8c68d9bc56` |
| `latest/source/docs/I01_KAGGLE.md` | 25509 | `439bc3b4c2fa43e93fa94094629b36b1b5dbee80f1cfab2bef9a536bc3fca61d` |
| `latest/source/docs/plans/i01-assisted-implementation-progress.md` | 4780 | `99673dfc052e4ebc143f2e79d8a1eb2913a840d8f1b2deec81a43a4cf0c3ef63` |
| `latest/source/docs/plans/i01-course-final-design-protocol-and-acceptance.md` | 32333 | `9e180efc062d6e64756805920144dfdfddf517dd6bcb050aa106c2070c1fa21a` |
| `latest/source/docs/plans/i01-course-final-experimental-design.md` | 25895 | `887b3325d8cbc04ccc8d27fb773d466f1f048b8bed82968fb720513d9f3c01a8` |
| `latest/source/docs/plans/i01-course-implementation-wbs.md` | 100306 | `54798c8c127c020844e19b6ab6452666cfebf6c895da0991b2e06c6b449bf72f` |
| `latest/source/docs/plans/i01-notebook-natural-workflow.md` | 26733 | `404f81d4058de9caa7cdfd1fee89bab2631207f17467a243eb7e19e561602273` |
| `latest/source/docs/proposals/i01-course-5-fix-and-improvement-proposal.md` | 28491 | `455cdcafa6a002530203e6cc39d4266f68a9ddd8a2cf799a21275569887bfed6` |
| `latest/source/docs/proposals/i01-course-6-fix-and-improvement-proposal.md` | 28136 | `13d0c52b001006b1d1a006d1dc5f0788704176342190f691208e87845d46c067` |
| `latest/source/docs/validation/i01-assisted-implementation.md` | 7743 | `06a0107b8238ec7768718e3f208ef0a32cb77881f4e161461bf8589858be24ac` |
| `latest/source/docs/validation/i01-course-1-repair.md` | 6083 | `8af5d6ef0f4c2016ef5f29f5d83a003faaaab08c39b5d20a63db15c16784301e` |
| `latest/source/docs/validation/i01-course-3-repair.md` | 10234 | `ea1dc697eb84398af8075f4aa1dd168aefbf5b98fbf0485716951b2fe4abbc72` |
| `latest/source/docs/validation/i01-course-4-run-all.md` | 7225 | `29f941a9f6409da784907fb68e38c36d6dfef532fcea1b94eb9dcd35ec8c081c` |
| `latest/source/docs/validation/i01-course-5-repair.md` | 8041 | `08c3336aad26f37634e5f04075124f358f1216946f2a28b3db61b11296f4e2d6` |
| `latest/source/docs/validation/i01-course-5-results-analysis.md` | 26094 | `74693517545d7b5320e1330e68f37d3b806df1f2864ffd439337f357b32703eb` |
| `latest/source/docs/validation/i01-course-6-repair.md` | 10257 | `e53e67d2f213f3cfdd026e648cee8aafcc4d5f2331b6784cbb47b1f5000448f7` |
| `latest/source/docs/validation/i01-course-6-results-analysis.md` | 27604 | `be466b2ceb138f410f979b28217944b452355f39ea08ffcd2d91a0bfd80d7db7` |
| `latest/source/docs/validation/i01-fresh-run.md` | 4501 | `fcc43448d6f9a58baea89c8738f2d8967f52c51c10b481dc4d9e2e741bef8aa0` |
| `latest/source/docs/validation/i01-implementation.md` | 14832 | `1fb7a8291bb3885d628b0832c89e09b9a1c8d9d703de348dcf96ac163bd6a441` |
| `latest/source/evidence_and_action_in_llm_teams-0.1.0-py3-none-any.whl` | 272626 | `28750203d2e716e1d62da574f9270344857e5e4c31a4cf7547c8847e9aa4bcb7` |
| `latest/source/notebooks/i01_course_kaggle.ipynb` | 39212 | `baa68dd3c811432a64a6e22b5f060a6dc4ceaf0fe2ddaf8217a77823df6b66ff` |
| `latest/source/notebooks/i01_course_research.ipynb` | 39212 | `baa68dd3c811432a64a6e22b5f060a6dc4ceaf0fe2ddaf8217a77823df6b66ff` |
| `latest/source/notebooks/validation/i01-development/assisted-core-checks.json` | 523 | `dab330dae0987b2cdf22354c096b1431c07702607345efbb60dce52cbdbaae66` |
| `latest/source/notebooks/validation/i01-development/assisted-final-source-checks.json` | 16315 | `ae13f0b716f943ee52a167853831a0ee4893255412a545d9b8197f1ab2430a4c` |
| `latest/source/notebooks/validation/i01-development/assisted-workflow-report-checks.json` | 805 | `3e769dbd466e0e5e6394c9837590796b87f3160a14d1fa9cb7022dcdf74bd5e4` |
| `latest/source/notebooks/validation/i01-development/course3-core-checks.json` | 5186 | `3238fbfb93529729cbd9ed9ec4eabcd0459bd0ec84bdcf5232154298c932fd99` |
| `latest/source/notebooks/validation/i01-development/course3-final-checks.json` | 5815 | `9ce79283551cb7b63a188af38e234ce143819ebfeb3e72f5e5e3458b51b64767` |
| `latest/source/notebooks/validation/i01-development/course3-format-checks.json` | 1555 | `60b5eec539fdba5c87c584cde4e65dbb6f91f05b46f22230a4b0f7efece4eee0` |
| `latest/source/notebooks/validation/i01-development/fresh-run-checks.json` | 1218 | `fe4de2f042b5c59887c81dc5ce9d6473c714c582cf74454ded64b6320aed60f4` |
| `latest/source/notebooks/validation/i01-development/outcomes-checks-summary.json` | 12083 | `d052e07ef5a6c4eb1316681aa843e6d7dbfd25250c642a599657fac1d70aaf70` |
| `latest/source/notebooks/validation/i01-development/outcomes-focused-checks.json` | 5231 | `819cb850539542f46dc0b2581617faf7eab9a71960c94975f1890b2762899875` |
| `latest/source/notebooks/validation/i01-development/outcomes-forecast-checks.json` | 5152 | `9efac6a12d2c896b99e48b20a6150f5355978e4dd962cbb31224dbea7e999a8a` |
| `latest/source/notebooks/validation/i01-development/outcomes-guard-checks.json` | 5118 | `2d73ff6fcfad5e3254b4a2d3fa67d4cb266202e3ca04c2e943cbe8fcc666e2d9` |
| `latest/source/notebooks/validation/i01-development/outcomes-saved-evidence.json` | 2105 | `82110484add4806b44afcff20e0b8c9f5bde3b37cbc228f2f1508ae184a47aa7` |
| `latest/source/notebooks/validation/i01-development/recovery-admission-checks.json` | 541 | `ade5209d5311ad623e5bbd9ef6ccd9e6da588a79c6b77593d760be9772fdfadb` |
| `latest/source/notebooks/validation/i01-development/recovery-final-checks.json` | 5336 | `3915aa5a110d28fb5189a9d4b9b154a711e6c18e1360c987d4bcae1e46327290` |
| `latest/source/notebooks/validation/i01-development/recovery-guard-checks.json` | 5678 | `77737bd85aa98bfaccdc4d23f18b0e81bee37639231e636f88be8c7f1d02d59c` |
| `latest/source/notebooks/validation/i01-development/recovery-saved-evidence.json` | 1429 | `f7cdb733aff1ff5dfbd1fa18d29013df087a8f68fff08ec867d076b5bbc0a361` |
| `latest/source/notebooks/validation/i01-development/run-all-checks.json` | 6382 | `8abcb15ad17edf8f12e52b5ee698b306f960c633acd7b09cdfc6e80a48bdfb0f` |
| `latest/source/PROJECT_SPECIFICATION.md` | 105945 | `4a3d2d5e0bfa24cba95ab20c9d1b33b3d19e731bf2a603e1de0f09d1b9736392` |
| `latest/source/pyproject.toml` | 693 | `d851f00351b3221aef8c92b5757aecf477f2942b03afbfb6925190220b1494b1` |
| `latest/source/recovery/__init__.py` | 81 | `b11591ab36164605ffe2de304b0503780e6b2c340b2c466e51b9c132dae0d738` |
| `latest/source/recovery/__main__.py` | 17835 | `a32e2fa488314eae101a42fb5520951565d7ab5f5c9f36aa4feeac88c529325a` |
| `latest/source/recovery/accounting.py` | 44484 | `4b910adf52a7583550fc60d8a201671e2a13d125cd4bfe67588acb85df3315d1` |
| `latest/source/recovery/analysis.py` | 31519 | `3740e341f07dfd3884363cf24935bdbf3b93de49e99b31b2b935928b46aa9e22` |
| `latest/source/recovery/attempts.py` | 13265 | `bac975625c7da55d5abcd4d2d75ba6ad91bb1cdd5b23028ff90794c84e502eb4` |
| `latest/source/recovery/costs.py` | 35346 | `6e2f8358177c00313b1f71fb755ec3bbb1b522d38e60ad22fabe8aec939bf82b` |
| `latest/source/recovery/edits.py` | 4821 | `bc378e9c65bb6abe243416b20b54be8a59eadb15fe2b70c2c4ce46527ab064fc` |
| `latest/source/recovery/evaluate.py` | 39314 | `2beb6d6f14ad10c7f474208ed66e9cca76b9ebb2880c7201ff351491884e1ec8` |
| `latest/source/recovery/events.py` | 5427 | `500ad12f8d68ee760e4fa2b2108089119f281b8d98db83113abe3e4a067d6704` |
| `latest/source/recovery/figures.py` | 14564 | `fab52110727c3dc9b8ed3e1da3a015fb1a437119e560be64cd36499b39c285c9` |
| `latest/source/recovery/i01/__init__.py` | 452 | `f459e50fe18b6916694ebce30b06ce75ff2e49f74a5ced478f33be045d95c0bc` |
| `latest/source/recovery/i01/archive.py` | 6132 | `836a5d1cf5296eccbcb72f2f40e9b2e37d549307ca164a5479b9741623c65697` |
| `latest/source/recovery/i01/checks.py` | 16783 | `eec39e76668cd9c1db98c1933b6737bed83de44ca37308be9e4c0f7f7a998e5e` |
| `latest/source/recovery/i01/cli.py` | 14101 | `51a012545e67b6c3d01c131657b2c627fff9be013e9920d2d386128001a200d8` |
| `latest/source/recovery/i01/client.py` | 7153 | `fbc6b2a31f63932831d55990479be2e69a3eb0ebe808cb1af4a150a2817f90b4` |
| `latest/source/recovery/i01/continuation.py` | 18839 | `faa58b3a463253ba241ac5c8b4ea23e4d171b57207a2dc0497867cfd3e869ea1` |
| `latest/source/recovery/i01/core.py` | 21162 | `8c10bcfaef0e5f862d5e34d25efeeccdb5db59bebb76e4f80c4dcf4859c9229e` |
| `latest/source/recovery/i01/inference.py` | 7026 | `af346cebfa65e3c3ef5de9667c59670b519ea08f0ba71d19e8ac1ce45dd10605` |
| `latest/source/recovery/i01/notebook.py` | 4037 | `4633fd8776ab5dd4c0ea70963f150ad4b17ccc9dcc2a937e79cc5399fac62bb2` |
| `latest/source/recovery/i01/policy.py` | 10176 | `3462a74d70b11b15b9d8f0f0a847f0484ecc593d400f771343175388facd6549` |
| `latest/source/recovery/i01/process.py` | 5199 | `17314150320b97c8d07edd3262d117db1f59c6b1c41728f48a45434cffe24fb0` |
| `latest/source/recovery/i01/report.py` | 58067 | `1f513cac2215472fb8814234ea2a6558182efdaec77228114664e8b6cf7c9b96` |
| `latest/source/recovery/i01/runtime.py` | 2666 | `39fb2de57d5401c0ad553e4dd0da78159442f39bd3f281dacfa464ee0c2ed09b` |
| `latest/source/recovery/i01/setup.py` | 16103 | `f75ecb3083b9826b525c4b21c32e0ecc4e962ccb94fb158c62d9c694a3169c56` |
| `latest/source/recovery/i01/store.py` | 17859 | `c09dc2b50652821cd48ce64ecdd881b388e410677de014f6992b4bca1b7e704b` |
| `latest/source/recovery/i01/ui.py` | 53952 | `16065a8a9fb382be4e9addd27f3550ff7c22d869c3c17be91529da1c7d657ea4` |
| `latest/source/recovery/i01/workflow.py` | 73551 | `859472317b7a17d068b1e8c277679344fd3fef0012b99ebcf168b8cb441d8c28` |
| `latest/source/recovery/inference.py` | 24709 | `561386a74cc951a24cc08457665d71ee77d0075aca1794a5946d6d7fe52ee026` |
| `latest/source/recovery/information.py` | 41391 | `9c8bf958955b60e73ac26ac565831cee5e45e8e52f4244e88b43345e46c1df19` |
| `latest/source/recovery/manifests.py` | 7211 | `f6157e9f945b5f185ad5dde079e5b5e902665b644b9b9ba3a58936cdfa895b82` |
| `latest/source/recovery/populations.py` | 15563 | `808c4f29a0b7cb90574d040d9f49e402291a6eadd2bacc2141f50cf97fba05c7` |
| `latest/source/recovery/prompts.py` | 18364 | `a3cefd5d802cef08233a7b404cfd01f328dd3469db7d23857db25aadefd45cdc` |
| `latest/source/recovery/protocol.py` | 11509 | `e12de998036f40cac1f0d5dbfb5a293785bbf6ce6239f3cc11784c894fd7f3cf` |
| `latest/source/recovery/replay.py` | 8239 | `36e8be2946aadd71666c697b794d76f3c58b696bedc27a4408e32063bbb55840` |
| `latest/source/recovery/report.py` | 45315 | `6c37e92c9c338f7901fb0bda7fe6d2ea79fa998af3b33356e4b33c69d4df9fd3` |
| `latest/source/recovery/rounds.py` | 22540 | `2c59648c4cc8d720d1c510f27e663165ab2654d9044c57e222323664a2f631bf` |
| `latest/source/recovery/runner.py` | 16985 | `8723cf0c11b7988900275118d0565645f0585647274269a3e343206664d43b8a` |
| `latest/source/recovery/schedule.py` | 14584 | `396d8322e28ef1031803322f94f501be7fd778f69c0489854f78c228e87354d6` |
| `latest/source/recovery/state.py` | 21869 | `acf99320366e55c18778b4a4836003dfeb820abd77bc314172c3d538d35d4276` |
| `latest/source/recovery/storage.py` | 39649 | `e688428c2f07dcba28d928dcfbc163920ac6eeec37d15801d623dca35810a0d3` |
| `latest/source/recovery/t4_attention.py` | 5832 | `b5f7e9b8e7a7f4fe0193c31628d907f1476812983e3178beb20c297b7d172ee8` |
| `latest/source/recovery/tasks.py` | 10706 | `59d80c0e47c005af082626253ec86b6f3fc56be0dc57bad0369d1a263ba7e9a4` |
| `latest/source/recovery/truth.py` | 4362 | `bfc51e6da767258fc3e27a516b7fd44b48bb58f61f8fde73ccbb7ff51e9c8b2c` |
| `latest/source/recovery/uncertainty.py` | 41804 | `8cfbb1a89110a07536b8937b9248851ed0fbcea963d6950cd290a550e8036dad` |
| `latest/source/recovery/witness.py` | 3393 | `15e25c69e44da2ac2eccae2032c7ecce4bd33a033d91e4acc76ec1f79d0e523b` |
| `latest/source/recovery/workers.py` | 37624 | `300c06a6b30de089ef71e7c8dcf74a433d99b62e206a234e208aeefe9eb832a9` |
| `latest/source/scripts/build_i01_course_notebook.py` | 25074 | `cba61842b2287e12da7c50ae117811df22ec2a9480415159d2e4dfe7ac2d20b7` |
| `latest/source/scripts/build_i01_course_release.py` | 8420 | `a132c504a3714c121e503a20fe6fa8dfe90c5c8ae6ac98037604f29702b5b105` |
| `latest/source/scripts/i01_course.py` | 241 | `36e6ecc1771fdca40c4bbb5e3b48aeef2eefb78cedad756651c1265751d1269b` |
| `latest/source/scripts/verify_i01_course_release.py` | 15675 | `3032d814420233e3562a1a0fa178798b1c2556260b31b763d916a0b212679761` |
| `latest/source/source-release.json` | 105248 | `e32ee983342d499dbaf52e37d3eac2503be69ce2e132549930ff7b253c2bfbd3` |
| `latest/source/tests/__init__.py` | 46 | `3de16dabcc772a42ec4dd3ca6939c798639e6d9ceee859b4c24856f0828057ee` |
| `latest/source/tests/test_i01_assisted_accounting.py` | 4694 | `21b736051420e8e5622b310c307f9a9df435f13039a1b9fe00adf75a50f8898c` |
| `latest/source/tests/test_i01_assisted_core.py` | 10491 | `627e317248f6de933abb95cc1bc2e593474963fbf9f587b46a61a0d150eca730` |
| `latest/source/tests/test_i01_assisted_delivery.py` | 4452 | `4407d15673a25add5d28486221379638b38ae57ca544a24510279f05fa86002d` |
| `latest/source/tests/test_i01_assisted_report.py` | 8981 | `32d0f7b4a53bb8c1c475e55f56cf20ee2d34427ff3c9e7f167da3f275a28b17c` |
| `latest/source/tests/test_i01_assisted_workflow.py` | 13725 | `55261c6c1cbc710d092145c116b5f3d663bbf35c0b0d0d93cf988a6a921fdfb7` |
| `latest/source/tests/test_i01_client_startup.py` | 3570 | `7c2a74ac80733c0b1ced294cfb3a6dd945ea4628adde592ea62be81c26929fb0` |
| `latest/source/tests/test_i01_course3_repairs.py` | 23487 | `0bc01a46beeaba592a0966e90de36c8846ff0be9b2f3cdf5e22fc2997c2167dc` |
| `latest/source/tests/test_i01_fresh_run.py` | 6865 | `ce8edc942e3dac3b5672c81e25e5338e83edf9505c73bcf9f5046aaec7bfd2c3` |
| `latest/source/tests/test_i01_integration.py` | 9345 | `4ba4d28b5905bedd6a3d1fb80a877a1d87b6f3160d64108bbb16d66192359619` |
| `latest/source/tests/test_i01_notebook_ui.py` | 8548 | `cf4529f376d18d75f2b0282269931219cdd75a1e984304f0f3c5d280f6cf4829` |
| `latest/source/tests/test_i01_outcome_admission.py` | 9879 | `d3d9bdb6f2dc6adcbf85a4042d7aba7f9653708f27c5c22b2d9ad84e4355ea9e` |
| `latest/source/tests/test_i01_recovery_admission.py` | 10605 | `36528d75195d97bd5ad749818c5b5c649cf2ef08e89cf99373e40b5c11f4db78` |
| `latest/source/tests/test_i01_repairs.py` | 10367 | `bec30749ab173fa4860bd389062d1820f322e50da095ae647ab7e782519f7180` |
| `latest/source/tests/test_i01_run_all.py` | 8701 | `87e318af3bffd181c12021053ca5d76053edfc9d378878ab2bf21a6f352c4846` |
| `latest/source/tests/test_i01_runtime.py` | 5742 | `080a684294c9f0125e69b899a6da437272bdec181bc49325752c68e1f0538219` |
| `latest/source/tests/test_i01_setup.py` | 3941 | `c7f43c44f0d4ba4cc7f240ce42e4fe2841d62887b76721718fd421d58ca52af6` |
| `latest/worker-0.sqlite` | 6246400 | `17b29a7882dc708c2dd3f7e89f6a4d382671d779d6629e165fb51ab5823f58e8` |
| `latest/worker-1.sqlite` | 5275648 | `48b8d2537ddb87933cfbe95b17850d88482accc1bf4e5a63da56d583c8cf0965` |
| `multi-agents-assisted-v1nb.ipynb` | 6380774 | `09cd97482d41eeccbbd28fa7ac3449510cb68c5ac26a936bdfa3abbc58df6b45` |

## 9. Repository preservation and delivery checks

Only the new Markdown files under `docs/analysis/assisted-v1/` are task-owned outputs. The audit established a pre-edit SHA-256/size baseline for 2,510 existing tracked repository and run-folder files. The final delivery check compares that baseline with current bytes and checks Git status for any changes outside the new documentation directory. The result is recorded in the reading index after final verification. No commit, implementation edit, scientific setting change, inference, GPU operation, publication or historical artifact deletion is performed.

## 10. Supplementary read-only document and historical checks

The following optional block checks the delivered all-response ledger, every main table row, relative links/trace anchors, TXT/HTML encoded raw-response coverage, and the Course-7 interval. It executes the first Python block in memory and writes nothing. It was run successfully after document generation. The main audit's 10,953 assertions remain the named audit checkpoint; these supplementary assertions are separate delivery checks.

```python

from pathlib import Path
import re,json,subprocess,hashlib
root=Path('.')
D=Path('docs/analysis/assisted-v1')
p=D/'forensic-reproducibility.md';fence=chr(96)*3
code=p.read_text(encoding='utf-8').split(fence+'python\n',1)[1].split('\n'+fence,1)[0]
exec(compile(code.split("\nout({'assertions':")[0],str(p),'exec'))
assert not anomalies,anomalies
ledger=(D/'exhaustive-trace-ledger.md').read_text(encoding='utf-8')
tick=chr(96)
headings=re.findall(r'^#### '+tick+'([^'+tick+']+)'+tick+'$',ledger,re.M)
assert len(headings)==len(calls)==len(set(headings))==356
assert set(headings)==set(bycall)
for c in calls:
 section=ledger.split('#### '+tick+c['id']+tick+'\n',1)[1].split('\n#### ',1)[0]
 assert c['outcome']['raw_text'] in section,c['id']
assert len(re.findall(r'^## (?:main|pilot|qualification)-\d\d$',ledger,re.M))==28
science=(D/'scientific-analysis.md').read_text(encoding='utf-8')
table_section=science.split('### 4.1 Exact twenty-world table',1)[1].split('### 4.2',1)[0]
table=[l for l in table_section.splitlines() if re.match(r'^\| \d\d \|',l)]
assert len(table)==20,len(table)
for i,line in enumerate(table):
 w=worlds[f'main-{i:02d}']
 for ph in ['prefix','retain','clear']:
  assert json.dumps(eps[w['id']+'/'+ph]['submissions'],separators=(',',':')) in line
 assert str(eps[w['id']+'/control-revised-direct']['submissions'][0]) in line
all_links=0
for p in D.glob('*.md'):
 text=p.read_text(encoding='utf-8')
 text=re.sub(r'^'+fence+r'[^\n]*\n.*?^'+fence+r'\s*$', '', text, flags=re.M|re.S)
 for target in re.findall(r'\[[^\]\n]+\]\(([^)]+)\)',text):
  all_links+=1
  if not target.startswith(('https://','http://','#')):
   assert (p.parent/target.split('#')[0]).resolve().exists(),(p.name,target)
sourcehtml=(L/'reports/conversations.html').read_text(encoding='utf-8')
anchors=set(re.findall(r'id=["\']([^"\']+)',sourcehtml))
assert all(cid in anchors for cid in headings)
import html
for name in ['conversations.txt','conversations.html']:
 text=(L/'reports'/name).read_text(encoding='utf-8')
 if name.endswith('html'):text=html.unescape(text)
 assert all(json.dumps(c['outcome']['raw_text'],ensure_ascii=False) in text for c in calls),name
out({'audit_assertions':sum(checks.values()),'anomalies':anomalies,'raw_response_sections':len(headings),'world_sections':28,'main_table_rows':len(table),'links_checked':all_links,'trace_anchors_checked':len(headings),'success_interval':boot('success'),'effort_interval':boot('ready')})

# Reproduce the historical interval without changing its seed or scoring.
historical_strata={}
for w in c7run['worlds']:
 if w['group']!='main':continue
 rv=int(c7eps[w['id']+'/retain']['submissions']==[w['revised_truth']]*2)
 cv=int(c7eps[w['id']+'/clear']['submissions']==[w['revised_truth']]*2)
 historical_strata.setdefault((w['owner'],w['first']),[]).append(cv-rv)
historical_rng=random.Random(c7run['config']['bootstrap_seed'])
historical_draws=sorted(sum(historical_rng.choice(v) for v in historical_strata.values() for _ in v)/20 for _ in range(10000))
assert [historical_draws[250],historical_draws[9750]]==[-.1,.1]
out({'course7_outcome_interval':[historical_draws[250],historical_draws[9750]],'historical_bootstrap_seed':c7run['config']['bootstrap_seed']})

```



