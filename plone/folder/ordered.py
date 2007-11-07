from zope.interface import implements
from zope.component import adapts

from zope.annotation.interfaces import IAnnotations
from zope.annotation.interfaces import IAttributeAnnotatable

from persistent.list import PersistentList
from zope.app.container.contained import notifyContainerModified

from AccessControl import ClassSecurityInfo
from AccessControl.Permissions import access_contents_information
from AccessControl.Permissions import manage_properties
from AccessControl.Permissions import delete_objects
from AccessControl.Permissions import view
from BTrees.OLBTree import OLBTree
from OFS.interfaces import IOrderedContainer

from Products.BTreeFolder2.BTreeFolder2 import BTreeFolder2Base, _marker
from Products.CMFCore.PortalFolder import PortalFolderBase
from Products.CMFCore.permissions import ModifyPortalContent

from AccessControl import Unauthorized
from Products.CMFCore import permissions
from Products.CMFCore.utils import _checkPermission

from plone.folder.interfaces import IOrderableFolder
from plone.folder.interfaces import IOrdering
from plone.folder.interfaces import IExplicitOrdering

from plone.memoize.instance import memoize

class OrderedBTreeFolderBase(BTreeFolder2Base, PortalFolderBase):
    """BTree folder for CMF sites, with ordering support. The ordering is
    done by adapter (to IOrdering), which makes the policy changeable.
    """
    implements(IOrderedContainer, IOrderableFolder, IAttributeAnnotatable)

    security = ClassSecurityInfo()

    def __init__(self, id, title=''):
        PortalFolderBase.__init__(self, id, title)
        BTreeFolder2Base.__init__(self, id)

    def _checkId(self, id, allow_dup=0):
        PortalFolderBase._checkId(self, id, allow_dup)
        BTreeFolder2Base._checkId(self, id, allow_dup)

    # IObjectManager
    
    def _getOb(self, id, default=_marker):
        """Return the named object from the folder.
        """
        try:
            return super(OrderedBTreeFolderBase, self)._getOb(id, default)
        except KeyError, e:
            raise AttributeError(e)
    
    def _setOb(self, id, object):
        """Store the named object in the folder.
        """
        super(OrderedBTreeFolderBase, self)._setOb(id, object)
        
        # Notify the ordering adapter
        IOrdering(self).notifyAdded(id)

    def _delOb(self, id):
        """Remove the named object from the folder.
        """
        super(OrderedBTreeFolderBase, self)._delOb(id)
        
        # Notify the ordering adapter
        IOrdering(self).notifyRemoved(id)

    def objectIds(self, spec=None):
        ordering = IOrdering(self)
        
        if spec is None:
            return ordering.idsInOrder()
        else:
            ids = super(OrderedBTreeFolderBase, self).objectIds(spec)
            idxs = []
            for id in ids:
                idxs.append((ordering.getObjectPosition(id), id))
            return [ x[1] for x in sorted(idxs, cmp=lambda a,b: cmp(a[0], b[0])) ]
        
    # IOrderSupport - mostly deprecated, use the adapter directly instead
    
    security.declareProtected(access_contents_information, 'getObjectPosition')
    def getObjectPosition(self, id):
        """Get the position of an object by its id.
        """
        return IOrdering(self).getObjectPosition(id) 

    security.declareProtected(manage_properties, 'moveObjectsUp')
    def moveObjectsUp(self, ids, delta=1, subset_ids=None):
        """ Move specified sub-objects up by delta in container.
        """
        ordering = IOrdering(self)
        if IExplicitOrdering.providedBy(ordering):
            return ordering.moveObjectsUp(ids, delta, subset_ids)
        else:
            return 0

    security.declareProtected(manage_properties, 'moveObjectsDown')
    def moveObjectsDown(self, ids, delta=1, subset_ids=None):
        """ Move specified sub-objects down by delta in container.
        """
        ordering = IOrdering(self)
        if IExplicitOrdering.providedBy(ordering):
            return ordering.moveObjectsDown(ids, delta, subset_ids)
        else:
            return 0

    security.declareProtected(manage_properties, 'moveObjectsToTop')
    def moveObjectsToTop(self, ids, subset_ids=None):
        """ Move specified sub-objects to top of container.
        """
        ordering = IOrdering(self)
        if IExplicitOrdering.providedBy(ordering):
            return ordering.moveObjectsToTop(ids, subset_ids)
        else:
            return 0

    security.declareProtected(manage_properties, 'moveObjectsToBottom')
    def moveObjectsToBottom(self, ids, subset_ids=None):
        """ Move specified sub-objects to bottom of container.
        """
        ordering = IOrdering(self)
        if IExplicitOrdering.providedBy(ordering):
            return ordering.moveObjectsToBottom(ids, subset_ids)
        else:
            return 0

    security.declareProtected(ModifyPortalContent, 'moveObject')
    def moveObject(self, id, position):
        """ Move specified object to absolute position.
        """
        ordering = IOrdering(self)
        if IExplicitOrdering.providedBy(ordering):
            return ordering.moveObjectToPosition(id, position)
        else:
            return 0

    security.declareProtected(manage_properties, 'moveObjectToPosition')
    def moveObjectToPosition(self, id, position, suppress_events=False):
        """ Move specified object to absolute position.
        """
        ordering = IOrdering(self)
        if IExplicitOrdering.providedBy(ordering):
            return ordering.moveObjectToPosition(id, position, suppress_events)
        else:
            return 0

    security.declareProtected(manage_properties, 'moveObjectsByDelta')
    def moveObjectsByDelta(self, ids, delta, subset_ids=None, suppress_events=False):
        """Move specified sub-objects by delta.
        """
        ordering = IOrdering(self)
        if IExplicitOrdering.providedBy(ordering):
            return ordering.moveObjectsByDelta(ids, delta, subset_ids, suppress_events)
        else:
            return 0

    security.declareProtected(manage_properties, 'orderObjects')
    def orderObjects(self, key, reverse=None):
        """Order sub-objects by key and direction.
        """
        ordering = IOrdering(self)
        if IExplicitOrdering.providedBy(ordering):
            return ordering.orderObjects(key, reverse)
        else:
            return 0

    # Overrides for Plone-ish behaviour

    def iterkeys(self):
        return iter(self.objectIds())
        
    __iter__ = iterkeys
        
    def manage_renameObject(self, id, new_id, REQUEST=None):
        """Rename a particular sub-object without changing its position.
        """
        old_position = self.getObjectPosition(id)
        result = super(OrderedBTreeFolderBase, self).manage_renameObject(id, new_id, REQUEST)
        self.moveObjectToPosition(new_id, old_position, suppress_events=True)
        reindex = getattr(self._getOb(new_id), 'reindexObject', None)
        if reindex is not None:
            reindex(idxs=('getObjPositionInParent',))
        return result
        
    security.declareProtected(view, 'getId')
    def getId(self):
        """Ensure that getId() is protected by the View permission
        """
        return super(OrderedBTreeFolderBase, self).getId()
        
    security.declareProtected(delete_objects, 'manage_delObjects')
    def manage_delObjects(self, ids=[], REQUEST=None):
        """Delete objects with the given id, but raise Unauthorized if the 
        user does not have the "Delete objects" permission on each of them.
        """
        if isinstance(ids, basestring):
            ids = [ids]
        for id in ids:
            item = self._getOb(id)
            if not _checkPermission(permissions.DeleteObjects, item):
                raise Unauthorized, (
                    "Do not have permissions to remove this object")
        return super(OrderedBTreeFolderBase, self).manage_delObjects(ids, REQUEST=REQUEST)

        

