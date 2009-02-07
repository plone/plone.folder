from unittest import defaultTestLoader
from plone.folder.interfaces import IOrderable
from plone.folder.tests.base import IntegrationTestCase, PloneFolderLayer
from plone.folder.tests.layer import PloneFolderPartialOrderingLayer


class Layer(PloneFolderPartialOrderingLayer, PloneFolderLayer):
    """ test layer for partial ordering support """


class PartialOrderingTests(IntegrationTestCase):
    """ tests regarding order-support for only items marked orderable """

    layer = Layer

    def testGetObjectPositionForNonOrderableContent(self):
        oid = self.folder.invokeFactory('Event', id='foo')
        obj = self.folder._getOb(oid)
        # a non-orderable object should return "no position"
        self.failIf(IOrderable.providedBy(obj), 'orderable events?')
        self.assertEqual(self.folder.getObjectPosition(oid), None)
        # a non-existant object should raise an error, though
        self.assertRaises(ValueError, self.folder.getObjectPosition, 'bar')


def test_suite():
    return defaultTestLoader.loadTestsFromName(__name__)

