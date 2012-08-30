from setuptools import setup, find_packages

version = '1.0.3'

setup(name='plone.folder',
      version=version,
      description='BTree-based folder implementation with order support',
      long_description=open("README.txt").read() + "\n" +
                       open("CHANGES.txt").read(),
      classifiers=[
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Framework :: Zope2",
          "Intended Audience :: Developers",
          "Intended Audience :: System Administrators",
          "Intended Audience :: Other Audience",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
        ],
      keywords='folder btree order',
      author='Plone Foundation',
      author_email='plone-developers@lists.sourceforge.net',
      url='http://pypi.python.org/pypi/plone.folder',
      license='GPL version 2',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['plone'],
      include_package_data=True,
      platforms='Any',
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.memoize',
          'zope.interface',
          'zope.component',
          'zope.annotation',
          'zope.container',
      ],
      extras_require={'test': [
          'profilehooks',
          'Products.CMFCore',
      ]},
)