class DefaultOrdering(object):
    """This implementation uses annotations to store the order on the object,
    and supports explicit ordering.
    """
    
    implements(IExplicitOrdering)
    adapts(IOrderableFolder)
    
    ORDER_KEY = "plone.folder.ordered.order"
    POS_KEY = "plone.folder.ordered.pos"
    
    def __init__(self, context):
        self.context = context
    
    def notifyAdded(self, id):
        """Inform the ordering implementation that an item was added
        """
        order = self._order(True)
        pos = self._pos(True)
        
        order.append(id)
        pos[id] = len(order) - 1
        
    def notifyRemoved(self, id):
        """Inform the ordering implementation that an item was removed
        """
        
        order = self._order()
        pos = self._pos()
        
        idx = pos[id]
        del order[idx]
        del pos[id]
        
    def moveObjectsByDelta(self, ids, delta, subset_ids=None, suppress_events=False):
        """Move the specified ids (a sequence) by the given delta 
        (a positive or negative number). By default, this moves the objects
        within the whole set of sub-items in the context container, but
        if subset_ids is specified, it gives a subset of ids to consider.
        
        Should return the number of objects that changed position.
        """
        
        order = self._order()
        pos = self._pos()

        min_position = 0
        
        if isinstance(ids, basestring):
            ids = (ids,)
        
        if subset_ids is None:
            subset_ids = self.idsInOrder()
        elif not isinstance(subset_ids, list):
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
            idx = 0
            
            for i in range(len(order)):
                if order[i] in subset_ids:
                    id = subset_ids[idx]
                    try:
                        order[i] = id
                        pos[id] = i
                        idx += 1
                    except KeyError:
                        raise ValueError('The object with the id "%s" does '
                                         'not exist.' % id)
        
        if not suppress_events:
            notifyContainerModified(self.context)
        
        return counter

    def moveObjectsUp(self, ids, delta=1, subset_ids=None):
        return self.moveObjectsByDelta(ids, -delta, subset_ids)

    def moveObjectsDown(self, ids, delta=1, subset_ids=None):
        return self.moveObjectsByDelta(ids, delta, subset_ids)

    def moveObjectsToTop(self, ids, subset_ids=None):
        return self.moveObjectsByDelta(ids, -len(self._order()), subset_ids )

    def moveObjectsToBottom(self, ids, subset_ids=None):
        return self.moveObjectsByDelta(ids, len(self._order()), subset_ids )

    def moveObjectToPosition(self, id, position, suppress_events=False):
        delta = position - self.getObjectPosition(id)
        if delta:
            return self.moveObjectsByDelta(id, delta, suppress_events=suppress_events)
            

    def orderObjects(self, key, reverse=None):
        """Order sub-objects by key and direction.
        """
        order = self._order()
        pos = self._pos()
        
        keyfn = lambda id: getattr(self.context._getOb(id), key)
        order.sort(None, keyfn, bool(reverse))
        for n, id in enumerate(order):
            pos[id] = n
        return -1
        
    def getObjectPosition(self, id):
        """Get the position of the given object.
        """
        pos = self._pos()
        if pos.has_key(id):
            return pos[id]
        else:
            raise ValueError('The object with the id "%s" does not exist.' % id)
    
    def idsInOrder(self):
        """Return all object ids, in the correct order
        """
        return list(self._order())
        
    # Annotation lookup with lazy creation
        
    @memoize
    def _order(self, create=False):
        annotations = IAnnotations(self.context)
        if create:
            return annotations.setdefault(self.ORDER_KEY, PersistentList())
        else:
            return annotations.get(self.ORDER_KEY, [])
        
    @memoize
    def _pos(self, create=False):
        annotations = IAnnotations(self.context)
        if create:
            return annotations.setdefault(self.POS_KEY, OLBTree())
        else:
            return annotations.get(self.POS_KEY, {})