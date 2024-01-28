from pathlib import Path
from importlib import resources

def get_grammer() -> str:
	"""Get grammer

	Returns
	-------
	str: the grammer content
	"""
	with resources.path("nf_parser", "nf.lark") as f:
		grammer= Path(f).read_text()
	return grammer

def value_type(value):
	if value.isdigit():
		type = 'interger'
	elif '/' in value:
		type = 'file'
	elif '/' in value:
		type = 'file'
	else:
		type = 'string'
	return type
	""" try:
		path = pathlib.PurePath(value)
		return True
	except (TypeError, ValueError):
		return False """
	
## utils
def flatten_list(lst):
	result = []
	for item in lst:
		if isinstance(item, list):
			result.extend(flatten_list(item))
		else:
			result.append(item)
	return result

