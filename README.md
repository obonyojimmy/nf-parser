# nf_parser

parse nextflow syntax to structured json/yaml and pythonic objects

## Installation

```bash
$ pip install nf_parser
```


## Dependecies

- python >=3.9

## Usage

```
from nf_parser import Parser

nf_file = './tests/nf/test3.nf'
schema = Parser().parse(path=nf_file)
print(schema)
```

## Testing

`pytest`

## Development

```bash
poetry install
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## Credits

