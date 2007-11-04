from zope.interface import implements
from persistent.list import PersistentList
from zope.app.container.contained import notifyContainerModified

from AccessControl import ClassSecurityInfo
from AccessControl.Permissions import access_contents_information
from AccessControl.Permissions import manage_properties
from BTrees.OLBTree import OLBTree
from OFS.interfaces import IOrderedContainer

from Products.BTreeFolder2.BTreeFolder2 import BTreeFolder2Base
from Products.CMFCore.PortalFolder import PortalFolderBase


class OrderedBTreeFolderBase(BTreeFolder2Base, PortalFolderBase):
    """BTree folder for CMF sites, with ordering support
    """
    implements(IOrderedContainer)

    _order = None       # PersistentList: { index -> id }
    _pos = None         # OLBTree: { id -> index }

    security = ClassSecurityInfo()

    def __init__(self, id, title=''):
        PortalFolderBase.__init__(self, id, title)
        BTreeFolder2Base.__init__(self, id)
        self._order = PersistentList()
        self._pos = OLBTree()

    def _checkId(self, id, allow_dup=0):
        PortalFolderBase._checkId(self, id, allow_dup)
        BTreeFolder2Base._checkId(self, id, allow_dup)

    # IObjectManager
    
    def _setOb(self, id, object):
        """Store the named object in the folder.
        """
        super(OrderedBTreeFolderBase, self)._setOb(id, object)
        self._order.append(id)
        self._pos[id] = len(self._order) - 1

    def _delOb(self, id):
        """Remove the named object from the folder.
        """
        super(OrderedBTreeFolderBase, self)._delOb(id)
        pos = self._pos[id]
        del self._order[pos]
        del self._pos[id]
                    
    def objectIds(self, spec=None):
        if spec is None:
            return list(self._order)
        else:
            # TODO: revisit this to see if it can be more efficient...
            ids = super(OrderedBTreeFolderBase, self).objectIds(spec)
            idxs = []
            for id in ids:
                idxs.append((self._pos[id], id))
            return [ x[1] for x in sorted(idxs, cmp=lambda a,b: cmp(a[0], b[0])) ]
        
    # IOrderSupport
        
    security.declareProtected(manage_properties, 'moveObjectsByDelta')
    def moveObjectsByDelta(self, ids, delta, subset_ids=None,
                           suppress_events=False):
        """ Move specified sub-objects by delta.
        """
        if isinstance(ids, basestring):
            ids = (ids,)
        min_position = 0
        if subset_ids is None:
            subset_ids = list(self.objectIds())
        else:
            subset_ids = list(subset_ids)
        # unify moving direction
        if delta > 0:
            ids = reversed(ids)
            subset_ids.reverse()
        counter = 0

        for id in ids:
            try:
                old_position = subset_ids.index(id)
            except ValueError:
                continue
            new_position = max( old_position - abs(delta), min_position )
            if new_position == min_position:
                min_position += 1
            if not old_position == new_position:
                subset_ids.remove(id)
                subset_ids.insert(new_position, id)
                counter += 1

        if counter > 0:
            if delta > 0:
                subset_ids.reverse()
            pos = 0
            order = self._order
            for i in range(len(order)):
                if order[i] in subset_ids:
                    id = subset_ids[pos]
                    try:
                        order[i] = id
                        self._pos[id] = i
                        pos += 1
                    except KeyError:
                        raise ValueError('The object with the id "%s" does '
                                         'not exist.' % id)

        if not suppress_events:
            notifyContainerModified(self)

        return counter

    security.declareProtected(manage_properties, 'moveObjectsUp')
    def moveObjectsUp(self, ids, delta=1, subset_ids=None):
        """ Move specified sub-objects up by delta in container.
        """
        return self.moveObjectsByDelta(ids, -delta, subset_ids)

    security.declareProtected(manage_properties, 'moveObjectsDown')
    def moveObjectsDown(self, ids, delta=1, subset_ids=None):
        """ Move specified sub-objects down by delta in container.
        """
        return self.moveObjectsByDelta(ids, delta, subset_ids)

    security.declareProtected(manage_properties, 'moveObjectsToTop')
    def moveObjectsToTop(self, ids, subset_ids=None):
        """ Move specified sub-objects to top of container.
        """
        return self.moveObjectsByDelta( ids, -self.objectCount(), subset_ids )

    security.declareProtected(manage_properties, 'moveObjectsToBottom')
    def moveObjectsToBottom(self, ids, subset_ids=None):
        """ Move specified sub-objects to bottom of container.
        """
        return self.moveObjectsByDelta( ids, self.objectCount(), subset_ids )

    security.declareProtected(manage_properties, 'orderObjects')
    def orderObjects(self, key, reverse=None):
        """ Order sub-objects by key and direction.
        """
        keyfn = lambda id: getattr(self._tree[id], key)
        self._order.sort(None, keyfn, bool(reverse))
        for n, id in enumerate(self._order):
            self._pos[id] = n
        return -1

    security.declareProtected(access_contents_information, 'getObjectPosition')
    def getObjectPosition(self, id):
        """ Get the position of an object by its id.
        """
        if self._pos.has_key(id):
            return self._pos[id]
        else:
            raise ValueError('The object with the id "%s" does not exist.' % id)

    security.declareProtected(manage_properties, 'moveObjectToPosition')
    def moveObjectToPosition(self, id, position, suppress_events=False):
        """ Move specified object to absolute position.
        """
        delta = position - self.getObjectPosition(id)
        return self.moveObjectsByDelta(id, delta,
                                       suppress_events=suppress_events)
                                       
    def manage_renameObject(self, id, new_id, REQUEST=None):
        """ Rename a particular sub-object without changing its position.
        """
        old_position = self.getObjectPosition(id)
        result = super(OrderSupport, self).manage_renameObject(id, new_id,
                                                               REQUEST)
        self.moveObjectToPosition(new_id, old_position, suppress_events=True)
        return result