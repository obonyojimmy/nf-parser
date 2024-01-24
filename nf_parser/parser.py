from lark import Lark, Transformer, v_args, Discard, Tree, Token
import re
from pathlib import Path
from .utils import get_grammer
from .transformers.nextflow import Nextflow

""" 
	Links:
		- https://github.com/lark-parser/lark/blob/master/docs/json_tutorial.md
"""

class Parser:
	def __init__(self):
		self.comments = []
		file = get_grammer()
		#file = f'./nf.lark'
		#print(file)
		self.lang = Path(file).read_text()
		self.transformer = Nextflow()
		self._PARSER = Lark(
			self.lang, 
			parser='lalr', 
			transformer=self.transformer, 
			#lexer_callbacks={'COMMENT': self.comments.append}
		)
		self._CONFIG_PARSER = Lark(
			self.lang, 
			parser='lalr',
			start="config",
			#transformer=self.transformer, 
			#lexer_callbacks={'COMMENT': self.comments.append}
		)
		

	def parse_config(self, file=None, text=None):
		if file:
			text = Path(file).read_text() 
		tree =  self._CONFIG_PARSER.parse(text)
		return tree

	def parse(self, file=None, text=None, ignore_error: bool = False):
		if file:
			text = Path(file).read_text() 
		def on_error(e):
			print(e)
			return True
		kwargs = {}
		if ignore_error:
			kwargs['on_error'] = on_error
		tree =  self._PARSER.parse(text, **kwargs)
		return tree
