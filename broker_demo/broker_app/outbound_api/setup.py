# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "imprcm_query_server"
VERSION = "0.0.1"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["connexion"]

setup(
    name=NAME,
    version=VERSION,
    description="Data Query API",
    author_email="imprcmapi@vivacityrail.com",
    url="",
    keywords=["Swagger", "Query API"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['swagger/swagger.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['query_server=imprcm_query_server.__main__:main']},
    long_description="""\
    This API demonstrates data querying of RCM data using IMP-RCM principles.
    """
)

