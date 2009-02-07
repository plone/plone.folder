from zope.component import provideAdapter
from zope.component import testing

from plone.folder.default import DefaultOrdering
from plone.folder.partial import PartialOrdering
from zope.annotation.attribute import AttributeAnnotations


class PloneFolderLayer:

    @classmethod
    def setUp(cls):
        provideAdapter(DefaultOrdering)
        provideAdapter(AttributeAnnotations)

    @classmethod
    def tearDown(cls):
        testing.tearDown


class PloneFolderPartialOrderingLayer:

    @classmethod
    def setUp(cls):
        provideAdapter(PartialOrdering)

    @classmethod
    def tearDown(cls):
        testing.tearDown
