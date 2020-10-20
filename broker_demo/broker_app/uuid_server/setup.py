# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "imprcm_uuid_server"
VERSION = "0.0.2"

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
    description="UUID Repository API",
    author_email="imprcmapi@vivacityrail.com",
    url="",
    keywords=["Swagger", "UUID Repository API"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['swagger/swagger.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['uuid_server=imprcm_uuid_server.__main__:main']},
    long_description="""\
    This API demonstrates a way of referencing and supplying UUIDs for IMP-RCM assets.
    """
)

