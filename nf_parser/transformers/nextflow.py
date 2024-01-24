from pathlib import Path
from lark import Lark, Transformer, v_args, Discard, Tree, Token
import re
from .. import utils

#__dir__ = Path(__file__).parent

class Nextflow(Transformer):
	INT = int
	NUMBER = float

	def __init__(self):
		self.param_list = {}
		self.module_list = []
		self.workflows = {}
		self.processes = {}
		self._configs = {}

	@v_args(inline=True)
	def import_entry(self, name, path):
		return {"type": "import", "module": name, "path": path.value}
	
	@v_args(inline=True)
	def module_entry(self, *args):
		path = args[-1]
		items = args[0:-1]
		imports = [m.value for m in items]
		module_def = {
			'module': "include {" + f"{','.join(imports)}"  + "} from './module/1.nf'",
			'imports': imports,
			'path': path
		}
		self.module_list.append(module_def)
		return {'type': 'module', 'modules': imports, 'path': path}
	
	@v_args(inline=True)
	def parameter_entry(self, key, value=None, comment=None, *args):
		print(key, value)
		if not key:
			return None
		default_val = value
		#print(default_val)
		val_type = utils.value_type(default_val)
		self.param_list[key.value] = {
			'name':  key.value, 
			'type':  val_type, 
			'default_value':  default_val,
			'description':  comment,
		}
		return {'type': 'param',  "value": (key, value, comment) }

	@v_args(inline=True)
	def workflow_block(self, name, body=None):
		if not body:
			body = name
			name = 'main'
		print('workflow_block.body', body)
		wf_body = {}
		for c in body.children:
			print(c, type(c))
			if not c:
				continue
			if isinstance(c, Token):
				print(c, c.type)
				#continue
				if c.type == 'COMMENT':
					continue
			#print(c.pretty())
			wf_body[c.data] = c.children
		
		self.workflows[name] = wf_body
		return {'type': 'workfow',  "value": (name, body) }
	
	""" @v_args(tree=True)
	def workflow_body(self, tree):
		print('workflow_body =>', tree)
		return tree """
	
	#@v_args(inline=True)
	""" def instruction(self, val):
		print('instruction =>', val)
		return val """
	
	@v_args(inline=True)
	def function_call(self, name, *args):
		print('function_call =>', name, args)
		return {name : {'args': list(args)}}
	
	@v_args(inline=True)
	def func_dot_call(self, name, *args):
		print('func_dot_call.before =>', name, args)
		if len(args) == 0:
			first_key, first_value = next(iter(name.items()))
			name = first_key.value
			args = first_value
		else:
			first_key, first_value = next(iter(args[0].items()))
			name = f'{name}.{first_key.value}'
			args = first_value
		print('func_dot_call.after =>', name, args)
		return {name : {'args': list(args)}}
	
	@v_args(inline=True)
	def pipe_func_call(self, name):
		print('pipe_func_call =>', name)
		args = [] # todo: args come from previous token
		return {
			name : {
				'args': args, 
				"pipe": True
			}
		}
	
	@v_args(inline=True)
	def func_arg(self, *val):
		return '.'.join(val)
	
	@v_args(inline=True)
	def emit_arg(self, *val):
		return '.'.join(val)
	
	@v_args(inline=True)
	def emit_named_arg(self, name, val):
		return {name: val}

	@v_args(inline=True)
	def process_block(self, name, body):
		print(name)
		p_def = {}
		for c in body.children:
			print(c)
			if not c:
				continue
			#print(c.pretty())
			#if c[0] not in ['script', 'shell', 'input', 'output']:
			p_def[c[0]] = c[1]
		self.processes[name] = p_def
		return {'type': 'process',  "value": (name, body) }

	@v_args(inline=True)
	def directive(self, d_type, expr, *args):
		if not d_type:
			return None
		return (d_type.value, expr)

	@v_args(inline=True)
	def script(self, c=None, body=None, *args):
		if not body:
			body = c
		print('script', body, args)
		return ('script', body)
	
	@v_args(inline=True)
	def shell(self, body):
		return ('shell', body)

	@v_args(inline=True)
	def input(self, *input_defs):
		_inputs = list(filter(lambda v: v is not None, input_defs))
		return ('input', list(_inputs))
	
	@v_args(inline=True)
	def output(self, *output_defs):
		_outputs = list(filter(lambda v: v is not None, output_defs))
		return ('output', list(_outputs))
	
	@v_args(inline=True)
	def expression(self, val, *options):
		dt = {'value': val}
		if len(options) != 0:
			dt['options'] = list(options)
		return dt

	@v_args(inline=True)
	def option(self, name, val):
		return {name: val}

	@v_args(inline=True)
	def input_def(self, name, val={}):
		return {name: val}

	""" @v_args(inline=True)
	def output_def(self, *args):
		print('output_def=>', args)
		name = args[0]
		val = args[1] if len(args) > 2 else {}
		return {name: val} """

	@v_args(inline=True)
	def output_def(self, name, val={}):
		return {name: val}

	@v_args(inline=True)
	def tuple_def(self, *args):
		print('tuple_def=>', args)
		return args

	@v_args(inline=True)
	def script_body(ws, val):
		#print('script_body=>', val)
		return val

	@v_args(inline=True)
	def conditional_script(self, *expr):
		print('conditional_script=>', expr)
		return list(expr)

	@v_args(inline=True)
	def if_script(self, expr, script):
		print('if_script=>', expr, script)
		return {'if': (expr, script)}
	
	@v_args(inline=True)
	def else_if_script(self, expr, script):
		return {'elif': (expr, script)}
	
	@v_args(inline=True)
	def else_script(self, script):
		return {'else': script}
	
	@v_args(inline=True)
	def comparison_expression(self, *args):
		return list(args)

	@v_args(inline=True)
	def SCRIPT(self, val):
		#print('SCRIPT', val)
		return val.strip('"').strip("'").strip()

	@v_args(inline=True)
	def QUALIFIER(self, val):
		return val.strip()

	@v_args(inline=True)
	def STRING(self, val):
		return val.strip('"').strip("'").strip()
	
	@v_args(inline=True)
	def FILE_PATH(self, val):
		return val.strip('"').strip("'").strip()
	
	@v_args(inline=True)
	def CNAME(self, val):
		return val
	
	@v_args(inline=True)
	def VALUE(self, val):
		return val.strip('"').strip("'").strip()
	
	@v_args(inline=True)
	def PARAM_COMMENT(self, comment_str):
		return comment_str.strip('//').strip()
	
	@v_args(inline=True)
	def COMMENT(self, comment_str):
		return None
	
	@v_args(inline=True)
	def comment(self, *args):
		return None
	
	def start(self, tree):
		self.meta_params = {
			"modules": self.module_list,
			"params": self.param_list,
			"workflows": self.workflows,
			"processes": self.processes,
		}
		return self.meta_params

	
	def config(self, tree):
		# todo
		return tree
	
	#@v_args(inline=True)
	#def unknown_entry(self, children):
	#	return Discard


