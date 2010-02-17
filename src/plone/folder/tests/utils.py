from zope.interface import implements
from zope.component import getAdapter, queryAdapter
from zope.annotation.interfaces import IAttributeAnnotatable
from plone.folder.interfaces import IOrderable, IOrderableFolder, IOrdering


class DummyObject(object):

    def __init__(self, id, meta_type=None):
        self.id = id
        self.meta_type = meta_type

    def __of__(self, obj):
        return self

    def manage_fixupOwnershipAfterAdd(self):
        pass


class DummyContainer(object):
    implements(IOrderableFolder, IAttributeAnnotatable)

    _ordering = u''         # name of adapter defining ordering policy

    def __init__(self):
        self.objs = {}

    @property
    def ordering(self):
        adapter = queryAdapter(self, IOrdering, name=self._ordering)
        if adapter is None:
            adapter = getAdapter(self, IOrdering)
        return adapter

    def add(self, id, obj):
        self.objs[id] = obj
        self.ordering.notifyAdded(id)           # notify the ordering adapter

    def remove(self, id):
        del self.objs[id]
        self.ordering.notifyRemoved(id)         # notify the ordering adapter

    def objectIds(self, spec=None, ordered=True):
        return set(self.objs)

    def _getOb(self, id, default=None):
        return self.objs.get(id, default)

    def hasObject(self, id):
        return id in self.objs


class Orderable(DummyObject):
    """ orderable mock object """
    implements(IOrderable)


class Chaoticle(DummyObject):
    """ non-orderable mock object;  this does not implement `IOrderable` """
