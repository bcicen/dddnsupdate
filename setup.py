import os,os.path
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
        README = f.read()

requires = [
    'docker-py',
    'dnspython',
    ]

setup(name='dddnsupdate',
        version='0.1',
        description='small CLI utility to dynamically nsupdate a bind server \
                     with discovered docker containers',
        long_description=README,
        author='Bradley Cicenas',
        author_email='bradley.cicenas@gmail.com',
        keywords='docker, ddns, nsupdate',
        packages=find_packages(),
        include_package_data=True,
        install_requires=requires,
        entry_points = {
        'console_scripts' : ['dddnsupdate = dddnsupdate.dddnsupdate:main']
        }
)
