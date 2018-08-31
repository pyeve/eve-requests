#!/usr/bin/env python
import io
import re

from setuptools import setup, find_packages

DESCRIPTION = "Client SDK for Eve-powered RESTful APIs"
with open("README.rst") as f:
    LONG_DESCRIPTION = f.read()

with io.open("eve_requests/__init__.py", "rt", encoding="utf8") as f:
    VERSION = re.search(r"__version__ = \"(.*?)\"", f.read()).group(1)

INSTALL_REQUIRES = ["requests"]

EXTRAS_REQUIRE = {
    # "docs": ["sphinx", "alabaster", "sphinxcontrib-embedly"],
    "tests": ["redis", "testfixtures", "pytest", "tox"]
}
EXTRAS_REQUIRE["dev"] = EXTRAS_REQUIRE["tests"]  # + EXTRAS_REQUIRE["docs"]

setup(
    name="Eve-Requests",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Nicola Iarocci",
    author_email="eve@nicolaiarocci.com",
    url="http://python-eve.org",
    project_urls={
        "Documentation": "http://python-eve.org",
        "Code": "https://github.com/pyeve/eve-requests",
        "Issue tracker": "https://github.com/pyeve/eve-requests/issues",
    },
    license="BSD",
    platforms=["any"],
    packages=find_packages(),
    test_suite="tests",
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    python_requires="!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
