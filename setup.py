import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open('requirements.txt') as f:
    install_reqs = f.readlines()
    reqs = [str(ir) for ir in install_reqs]

setup(
    name='belvo-transactions',
    version='1.0.0',
    url='https://github.com/blankazucenalg/belvo-challenge-api',
    license='MIT',
    author='Blanca Azucena López Garduño',
    author_email='blankazucenalg@gmail.com',
    description='A RESTful API for transactions',
    packages=find_packages(),
    include_package_data=True,
    install_requires=reqs
)
