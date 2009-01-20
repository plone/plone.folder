from Acquisition import aq_base
from zope.interface import implements
from zope.component import adapts
from plone.folder.interfaces import IOrderable
from plone.folder.interfaces import IOrderableFolder
from plone.folder.interfaces import IExplicitOrdering


ORDER_ATTR = '_objectordering'


class PartialOrdering(object):
    """ this implementation uses a list ot store order information on a
        regular attribute of the folderish object;  explicit ordering
        is supported """
    implements(IExplicitOrdering)
    adapts(IOrderableFolder)

    def __init__(self, context):
        self.context = context

    @property
    def order(self):
        context = aq_base(self.context)
        if not hasattr(context, ORDER_ATTR):
            setattr(context, ORDER_ATTR, [])
        return getattr(context, ORDER_ATTR)

    def notifyAdded(self, id, obj):
        """ see interfaces.py """
        assert not id in self.order
        if IOrderable.providedBy(obj):
            self.order.append(id)

    def notifyRemoved(self, id):
        """ see interfaces.py """
        self.order.remove(id)

    def idsInOrder(self):
        """ see interfaces.py """
        return list(self.order)

