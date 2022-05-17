
from setuptools import setup, find_packages

NAME = "streamduo"
VERSION = "0.0.35"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["requests", "jsonschema", "pynacl", "pandas", "great_expectations"]

setup(
    name=NAME,
    version=VERSION,
    description="streamduo.com API",
    author_email="steve@streamduo.com",
    url="",
    keywords=["streamduo.com API"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description="""\
    SDK for streamduo.com
    """
)
