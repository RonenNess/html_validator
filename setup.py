from distutils.core import setup
setup(
  name = 'html_validator',
  packages = ['html_validator'],
  package_data = {'html_validator' : ["*.py", "vnu.jar", "README.md"], },
  version = '1.0.1',
  description = 'A simple offline HTML validator using the standard v.Nu validator.',
  author = 'Ronen Ness',
  author_email = 'ronenness@gmail.com',
  url = 'https://github.com/RonenNess/html_validator',
  download_url = 'https://github.com/RonenNess/html_validator/tarball/1.0.1',
  keywords = ['html validator', 'html', 'validator', 'checker', 'html5', 'w3', 'vnu'],
  classifiers = [],
)