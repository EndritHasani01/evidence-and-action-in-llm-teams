import hashlib,json,sys,site
from pathlib import Path
from importlib.metadata import version
import recovery,recovery.inference,recovery.runner
from langgraph.checkpoint.sqlite import SqliteSaver
from transformers import Qwen3_5ForCausalLM
import torch
wanted={'torch': '2.11.0+cu128', 'pydantic': '2.13.5', 'langgraph': '1.2.12', 'langgraph-checkpoint': '4.2.0', 'langgraph-checkpoint-sqlite': '3.1.1', 'langchain-core': '1.6.6', 'transformers': '5.12.0', 'accelerate': '1.14.0', 'bitsandbytes': '0.49.2', 'tokenizers': '0.22.2', 'huggingface-hub': '1.19.0'}
actual={n:version(n) for n in wanted}
assert actual==wanted, {'expected':wanted,'actual':actual}
assert sys.prefix!=sys.base_prefix and site.ENABLE_USER_SITE is False
assert torch.__version__=='2.11.0+cu128' and torch.version.cuda=='12.8'
package=Path(recovery.__file__).resolve().parent
expected={'recovery/__init__.py': '63a4a14c67585083390ba36815bbf99c7929cfd8dd52548bcce20f85b7bcfdbd'}
observed={'recovery/'+p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in package.glob('*.py')}
assert observed==expected, 'source-to-installed module bytes differ'
assert package.is_relative_to(Path(sys.prefix).resolve()), 'base/source import contamination'
Path('C:\\Users\\EndritHasani\\Downloads\\recovery_blueprint\\recovery_blueprint\\notebooks\\validation\\m5-probe-output-repair\\controlled-case\\recovery-m5-continuation-d2f74d48a511\\installed-probe-result.json').write_text(json.dumps({'versions':actual,'executable':sys.executable,'prefix':sys.prefix,
'sys_path':sys.path,'module_root':str(package),'verified_module_hashes':observed,
'qwen_text_class':Qwen3_5ForCausalLM.__name__,'torch_cuda_build':torch.version.cuda,
'gpu_native_diagnostics':None,'model_generations':0}),encoding='utf-8')
