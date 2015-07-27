# -*- coding: utf-8 -*-
from Acquisition import aq_base
from plone.folder.interfaces import IOrderableFolder
from plone.folder.interfaces import IOrdering
from zope.component import adapter
from zope.interface import implementer


@implementer(IOrdering)
@adapter(IOrderableFolder)
class UnorderedOrdering(object):
    """ This implementation provides no ordering. """

    def __init__(self, context):
        self.context = context

    def notifyAdded(self, obj_id):
        pass

    def notifyRemoved(self, obj_id):
        pass

    def idsInOrder(self):
        return aq_base(self.context).objectIds(ordered=False)

    def getObjectPosition(self, obj_id):
        return None
