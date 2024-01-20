import pathlib
from importlib import resources

def get_grammer():
	"""Get path to example "Flatland" [1]_ text file.

	Returns
	-------
	pathlib.PosixPath
		Path to file.
	"""
	with resources.path("nf_parser", "nf.lark") as f:
		grammer_file_path = f
	return grammer_file_path

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

