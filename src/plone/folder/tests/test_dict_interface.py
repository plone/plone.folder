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


def test_suite():
    return defaultTestLoader.loadTestsFromName(__name__)
