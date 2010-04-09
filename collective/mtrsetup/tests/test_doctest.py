import unittest
import doctest

#from zope.testing import doctestunit
#from zope.component import testing, eventtesting

from Testing import ZopeTestCase as ztc

from collective.mtrsetup.tests import base

functionl_doctest_files = [
    'README.txt',
    'tests/profile.txt',
    ]

def test_suite():
    return unittest.TestSuite([
            # Demonstrate the main content types
            ztc.ZopeDocFileSuite(
                file_, package='collective.mtrsetup',
                test_class=base.FunctionalTestCase,
                optionflags=doctest.REPORT_ONLY_FIRST_FAILURE |
                doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS)
            for file_ in functionl_doctest_files
            ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
