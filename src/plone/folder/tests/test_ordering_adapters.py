# -*- coding: utf-8 -*-
from plone.folder.default import DefaultOrdering
from plone.folder.ordered import OrderedBTreeFolderBase
from plone.folder.testing import PLONEFOLDER_INTEGRATION_TESTING
from plone.folder.unordered import UnorderedOrdering
from zope.component import ComponentLookupError

import unittest


class OrderingAdapterTests(unittest.TestCase):
    """ tests regarding available ordering adapters """

    layer = PLONEFOLDER_INTEGRATION_TESTING

    def testDefaultAdapter(self):
        folder = OrderedBTreeFolderBase()
        self.assertTrue(isinstance(folder.getOrdering(), DefaultOrdering))

    def testUnorderedOrdering(self):
        folder = OrderedBTreeFolderBase()
        folder._ordering = 'unordered'
        self.assertTrue(isinstance(folder.getOrdering(), UnorderedOrdering))

    def testUnknownOrdering(self):
        folder = OrderedBTreeFolderBase()
        folder._ordering = 'foo'
        self.assertTrue(isinstance(folder.getOrdering(), DefaultOrdering))

    def testSetOrdering(self):
        folder = OrderedBTreeFolderBase()
        folder.setOrdering('unordered')
        self.assertTrue(isinstance(folder.getOrdering(), UnorderedOrdering))
        folder.setOrdering()
        self.assertTrue(isinstance(folder.getOrdering(), DefaultOrdering))

    def testSetUnknownOrdering(self):
        folder = OrderedBTreeFolderBase()
        self.assertRaises(ComponentLookupError, folder.setOrdering, 'foo')
