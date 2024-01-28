from lark import Transformer, v_args, Discard
from typing import List
from .schemas import *
from .utils import flatten_list

@v_args(inline=True)
class NextflowTransformer(Transformer):
	proceses: List[Process] = []
	#def __default__(self, data, c, h):
	#	return Discard
	CNAME = lambda _, v: str(v)
	STRING = lambda _, v: str(v)
	float = lambda _, v: float(v)
	int = lambda _, v: int(v)
	string = lambda _, v: str(v)
	variable = lambda _, v: str(v)
	map = lambda _, k, v: {k: v}

	def __init__(self):
		super().__init__()
	
	@v_args(inline=False)
	def start(self, items) -> Pipeline:
		comments, modules,  processes, workflows, params, functions = None, None, None, None, None, None
		for item in items:
			if type(item) == Comment:
				if not comments:
					comments = []
				comments.append(item)
			elif type(item) == Module:
				if not modules:
					modules = []
				modules.append(item)
			elif type(item) == Param:
				if not params:
					params = []
				params.append(item)
			elif type(item) == Process:
				if not processes:
					processes = []
				processes.append(item)
			elif type(item) == Workflow:
				if not workflows:
					workflows = []
				workflows.append(item)
			elif type(item) == Function:
				if not functions:
					functions = []
				functions.append(item)
		pipeline = Pipeline(
			modules=modules, 
			params=params, 
			processes=processes, 
			functions=functions,
			workflows=workflows
		)
		return pipeline
		
	
	def dsl(self, item):
		pass

	def comment(self, item):
		return Comment(text=str(item))

	@v_args(inline=False)
	def module_import(self, items):
		print("module_import:", items)
		mod_path = items[-1]
		mods = items[:-1]
		return Module(path=mod_path, imports=mods)

	def param(self, name, default_val=None, comment=None):
		# todo: detect the param value type from use or default_value
		_type = 'string'
		return Param(name=name, type=_type, default_value=default_val, comment=comment)

	@v_args(inline=False)
	def function(self, items:list):
		print("function:", items)
		name, code = items.pop(0) , items.pop(-1)
		args = []
		if items:
			args = items[0]
		#print("args:", args)
		return Function(name=name, code=code, args=args)

	@v_args(inline=False)
	def workflow(self, name, items=None):
		print('workflow:', name, items)
		if not items:
			items = name
			name = 'main'
		comments, expressions, channels = [], [], []
		for item in flatten_list(items):
			if type(item) == Comment:
				comments.append(item)
			elif type(item) == Expression:
				expressions.append(item)
			elif isinstance(item, Expression):
				expressions.append(item)
		print('workflow:', name, expressions, comments)
		return Workflow(
			name=name, 
			expressions=expressions, 
			#channels=channels, 
			comments=comments or None
		)

	def process(self, name, items) -> Process:
		print('process:',items)
		return Process(name=name, **items)

	@v_args(inline=False)
	def workflow_block(self, items):
		items = flatten_list(items)
		print('workflow_block:', items)
		return items

	def workflow_input(self, item):
		return Input(name="take", value=item)

	@v_args(inline=False)
	def main(self, items):
		items = flatten_list(items)
		print('workflow.main:',items)
		return items

	def emit(self, items):
		return items

	def wf_output(self, item):
		return Output(name="emit", value=str(item))

	def channel(self, item):
		return Channel(code=str(item))

	def expression(self, item):
		print('workflow.expression:', item)
		return Expression(code=str(item))

	@v_args(inline=False)
	def process_block(self, items):
		inputs, outputs, comments, scripts, directives = [], [], [], [], []
		items = flatten_list(items)
		print("process_block:", items)
		for item in items:
			if isinstance(item, Comment):
				comments.append(item)
			elif type(item) == Input:
				inputs.append(item)
			elif type(item) == Output:
				outputs.append(item)
			elif type(item) == Script:
				scripts.append(item)
			elif type(item) == Directive:
				directives.append(item)
			
		return {
			"inputs": inputs,
			"outputs": outputs,
			"comments": comments, 
			"scripts": scripts,
			"directives": directives,
		}
		#return f'Process Block: {items}'

	@v_args(inline=False)
	def input(self, items):
		items = flatten_list(items)
		#print('input:', items)
		out = []
		for x in items:
			if isinstance(x, dict):
				x = Input(**x)
			out.append(x)
		#print('input-transformed:', items)
		return out

	@v_args(inline=False)
	def output(self, items):
		items = flatten_list(items)
		#print('output:', items)
		out = []
		for x in items:
			if isinstance(x, dict):
				x = Output(**x)
			out.append(x)
		#print('output-transformed:', items)
		return out
	
	@v_args(inline=False)
	def script(self, items):
		#items = flatten_list(items)
		print('script:', items)
		return items

	def shell(self, items):
		return items

	def exec(self, val):
		## todo: improve grammer parsing, might break
		return Script(type="exec", code=str(val))

	def directive(self, item):
		print('directive:', item)
		return item

	def bash_script(self, val):
		## todo: check the shebang of script if provided to annotate correct script type
		return Script(type="bash", code=str(val))

	def shell_script(self, val):
		return Script(type="shell", code=str(val))

	def template(self, val):
		# todo: get the script template source from the template path
		return Script(type="shell", code=str(val), template=str(val))

	def if_script(self, val):
		## todo: separate condition from expression
		return Script(type="bash", code=str(val), condition="if")

	def elif_script(self, val):
		## todo: separate condition from expression
		return Script(type="bash", code=str(val), condition="elif")

	def else_script(self, val):
		## todo: separate condition from expression
		return Script(type="bash", code=str(val), condition="else")

	@v_args(inline=False)
	def conditional_script(self, items):
		print('conditional_script:', items)
		return items

	def val(self, value):
		return {"name":"val", "value":value}

	def file(self, value):
		print('file:', value)
		return {"name":"file", "value":value}
	
	def path(self, value):
		return {"name":"path", "value":value}
	
	def env(self, value):
		return {"name":"env", "value":value}
	
	def stdin(self, value):
		return {"name":"stdin", "value":value}

	def tuple(self, value):
		return {"name":"tuple", "value":value}
	
	def each(self, value):
		return {"name":"each", "value":value}

	def accelerator(self, val, options=None):
		print(f'queue:', val, options)
		return Directive(name="accelerator", value=str(val), options=options)
	
	def before_script(self, val, options=None):
		print(f'before_script:', val, options)
		return Directive(name="before_script", value=str(val), options=options)
	
	def after_script(self, val, options=None):
		print(f'after_script:', val, options)
		return Directive(name="after_script", value=str(val), options=options)
	
	def cluster_options(self, val, options=None):
		print(f'cluster_options:', val, options)
		return Directive(name="cluster_options", value=str(val), options=options)
	
	def conda(self, val, options=None):
		print(f'conda:', val, options)
		return Directive(name="conda", value=str(val), options=options)
	
	def cache(self, val, options=None):
		print(f'cache:', val, options)
		return Directive(name="cache", value=str(val), options=options)
	
	def cpus(self, val, options=None):
		print(f'cpus:', val, options)
		return Directive(name="cpus", value=str(val), options=options)
	
	def container(self, val, options=None):
		print(f'container:', val, options)
		return Directive(name="container", value=str(val), options=options)
	
	def container_options(self, val, options=None):
		print(f'container_options:', val, options)
		return Directive(name="container_options", value=str(val), options=options)
	
	def debug(self, val, options=None):
		print(f'debug:', val, options)
		return Directive(name="debug", value=str(val), options=options)
	
	def disk(self, val, options=None):
		print(f'disk:', val, options)
		return Directive(name="disk", value=str(val), options=options)
	
	def echo(self, val, options=None):
		print(f'echo:', val, options)
		return Directive(name="echo", value=str(val), options=options)
	
	def error_strategy(self, val, options=None):
		print(f'error_strategy:', val, options)
		return Directive(name="error_strategy", value=str(val), options=options)
	
	def executor(self, val, options=None):
		print(f'executor:', val, options)
		return Directive(name="executor", value=str(val), options=options)
	
	def ext(self, val, options=None):
		print(f'ext:', val, options)
		return Directive(name="ext", value=str(val), options=options)
	
	def fair(self, val, options=None):
		print(f'fair:', val, options)
		return Directive(name="fair", value=str(val), options=options)
	
	def label(self, val, options=None):
		print(f'label:', val, options)
		return Directive(name="label", value=str(val), options=options)
	
	def machine_type(self, val, options=None):
		print(f'machine_type:', val, options)
		return Directive(name="machine_type", value=str(val), options=options)
	
	def max_errors(self, val, options=None):
		print(f'max_errors:', val, options)
		return Directive(name="max_errors", value=str(val), options=options)
	
	def max_forks(self, val, options=None):
		print(f'max_forks:', val, options)
		return Directive(name="max_forks", value=str(val), options=options)
	
	def max_retries(self, val, options=None):
		print(f'max_retries:', val, options)
		return Directive(name="max_retries", value=str(val), options=options)
	
	def memory(self, val, options=None):
		print(f'memory:', val, options)
		return Directive(name="memory", value=str(val), options=options)
	
	def module(self, val, options=None):
		print(f'module:', val, options)
		return Directive(name="module", value=str(val), options=options)
	
	def penv(self, val, options=None):
		print(f'penv:', val, options)
		return Directive(name="penv", value=str(val), options=options)
	
	def pod(self, val, options=None):
		print(f'pod:', val, options)
		return Directive(name="pod", value=str(val), options=options)
	
	#@v_args(inline=False)
	def publish_dir(self, val, options=None):
		print(f'publish_dir:', val, options)
		return Directive(name="publish_dir", value=str(val), options=options)

	def queue(self, val, options=None):
		print(f'queue:', val, options)
		return Directive(name="queue", value=str(val), options=options)
	
	def resource_labels(self, val, options=None):
		print(f'resource_labels:', val, options)
		return Directive(name="resource_labels", value=str(val), options=options)
	
	def scratch(self, val, options=None):
		print(f'scratch:', val, options)
		return Directive(name="scratch", value=str(val), options=options)
	
	def spack(self, val, options=None):
		print(f'spack:', val, options)
		return Directive(name="spack", value=str(val), options=options)
	
	def store_dir(self, val, options=None):
		print(f'store_dir:', val, options)
		return Directive(name="store_dir", value=str(val), options=options)
	
	def stage_in_mode(self, val, options=None):
		print(f'stage_in_mode:', val, options)
		return Directive(name="stage_in_mode", value=str(val), options=options)
	
	def stage_out_mode(self, val, options=None):
		print(f'stage_out_mode:', val, options)
		return Directive(name="stage_out_mode", value=str(val), options=options)
	
	def tag(self, val, options=None):
		print(f'tag:', val, options)
		return Directive(name="tag", value=str(val), options=options)

	def time(self, val, options=None):
		print(f'time:', val, options)
		return Directive(name="time", value=str(val), options=options)

	@v_args(inline=False)
	def args(self, items):
		items = flatten_list(items)
		#print("args::", items)
		return items

	def arg(self, name):
		return Arg(name=name) 

	def identifier(self, val):
		return val

	def declaration(self, val):
		return val

	def value(self, val):
		return val

	def code_block(self, val):
		return str(val)

	def statement(self, val):
		return str(val)

	def operator(self, val):
		## todo
		return str(val)
