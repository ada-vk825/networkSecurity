from setuptools import find_packages, setup
from typing import List
'''find_packages() will automatically find all the packages and subpackages in the project directory.
This is useful because it saves you from having to manually list all the packages and subpackages in your setup.py file.
The find_packages() function will look for __init__.py files in the project directory and its subdirectories to identify packages.
This means that if you have a package called "my_package" with a subpackage called "my_subpackage", 
the find_packages() function will automatically include both "my_package" and "my_subpackage" in the
list of packages to be installed.

setup() is a function provided by the setuptools library that is used to define the metadata and configuration for a Python package.
It is typically used in a setup.py file to specify information about the package, such as its name, version, author, description, and dependencies.

typing.List is a type hint that indicates that the function expects a list of items as an argument.'''


def get_requirements() -> List[str]:
    '''This function reads a requirements.txt file and returns a list of requirements.'''
    try:
        with open('requirements.txt', 'r') as f:
            requirements = f.read().splitlines()
            if '-e .' in requirements:
                requirements.remove('-e .')
        return requirements
    except FileNotFoundError:
        return 'requirements.txt file not found. Please create a requirements.txt file with the necessary dependencies.'


setup(
    name='NetworkSecurity',
    version='0.1.0',
    packages=find_packages(),
    install_requires=get_requirements(),
    description='A project for network security analysis and visualization.',
    author='Varun Kokkiligadda',
    author_email='varun.kokkiligadda7702@gmail.com'
    )
