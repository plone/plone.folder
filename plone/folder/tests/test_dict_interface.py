from unittest import TestCase, defaultTestLoader

import Acquisition
from plone.folder.ordered import OrderedBTreeFolderBase
from plone.folder.tests.layer import PloneFolderLayer


class Mock(Acquisition.Explicit):
    def manage_fixupOwnershipAfterAdd(self):
        pass


class DictInterfaceTests(TestCase):
    """ tests borrowed from OFS.tests.testOrderSupport """

    layer = PloneFolderLayer

    def create(self):
        folder = OrderedBTreeFolderBase("f1")
        return folder

    # Test for dict style interface

    def test_len_empty_folder(self):
        folder = self.create()
        self.assertEquals(len(folder), 0)

    def test_len_one_child(self):
        folder = self.create()
        folder["child"] = Mock()
        self.assertEquals(len(folder), 1)


def test_suite():
    return defaultTestLoader.loadTestsFromName(__name__)

