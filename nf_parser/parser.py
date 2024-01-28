from lark import Lark, Transformer, v_args, Discard, Tree, Token
import re
from pathlib import Path
from .utils import get_grammer
from .nextflow import NextflowTransformer

""" 
	Links:
		- https://github.com/lark-parser/lark/blob/master/docs/json_tutorial.md
"""

class NextflowParser:
	def __init__(self):
		self.comments = []
		self.grammar = get_grammer()
		self.transformer = NextflowTransformer()
		self.parser = Lark(
			self.grammar, 
			parser='lalr', 
			transformer=self.transformer, 
			#lexer_callbacks={'COMMENT': self.comments.append}
		)
	
	@staticmethod
	def on_error(e):
		print(e)
		return True

	def parse_config(self, file=None, text=None):
		if file:
			text = Path(file).read_text()
		parser = Lark(
			self.grammar, 
			parser='lalr', 
			transformer=self.transformer, 
			#lexer_callbacks={'COMMENT': self.comments.append}
		)
		data =  parser.parse(text)
		return data

	def parse(self, file=None, text=None, ignore_error: bool = False):
		if file:
			text = Path(file).read_text()
		kwargs = {}
		if ignore_error:
			kwargs['on_error'] = self.on_error
		tree =  self.parser.parse(text, **kwargs)
		return tree
