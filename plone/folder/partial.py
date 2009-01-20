from Acquisition import aq_base
from zope.interface import implements
from zope.component import adapts
from zope.app.container.contained import notifyContainerModified
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

    def moveObjectsByDelta(self, ids, delta, subset_ids=None, suppress_events=False):
        """ see interfaces.py """
        min_position = 0
        if isinstance(ids, basestring):
            ids = (ids,)
        if subset_ids is None:
            subset_ids = self.idsInOrder()
        elif not isinstance(subset_ids, list):
            subset_ids = list(subset_ids)
        if delta > 0:                   # unify moving direction
            ids = reversed(ids)
            subset_ids.reverse()
        counter = 0
        for id in ids:
            try:
                old_position = subset_ids.index(id)
            except ValueError:
                continue
            new_position = max(old_position - abs(delta), min_position)
            if new_position == min_position:
                min_position += 1
            if not old_position == new_position:
                subset_ids.remove(id)
                subset_ids.insert(new_position, id)
                counter += 1
        if counter > 0:
            if delta > 0:
                subset_ids.reverse()
            idx = 0
            for i, value in enumerate(self.order):
                if value in subset_ids:
                    id = subset_ids[idx]
                    try:
                        self.order[i] = id
                        idx += 1
                    except KeyError:
                        raise ValueError('No object with id "%s" exists.' % id)
        if not suppress_events:
            notifyContainerModified(self.context)
        return counter

    def moveObjectsUp(self, ids, delta=1, subset_ids=None):
        """ see interfaces.py """
        return self.moveObjectsByDelta(ids, -delta, subset_ids)

    def moveObjectsDown(self, ids, delta=1, subset_ids=None):
        """ see interfaces.py """
        return self.moveObjectsByDelta(ids, delta, subset_ids)

    def moveObjectsToTop(self, ids, subset_ids=None):
        """ see interfaces.py """
        return self.moveObjectsByDelta(ids, -len(self.order), subset_ids )

    def moveObjectsToBottom(self, ids, subset_ids=None):
        """ see interfaces.py """
        return self.moveObjectsByDelta(ids, len(self.order), subset_ids )

    def moveObjectToPosition(self, id, position, suppress_events=False):
        """ see interfaces.py """
        delta = position - self.getObjectPosition(id)
        if delta:
            return self.moveObjectsByDelta(id, delta, suppress_events=suppress_events)

    def orderObjects(self, key, reverse=None):
        """ see interfaces.py """
        keyfn = lambda id: getattr(self.context._getOb(id), key)
        self.order.sort(None, keyfn, bool(reverse))
        return -1

    def getObjectPosition(self, id):
        """ see interfaces.py """
        try:
            return self.order.index(id)
        except ValueError:
            raise ValueError('No object with id "%s" exists.' % id)


