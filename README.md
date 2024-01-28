# nf-parser

Parse and inspect Nextflow DSL scripts to extract information from Nextflow workflows, processes, channels, and more.

## Features

- **DSL Parsing:** Parse Nextflow DSL scripts to extract structured information.
- **Workflow Analysis:** Retrieve details about workflows, processes, channels, and other components.
- **Channel Operators:** Parse and understand Nextflow channel operators for further analysis.
- **DAG Generation:** Generate a Directed Acyclic Graph (DAG) of the workflow for visualization and analysis.
- **Syntax Validation:** Validate Nextflow syntax to catch errors early in the development process.

## Installation

```bash
pip install nf-parser
```

## Dependecies

- python >=3.9
- lark

## Usage
```
from nf_parser import NextflowParser

# Example usage
script = """
workflow example {
    input:
    path data

    script:
    """
    cat ${data} > output.txt
    """
}
"""

# Parse the script
parser = NextflowParser()
parsed_data = parser.parse(script)

# Access parsed information
workflow_name = parsed_data["workflows"][0]["name"]
print(f"Workflow Name: {workflow_name}")

# Generate a DAG
dag = NextflowDAG(parsed_data)
dag.generate_dag()
dag.visualize_dag("workflow_dag.png")

# Validate syntax
is_valid_syntax = parser.validate_syntax(script)
print(f"Is Syntax Valid: {is_valid_syntax}")
```

## Documentation

Detailed documentation, including available methods and data structures, can be found in the [documentation]().

## Testing

`pytest`


## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## Credits

