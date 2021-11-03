
from setuptools import setup, find_packages  # noqa: H301

NAME = "streamduo"
VERSION = "0.0.9-alpha"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["urllib3 >= 1.15", "six >= 1.10", "certifi", "python-dateutil"]

setup(
    name=NAME,
    version=VERSION,
    description="streamduo.com API",
    author_email="steve@streamduo.com",
    url="",
    keywords=["Swagger", "streamduo.com API"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description="""\
    Swagger docs for streamduo.com  # noqa: E501
    """
)