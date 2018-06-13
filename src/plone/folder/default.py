# -*- coding: utf-8 -*-
from BTrees.OIBTree import OIBTree
from persistent.list import PersistentList
from plone.folder.interfaces import IExplicitOrdering
from plone.folder.interfaces import IOrderableFolder
from zope.annotation.interfaces import IAnnotations
from zope.component import adapter
from zope.container.contained import notifyContainerModified
from zope.interface import implementer

import six


@implementer(IExplicitOrdering)
@adapter(IOrderableFolder)
class DefaultOrdering(object):
    """ This implementation uses annotations to store the order on the
        object, and supports explicit ordering. """

    ORDER_KEY = "plone.folder.ordered.order"
    POS_KEY = "plone.folder.ordered.pos"

    def __init__(self, context):
        self.context = context

    def notifyAdded(self, obj_id):
        """ see interfaces.py """
        order = self._order(True)
        pos = self._pos(True)
        order.append(obj_id)
        pos[obj_id] = len(order) - 1

    def notifyRemoved(self, obj_id):
        """ see interfaces.py """
        order = self._order()
        pos = self._pos()
        idx = pos[obj_id]
        del order[idx]
        # we now need to rebuild pos since the ids have shifted
        pos.clear()
        for count, obj_id in enumerate(order):
            pos[obj_id] = count

    def moveObjectsByDelta(
        self,
        ids,
        delta,
        subset_ids=None,
        suppress_events=False
    ):
        """ see interfaces.py """
        order = self._order()
        pos = self._pos()
        min_position = 0
        if isinstance(ids, six.string_types):
            ids = [ids]
        if subset_ids is None:
            subset_ids = self.idsInOrder()
        elif not isinstance(subset_ids, list):
            subset_ids = list(subset_ids)
        if delta > 0:                   # unify moving direction
            ids = reversed(ids)
            subset_ids.reverse()
        counter = 0
        for obj_id in ids:
            try:
                old_position = subset_ids.index(obj_id)
            except ValueError:
                continue
            new_position = max(old_position - abs(delta), min_position)
            if new_position == min_position:
                min_position += 1
            if not old_position == new_position:
                subset_ids.remove(obj_id)
                subset_ids.insert(new_position, obj_id)
                counter += 1
        if counter > 0:
            if delta > 0:
                subset_ids.reverse()
            idx = 0
            for i in range(len(order)):
                if order[i] not in subset_ids:
                    continue
                obj_id = subset_ids[idx]
                try:
                    order[i] = obj_id
                    pos[obj_id] = i
                    idx += 1
                except KeyError:
                    raise ValueError(
                        'No object with id "{0:s}" exists.'.format(obj_id)
                    )
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
        return self.moveObjectsByDelta(ids, -len(self._order()), subset_ids)

    def moveObjectsToBottom(self, ids, subset_ids=None):
        """ see interfaces.py """
        return self.moveObjectsByDelta(ids, len(self._order()), subset_ids)

    def moveObjectToPosition(self, obj_id, position, suppress_events=False):
        """ see interfaces.py """
        delta = position - self.getObjectPosition(obj_id)
        if delta:
            return self.moveObjectsByDelta(
                obj_id,
                delta,
                suppress_events=suppress_events
            )

    def orderObjects(self, key=None, reverse=None):
        """ see interfaces.py """
        if key is None and not reverse:
            return -1
        order = self._order()
        pos = self._pos()

        if key is None and reverse:
            # Simply reverse the current ordering.
            order.reverse()
        else:
            def keyfn(obj_id):
                attr = getattr(self.context._getOb(obj_id), key)
                if callable(attr):
                    return attr()
                return attr
            # order.sort(cmd=None, key=keyfn, reverse=bool(reverse))
            order = sorted(order, key=keyfn, reverse=bool(reverse))
            self._set_order(order)
        for n, obj_id in enumerate(order):
            pos[obj_id] = n
        return -1

    def getObjectPosition(self, obj_id):
        """ see interfaces.py """
        pos = self._pos()
        if obj_id in pos:
            return pos[obj_id]
        raise ValueError('No object with id "{0:s}" exists in "{1:s}".'.format(
            obj_id, '/'.join(self.context.getPhysicalPath())))

    def idsInOrder(self):
        """ see interfaces.py """
        return list(self._order())

    def __getitem__(self, index):
        return self._order()[index]

    # Annotation lookup with lazy creation

    def _order(self, create=False):
        annotations = IAnnotations(self.context)
        if create:
            return annotations.setdefault(self.ORDER_KEY, PersistentList())
        return annotations.get(self.ORDER_KEY, [])

    def _set_order(self, value):
        # We added a setter because in py2 _order is modified inplace
        # with .sort() while in py3 we sort with sorted and thus need to set it
        # explicitly
        annotations = IAnnotations(self.context)
        annotations[self.ORDER_KEY] = value

    def _pos(self, create=False):
        annotations = IAnnotations(self.context)
        if create:
            return annotations.setdefault(self.POS_KEY, OIBTree())
        return annotations.get(self.POS_KEY, {})
