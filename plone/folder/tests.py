import unittest

from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
ptc.setupPloneSite()

import plone.folder

class TestCase(ptc.PloneTestCase):
    pass
    

def test_suite():
    return unittest.TestSuite([unittest.makeSuite(TestCase)])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')