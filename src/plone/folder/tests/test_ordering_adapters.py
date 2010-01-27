from unittest import TestCase, defaultTestLoader
from plone.folder.ordered import OrderedBTreeFolderBase
from plone.folder.default import DefaultOrdering
from plone.folder.unordered import UnorderedOrdering
from plone.folder.tests.layer import PloneFolderLayer


class OrderingAdapterTests(TestCase):
    """ tests regarding available ordering adapters """

    layer = PloneFolderLayer

    def testDefaultAdapter(self):
        folder = OrderedBTreeFolderBase()
        self.failUnless(isinstance(folder.getOrdering(), DefaultOrdering))

    def testUnorderedOrdering(self):
        folder = OrderedBTreeFolderBase()
        folder._ordering = 'unordered'
        self.failUnless(isinstance(folder.getOrdering(), UnorderedOrdering))

    def testUnknownOrdering(self):
        folder = OrderedBTreeFolderBase()
        folder._ordering = 'foo'
        self.failUnless(isinstance(folder.getOrdering(), DefaultOrdering))

    def testSetOrdering(self):
        folder = OrderedBTreeFolderBase()
        folder.setOrdering('unordered')
        self.failUnless(isinstance(folder.getOrdering(), UnorderedOrdering))
        folder.setOrdering()
        self.failUnless(isinstance(folder.getOrdering(), DefaultOrdering))


def test_suite():
    return defaultTestLoader.loadTestsFromName(__name__)
