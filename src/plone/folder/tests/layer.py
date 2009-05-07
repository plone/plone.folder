from zope.component import provideAdapter
from zope.annotation.attribute import AttributeAnnotations
from plone.folder.default import DefaultOrdering
from plone.folder.partial import PartialOrdering


class PloneFolderLayer:

    @classmethod
    def setUp(cls):
        provideAdapter(DefaultOrdering)
        provideAdapter(AttributeAnnotations)

    @classmethod
    def tearDown(cls):
        pass


class PartialOrderingLayer:

    @classmethod
    def setUp(cls):
        provideAdapter(PartialOrdering)

    @classmethod
    def tearDown(cls):
        pass
