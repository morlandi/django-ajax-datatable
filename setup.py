import os
import re
from setuptools import find_packages, setup


def get_version(*file_paths):
    """Retrieves the version from specific file"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


version = get_version("ajax_datatable", "__init__.py")
readme = open('README.rst').read()
history = open('CHANGELOG.rst').read().replace('.. :changelog:', '')


setup(name='django-ajax-datatable',
      version=version,
      description='Helper class to integrate Django with datatables',
      long_description=readme + '\n\n' + history,
      url='http://github.com/morlandi/django-ajax-datatable',
      author='Mario Orlandi',
      author_email='morlandi@brainstorm.it',
      license='MIT',
      include_package_data=True,
      packages=find_packages(),
      zip_safe=False)
