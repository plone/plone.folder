from zope.interface import implements
from zope.component import adapts
from plone.folder.interfaces import IOrderableFolder
from plone.folder.interfaces import IExplicitOrdering


class PartialOrdering(object):
    """ this implementation uses a list ot store order information on a
        regular attribute of the folderish object;  explicit ordering
        is supported """
    implements(IExplicitOrdering)
    adapts(IOrderableFolder)

    def __init__(self, context):
        self.context = context

