from zope.interface import implements
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
    implements(IOrderableFolder)

    def __init__(self):
        self.objs = {}

    def add(self, id, obj):
        self.objs[id] = obj
        IOrdering(self).notifyAdded(id)         # notify the ordering adapter

    def remove(self, id):
        del self.objs[id]
        IOrdering(self).notifyRemoved(id)       # notify the ordering adapter

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
