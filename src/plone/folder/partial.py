from Acquisition import aq_base
from plone.folder.interfaces import IExplicitOrdering
from plone.folder.interfaces import IOrderable
from plone.folder.interfaces import IOrderableFolder
from zope.component import adapts
from zope.container.contained import notifyContainerModified
from zope.interface import implementer


ORDER_ATTR = "_objectordering"


@implementer(IExplicitOrdering)
class PartialOrdering:
    """this implementation uses a list to store order information on a
    regular attribute of the folderish object;  explicit ordering
    is supported"""

    adapts(IOrderableFolder)

    def __init__(self, context):
        self.context = context

    @property
    def order(self):
        context = aq_base(self.context)
        if not hasattr(context, ORDER_ATTR):
            self.order = []
        return getattr(context, ORDER_ATTR)

    @order.setter
    def order(self, value):
        # We added a setter because in py2 order is modified inplace
        # with .sort() while in py3 we sort with sorted and thus need to set it
        # explicitly
        context = aq_base(self.context)
        setattr(context, ORDER_ATTR, value)

    def notifyAdded(self, id):
        """see interfaces.py"""
        assert id not in self.order
        context = aq_base(self.context)
        obj = context._getOb(id)
        if IOrderable.providedBy(obj):
            self.order.append(id)
            self.context._p_changed = True  # the order was changed

    def notifyRemoved(self, id):
        """see interfaces.py"""
        try:
            self.order.remove(id)
            self.context._p_changed = True  # the order was changed
        except ValueError:  # removing non-orderable items is okay
            pass

    def idsInOrder(self, onlyOrderables=False):
        """see interfaces.py"""
        ordered = list(self.order)
        ordered_set = set(ordered)
        if not onlyOrderables:
            ids = aq_base(self.context).objectIds(ordered=False)
            for id in ids:
                if id not in ordered_set:
                    ordered.append(id)
        return ordered

    def moveObjectsByDelta(self, ids, delta, subset_ids=None, suppress_events=False):
        """see interfaces.py"""
        min_position = 0
        if isinstance(ids, str):
            ids = [ids]
        if subset_ids is None:
            subset_ids = self.idsInOrder(onlyOrderables=True)
        elif not isinstance(subset_ids, list):
            subset_ids = list(subset_ids)
        if delta > 0:  # unify moving direction
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
            # micro-optimization: set is 1000 time faster on contains than list
            subset_ids_as_set = set(subset_ids)
            for i, value in enumerate(self.order):
                if value in subset_ids_as_set:
                    id = subset_ids[idx]
                    try:
                        self.order[i] = id
                        idx += 1
                    except KeyError:
                        raise ValueError('No object with id "%s" exists.' % id)
            if idx > 0:
                self.context._p_changed = True  # the order was changed
        if not suppress_events:
            notifyContainerModified(self.context)
        return counter

    def moveObjectsUp(self, ids, delta=1, subset_ids=None):
        """see interfaces.py"""
        return self.moveObjectsByDelta(ids, -delta, subset_ids)

    def moveObjectsDown(self, ids, delta=1, subset_ids=None):
        """see interfaces.py"""
        return self.moveObjectsByDelta(ids, delta, subset_ids)

    def moveObjectsToTop(self, ids, subset_ids=None):
        """see interfaces.py"""
        return self.moveObjectsByDelta(ids, -len(self.order), subset_ids)

    def moveObjectsToBottom(self, ids, subset_ids=None):
        """see interfaces.py"""
        return self.moveObjectsByDelta(ids, len(self.order), subset_ids)

    def moveObjectToPosition(self, id, position, suppress_events=False):
        """see interfaces.py"""
        old_position = self.getObjectPosition(id)
        if old_position is not None:
            delta = position - old_position
            if delta:
                return self.moveObjectsByDelta(
                    id, delta, suppress_events=suppress_events
                )

    def orderObjects(self, key=None, reverse=None):
        """see interfaces.py"""
        if key is None:
            if not reverse:
                return -1
            else:
                # Simply reverse the current ordering.
                self.order.reverse()
        else:

            def keyfn(id):
                attr = getattr(self.context._getOb(id), key)
                if callable(attr):
                    return attr()
                return attr

            self.order = sorted(self.order, key=keyfn, reverse=bool(reverse))
        self.context._p_changed = True  # the order was changed
        return -1

    def getObjectPosition(self, id):
        """see interfaces.py"""
        try:
            # using `index` here might not be that efficient for very large
            # lists, but the idea behind this adapter is to use it when the
            # site contains relatively few "orderable" items
            return self.order.index(id)
        except ValueError:
            # non-orderable objects should return "no position" instead of
            # breaking things when partial ordering support is active...
            if self.context.hasObject(id):
                return None
            raise ValueError('No object with id "%s" exists.' % id)
