from pathlib import Path
from setuptools import setup


version = "5.0.0a2.dev0"

long_description = (
    f"{Path('README.rst').read_text()}\n{Path('CHANGES.rst').read_text()}"
)

setup(
    name="plone.folder",
    version=version,
    description="BTree-based folder implementation with order support",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    # Get more strings from
    # https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 6.2",
        "Framework :: Plone :: Core",
        "Framework :: Zope2",
        "Framework :: Zope :: 4",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Other Audience",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="folder btree order",
    author="Plone Foundation",
    author_email="plone-developers@lists.sourceforge.net",
    url="https://pypi.org/project/plone.folder",
    license="GPL version 2",
    include_package_data=True,
    platforms="Any",
    zip_safe=False,
    python_requires=">=3.10",
    install_requires=[
        "Products.CMFCore",
        "Products.ZCatalog",
        "Zope",
    ],
    extras_require={
        "test": [
            "plone.app.testing",
            "profilehooks",
        ]
    },
)
