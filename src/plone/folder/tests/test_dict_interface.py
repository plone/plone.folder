from Acquisition import aq_base
from plone.folder.ordered import OrderedBTreeFolderBase
from plone.folder.testing import PLONEFOLDER_INTEGRATION_TESTING
from plone.folder.tests.utils import DummyObject

import unittest


class DictInterfaceTests(unittest.TestCase):
    """tests for dict style interface"""

    layer = PLONEFOLDER_INTEGRATION_TESTING

    def test_getitem(self):
        folder = OrderedBTreeFolderBase("f1")
        foo = DummyObject("foo")
        folder._setOb("foo", foo)
        self.assertEqual(folder["foo"], foo)
        self.assertEqual(folder.__getitem__("foo"), foo)
        self.assertRaises(KeyError, folder.__getitem__, "bar")

    def test_setitem(self):
        folder = OrderedBTreeFolderBase("f1")
        foo = DummyObject("foo")
        folder["foo"] = foo
        self.assertEqual(folder._getOb("foo"), foo)

    def test_contains(self):
        folder = OrderedBTreeFolderBase("f1")
        folder._setOb("foo", DummyObject("foo"))
        folder._setOb("bar", DummyObject("bar"))
        self.assertTrue("foo" in folder)
        self.assertTrue("bar" in folder)

    def test_delitem(self):
        folder = OrderedBTreeFolderBase("f1")
        folder._setOb("foo", DummyObject("foo"))
        folder._setOb("bar", DummyObject("bar"))
        self.assertEqual(len(folder.objectIds()), 2)
        del folder["foo"]
        del folder["bar"]
        self.assertEqual(len(folder.objectIds()), 0)

    def test_len_empty_folder(self):
        folder = OrderedBTreeFolderBase("f1")
        self.assertEqual(len(folder), 0)

    def test_len_one_child(self):
        folder = OrderedBTreeFolderBase("f1")
        folder["child"] = DummyObject("child")
        self.assertEqual(len(folder), 1)

    def test_to_verify_ticket_9120(self):
        folder = OrderedBTreeFolderBase("f1")
        folder["ob1"] = ob1 = DummyObject("ob1")
        folder["ob2"] = DummyObject("ob2")
        folder["ob3"] = DummyObject("ob3")
        folder["ob4"] = ob4 = DummyObject("ob4")
        del folder["ob2"]
        del folder["ob3"]
        self.assertEqual(folder.keys(), ["ob1", "ob4"])
        self.assertEqual(list(map(aq_base, folder.values())), [ob1, ob4])
        self.assertEqual([key in folder for key in folder], [True, True])


class RelatedToDictInterfaceTests(unittest.TestCase):
    """various tests which are related to the dict-like interface"""

    layer = PLONEFOLDER_INTEGRATION_TESTING

    def create(self):
        folder = OrderedBTreeFolderBase("f1")
        folder._setOb("o1", DummyObject("o1", "mt1"))
        folder._setOb("o2", DummyObject("o2", "mt2"))
        folder._setOb("o3", DummyObject("o3", "mt1"))
        folder._setOb("o4", DummyObject("o4", "mt2"))
        return folder

    def testObjectIdsWithSpec(self):
        folder = self.create()
        self.assertEqual(["o1", "o3"], folder.objectIds(spec="mt1"))
        self.assertEqual(["o2", "o4"], folder.objectIds(spec="mt2"))
        folder.moveObjectsToTop(["o3"])
        folder.moveObjectsDown(["o2"])
        self.assertEqual(["o3", "o1"], folder.objectIds(spec="mt1"))
        self.assertEqual(["o4", "o2"], folder.objectIds(spec="mt2"))
