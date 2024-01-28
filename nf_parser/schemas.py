## constructs
from pydantic import validator, BaseModel, Field
from typing import List, Optional, Any, Union, Dict

class Comment(BaseModel):
	text: str = Field(..., description="the comment textual value")

class Module(BaseModel):
	""" a nextflow [module](https://www.nextflow.io/docs/latest/module.html) """
	path: str = Field(..., description="the module path")
	imports: List[str] = Field(..., description="the module imports")

class Param(BaseModel):
	""" nextflow pipeline param """
	name: str = Field(..., description="the param name")
	type: str = Field('string', description="the param type")
	default_value: Optional[Union[str, int]] = Field(None, description="the param default value")
	comment: Optional[Comment] = Field(None, description="the param comment can be likened to its description")

class Expression(BaseModel):
	""" a call """
	code: str = Field(..., description="the expr code")

class Channel(Expression):
	pass

class Arg(BaseModel):
	""" groovy function args """
	name: str = Field(..., description="the arg")
	#type: str = Field('string', description="the param type")

class Function(BaseModel):
	name: str = Field(..., description="the func name")
	args: Optional[List[Arg]] = Field(None, description="the func args")
	code: str = Field(None, description="the func code block")

class Script(BaseModel):
	type: str = Field("bash", description="the script type")
	code: str = Field(..., description="the script source code text")
	template: Optional[str] = Field(None, description="path to shell script if template was provided. see [nextflow script template docs](https://www.nextflow.io/docs/latest/process.html#template)")
	condition: Optional[str] = Field(None, description="script conditional control flow expression type. see [nextflow conditional-scripts docs](https://www.nextflow.io/docs/latest/process.html#conditional-scripts)")

class Directive(BaseModel):
	name: str = Field(..., description="the directive name")
	value: str = Field(..., description="the directive value")
	options: Dict[str, Any] = Field(None, description="the directive options")

class Input(BaseModel):
	name: str = Field(..., description="the type")
	value: Union[str, List[str]] = Field(..., description="the value")
	comment: Optional[Comment] = None

class Output(Input):
	pass

class Process(BaseModel):
	name: str = Field(..., description="the process name")
	inputs: List[Input] = []
	outputs: List[Output] = []
	comments: List[Comment] = None
	scripts: List[Script] = None
	directives: List[Directive] = None

class Workflow(BaseModel):
	name: str = Field('main', description="the workflow name")
	inputs: Optional[List[Input]] = Field(None, description="the workflow inputs aka `take`")
	outputs: Optional[List[Output]] = Field(None, description="the workflow outputs aka `emit`")
	expressions: List[Union[Expression, Channel]] = Field(None, description="the workflow expressions")
	#channels: Any = Field(None, description="the workflow channel expressions ie. data flow statements")
	comments: List[Comment] = None
	
class Pipeline(BaseModel):
	""" a nextflow pipeline  """
	modules: Optional[List[Module]] = Field(None, description="the nextflow [modules](https://www.nextflow.io/docs/latest/module.html)")
	params: Optional[List[Param]] = Field(None, description="the nextflow [params](https://www.nextflow.io/docs/latest/basic.html#processes-and-channels)")
	processes: Optional[List[Process]] = Field(None, description="the nextflow [processes](https://www.nextflow.io/docs/latest/process.html)")
	workflows: Optional[List[Workflow]] = Field(None, description="the nextflow [workflows](https://www.nextflow.io/docs/latest/workflow.html)")
	functions: Optional[List[Function]] = Field(None, description="pipeline defined functions")
	comments: Optional[List[Comment]] = Field(None, description="pipeline level comments")
