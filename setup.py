from setuptools import setup, find_packages

version = '3.1.0'

setup(
    name='plone.folder',
    version=version,
    description='BTree-based folder implementation with order support',
    long_description=(open("README.rst").read() + "\n" +
                      open("CHANGES.rst").read()),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 5.2",
        "Framework :: Plone :: Core",
        "Framework :: Zope2",
        "Framework :: Zope :: 4",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Other Audience",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords='folder btree order',
    author='Plone Foundation',
    author_email='plone-developers@lists.sourceforge.net',
    url='https://pypi.org/project/plone.folder',
    license='GPL version 2',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['plone'],
    include_package_data=True,
    platforms='Any',
    zip_safe=False,
    install_requires=[
        'plone.memoize',
        'Products.BTreeFolder2',
        'Products.CMFCore',
        'Products.ZCatalog',
        'setuptools',
        'six',
        'zope.annotation',
        'zope.component',
        'zope.container',
        'zope.interface',
        'Zope2',
    ],
    extras_require={
        'test': [
            'profilehooks',
        ]
    },
)
