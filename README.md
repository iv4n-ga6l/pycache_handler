# pycache-handler

[![PyPI Downloads](https://img.shields.io/pypi/dm/pycache-handler.svg?label=PyPI%20downloads)](
https://pypi.org/project/pycache-handler/)


It aims to continuously scan a project and then delete any `__pycache__` directory generated by the project. This is to ensure the project will be clean and avoid to delete `__pycache__` manually.


## Installation

To install it :

```sh
pip install pycache-handler
```


## Usage

```python
from pycache_handler.handler import py_cache_handler

@py_cache_handler
def main():
    # Your main application code here
    pass

# Or specify a custom directory to monitor
@py_cache_handler(project_dir=r"path/to/your/project")
def main():
    # Your main application code here
    pass

if __name__ == "__main__":
    main()
```


## Requirements
- watchdog

## License
This project is licensed under the MIT [License](LICENSE.md)

