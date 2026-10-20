"""Independently reconstruct stored requests, legal actions, histories and outcomes.

Input paths follow this course repository. Scientific checks use the original
frozen instructions and records, with no model or tokenizer imports.
"""
from pathlib import Path
import json,sqlite3,collections,hashlib,zipfile,csv,io,math,statistics,random,re
import sys
ROOT=Path(__file__).resolve().parents[2]
L=Path(sys.argv[1]); C7=Path(sys.argv[2]); S=L/'source'
R=ROOT/'experiments/assisted-experiment'
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
with zipfile.ZipFile(R/'kaggle-results.zip') as z:
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
for record in json.loads((ROOT/'scripts/analysis/support/historical-inputs.json').read_text(encoding='utf-8')):
 for w in record['worlds']:
  for ph in ['original','revised']:exposed.add(canonical(w[ph]))
 source_inputs.append((record['source'],len(record['worlds'])))
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
# C7 is the separately extracted preliminary checkpoint supplied by the wrapper.
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
