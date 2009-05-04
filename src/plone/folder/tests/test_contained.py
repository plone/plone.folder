from unittest import TestCase, defaultTestLoader

from zope.interface import implements
from zope.location.interfaces import ILocation
from zope.app.container.interfaces import IContained
from zope.app.container.contained import Contained
from plone.folder.ordered import OrderedBTreeFolderBase
from plone.folder.tests.layer import PloneFolderLayer
from plone.folder.tests.utils import DummyObject


class DummyLocatable(DummyObject):
    implements(ILocation)

    def __init__(self, id=None, meta_type='DummyLocatable'):
        super(DummyLocatable, self).__init__(id, meta_type)


class DummyContained(DummyObject, Contained):
    implements(ILocation)

    def __init__(self, id=None, meta_type='DummyContained'):
        super(DummyContained, self).__init__(id, meta_type)


class DummyNonLocatable(DummyObject):

    def __init__(self, id=None, meta_type='DummyNonLocatable'):
        super(DummyNonLocatable, self).__init__(id, meta_type)


class ContainedTests(TestCase):
    """ tests regarding support for IContainer/IContained """

    layer = PloneFolderLayer

    def test_setitem_sets_IContained_and_parent_for_ILocation(self):
        folder = OrderedBTreeFolderBase("f1")
        folder['locatable'] = DummyLocatable()
        self.failUnless(IContained.providedBy(folder['locatable']))
        self.failUnless(folder['locatable'].__parent__ is folder)
        self.assertEquals('locatable', folder['locatable'].__name__)

    def test_setitem_sets_parent_for_IContained(self):
        folder = OrderedBTreeFolderBase("f1")
        folder['contained'] = DummyContained()
        self.failUnless(IContained.providedBy(folder['contained']))
        self.failUnless(folder['contained'].__parent__ is folder)
        self.assertEquals('contained', folder['contained'].__name__)

    def test_setitem_does_not_set_parent_or_IContained_for_non_ILocation(self):
        folder = OrderedBTreeFolderBase("f1")
        folder['other'] = DummyNonLocatable()
        self.failIf(IContained.providedBy(folder['other']))
        self.failIf(hasattr(folder['other'], '__parent__'))

    def test_delitem(self):
        folder = OrderedBTreeFolderBase("f1")
        folder['locatable'] = DummyLocatable()
        folder['contained'] = DummyContained()
        folder['other'] = DummyNonLocatable()
        # Make sure these don't fail when attempting to unset __parent__
        del folder['locatable']
        del folder['contained']
        del folder['other']


def test_suite():
    return defaultTestLoader.loadTestsFromName(__name__)
