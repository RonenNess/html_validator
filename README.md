# html_validator
An **offline** HTML validator in Python, using the standard [v.Nu Html Validator](https://github.com/validator/validator).

Source at [GitHub](https://github.com/RonenNess/html_validator).
Docs at [PythonHosted.org](http://pythonhosted.org/html_validator/).

## Install

Install html_validator via pip:

```python
pip install html_validator
```

In addition you'll need to have Java installed on your machine and Java path properly set (so you can execute jar files from shell / cmd prompt).

## Version
This library is only compatible with Python 2.

## How to use

```html_validator``` provide a single function, ```validate```, which receive an HTML file path or a list of HTML files and validate them:

```py
from html_validator import validate

errors = validate("test.html")
for err in errors:
    print("Type: %s, File: %s, Line: %d, Description: %s" % (err.type, err.file, err.line, err.description))
```

Example output:

```
Type: error, File: test.html, Line: 18, Description: Stray end tag "dv".
Type: error, File: test.html, Line: 15, Description: End tag for  "body" seen, but there were unclosed elements.
```

## How it works

There's not much magic here, this package just invokes a pre-compiled ```vnu.jar``` file from Python and parse its output (eg break it into nice Python objects).

## Run Tests

From ```html_validator``` root dir:

```shell
cd tests
python test_all.py
```

Note that the tests are not included in the pypi package, so to run them please clone the git repository from [GitHub](https://github.com/RonenNess/html_validator).


## Contact

For bugs please use [GitHub issues](https://github.com/RonenNess/html_validator/issues).
For other matters feel free to contact me at ronenness@gmail.com.

