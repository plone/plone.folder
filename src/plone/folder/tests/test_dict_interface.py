from unittest import TestCase, defaultTestLoader

from plone.folder.ordered import OrderedBTreeFolderBase
from plone.folder.tests.layer import PloneFolderLayer
from plone.folder.tests.utils import DummyObject


class DictInterfaceTests(TestCase):
    """ tests for dict style interface """

    layer = PloneFolderLayer

    def create(self):
        folder = OrderedBTreeFolderBase("f1")
        return folder

    def test_len_empty_folder(self):
        folder = self.create()
        self.assertEquals(len(folder), 0)

    def test_len_one_child(self):
        folder = self.create()
        folder['child'] = DummyObject('child')
        self.assertEquals(len(folder), 1)


class RelatedToDictInterfaceTests(TestCase):
    """ various tests which are related to the dict-like interface """

    layer = PloneFolderLayer

    def create(self):
        folder = OrderedBTreeFolderBase("f1")
        folder._setOb('o1', DummyObject('o1', 'mt1'))
        folder._setOb('o2', DummyObject('o2', 'mt2'))
        folder._setOb('o3', DummyObject('o3', 'mt1'))
        folder._setOb('o4', DummyObject('o4', 'mt2'))
        return folder

    def testObjectIdsWithSpec(self):
        folder = self.create()
        self.assertEquals(['o1', 'o3'], folder.objectIds(spec='mt1'))
        self.assertEquals(['o2', 'o4'], folder.objectIds(spec='mt2'))
        folder.moveObjectsToTop(['o3'])
        folder.moveObjectsDown(['o2'])
        self.assertEquals(['o3', 'o1'], folder.objectIds(spec='mt1'))
        self.assertEquals(['o4', 'o2'], folder.objectIds(spec='mt2'))


def test_suite():
    return defaultTestLoader.loadTestsFromName(__name__)
