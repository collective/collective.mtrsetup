from setuptools import setup, find_packages
import os

version = '1.6.1.dev0'

tests_require = [
    'Plone',
    'zope.testing',
    'plone.app.testing',
    ]

setup(name='collective.mtrsetup',
      version=version,
      description="Extension for GenericSetup, adding support for import / export of mimetypes_registry",
      long_description=open("README.rst").read() + "\n" + \
          open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone :: 4.2",
        "Framework :: Plone :: 4.3",
        "Framework :: Plone :: 5.1",
        "Programming Language :: Python",
        ],
      keywords='generic setup gs mimetypes registry import export',
      author='Jonas Baumann, 4teamwork GmbH',
      author_email='mailto:info@4teamwork.ch',
      url='https://github.com/collective/collective.mtrsetup',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        'Products.GenericSetup',
        'Products.MimetypesRegistry',
        # -*- Extra requirements: -*-
        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      #      test_suite = 'collective.mtrsetup.tests.test'
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
