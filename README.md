# llm-fragments-dir

[![PyPI](https://img.shields.io/pypi/v/llm-fragments-dir.svg)](https://pypi.org/project/llm-fragments-dir/)
[![Changelog](https://img.shields.io/github/v/release/rkeelan/llm-fragments-dir?include_prereleases&label=changelog)](https://github.com/rkeelan/llm-fragments-dir/releases)
[![Tests](https://github.com/rkeelan/llm-fragments-dir/actions/workflows/test.yml/badge.svg)](https://github.com/rkeelan/llm-fragments-dir/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/rkeelan/llm-fragments-dir/blob/main/LICENSE)

Load files from a local directory as fragments. The current implementation will only attempt to load files that it thinks are UT8-encoded.

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-fragments-dir
```
## Usage

Use `-f dir:path/to/directory` to recursively include every text file from the specified directory as a fragment. For example:
```bash
llm -f dir:/home/user/src/repo "Suggest new features for this tool"
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-fragments-dir
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
llm install -e '.[test]'
```
To run the tests:
```bash
pytest .
```
