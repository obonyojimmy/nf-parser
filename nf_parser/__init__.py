# read version from installed package
from importlib.metadata import version
__version__ = version("nf_parser")

from .parser import NextflowParser
