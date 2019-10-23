from collective.mtrsetup.tests.base import MTRSETUP_INTEGRATION_TESTING
from plone.testing import layered
import doctest
import unittest


FLAGS = doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS


def test_suite():

    suite = unittest.TestSuite()
    suite.addTests([
        layered(doctest.DocFileSuite('../../../README.rst', optionflags=FLAGS), layer=MTRSETUP_INTEGRATION_TESTING),
        layered(doctest.DocFileSuite('../tests/profile.txt', optionflags=FLAGS), layer=MTRSETUP_INTEGRATION_TESTING),
    ])
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
