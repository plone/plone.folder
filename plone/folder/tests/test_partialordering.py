from unittest import TestCase, defaultTestLoader
from zope.component import provideAdapter
from zope.component import testing
from plone.folder.interfaces import IOrdering
from plone.folder.partial import PartialOrdering
from plone.folder.tests.utils import DummyContainer


class Layer:

    @classmethod
    def setUp(cls):
        provideAdapter(PartialOrdering)

    @classmethod
    def tearDown(cls):
        testing.tearDown


class PartialOrderingTests(TestCase):
    """ tests regarding order-support for only items marked orderable """

    layer = Layer

    def setUp(self):
        self.container = DummyContainer()

    def testAdapter(self):
        ordering = IOrdering(self.container)
        self.failUnless(ordering)


def test_suite():
    return defaultTestLoader.loadTestsFromName(__name__)

