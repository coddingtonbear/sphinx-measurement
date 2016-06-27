import os
from setuptools import setup, find_packages
import sys
import uuid


requirements_path = os.path.join(
    os.path.dirname(__file__),
    'requirements.txt',
)
try:
    from pip.req import parse_requirements
    requirements = [
        str(req.req) for req in parse_requirements(
            requirements_path,
            session=uuid.uuid1()
        )
    ]
except ImportError:
    requirements = []
    with open(requirements_path, 'r') as in_:
        requirements = [
            req for req in in_.readlines()
            if not req.startswith('-')
            and not req.startswith('#')
        ]


setup(
    name='sphinx-measurement',
    version='0.1',
    url='https://github.com/coddingtonbear/sphinx-measurement',
    description=(
        'Embed and convert measurements easily within your sphinx document.'
    ),
    author='Adam Coddington',
    author_email='me@adamcoddington.net',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    include_package_data = True,
    install_requires=requirements,
    packages=find_packages(),
)
