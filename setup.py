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
readme = open('README.rst', encoding="utf8").read()
history = open('CHANGELOG.rst', encoding="utf8").read().replace('.. :changelog:', '')


setup(name='django-ajax-datatable',
      version=version,
      description='Helper class to integrate Django with datatables',
      long_description=readme + '\n\n' + history,
      long_description_content_type='text/x-rst',
      url='http://github.com/morlandi/django-ajax-datatable',
      author='Mario Orlandi',
      author_email='morlandi@brainstorm.it',
      license='MIT',
      include_package_data=True,
      packages=find_packages(),
      zip_safe=False,
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Framework :: Django',
          'Framework :: Django :: 2.2',
          'Framework :: Django :: 3.0',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Natural Language :: English',
          'Programming Language :: Python :: 3.7',
      ],
      )
