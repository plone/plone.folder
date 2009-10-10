from setuptools import setup, find_packages
from os.path import join

version = '1.0b1'
readme = open(join('README.txt')).read()
history = open(join('docs', 'HISTORY.txt')).read()

setup(name = 'plone.folder',
      version = version,
      description = 'BTree-based folder implementation with order support',
      long_description = readme[readme.find('\n\n'):] + '\n' + history,
      classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords = 'folder btree order',
      author = 'Plone Foundation',
      author_email = 'plone-developers@lists.sourceforge.net',
      url = 'http://pypi.python.org/pypi/plone.folder/',
      license = 'LGPL',
      packages = find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages = ['plone'],
      include_package_data = True,
      platforms = 'Any',
      zip_safe = False,
      install_requires = [
          'setuptools',
      ],
      tests_require = [
          'zope.testing',
      ],
      entry_points = '',
)
