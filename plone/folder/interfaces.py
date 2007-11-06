from zope.interface import Interface

class IFolder(Interface):
    """Marker interface for Plone-like folders
    """
    
class IOrderableFolder(IFolder):
    """Marker interface for Plone-like folders with ordering support
    """
    
class IOrdering(Interface):
    """An adapter providing ordering operations on its context folder
    """
    
    def notifyAdded(id):
        """Inform the ordering implementation that an item was added
        """
        
    def notifyRemoved(id):
        """Inform the ordering implementation that an item was removed
        """
        
    def getObjectPosition(id):
        """Get the position of the given object.
        """
    
    def idsInOrder():
        """Return all object ids, in the correct order
        """
        
class IExplicitOrdering(IOrdering):
    """An adapter allowing explicit ordering
    """

    def moveObjectsByDelta(ids, delta, subset_ids=None, suppress_events=False):
        """Move the specified ids (a sequence, or a single string id) by the 
        given delta (a positive or negative number). By default, this moves 
        the objects within the whole set of sub-items in the context 
        container, but if subset_ids is specified, it gives a subset of ids 
        to consider.
        
        Should return the number of objects that changed position.
        """
    
    def moveObjectsUp(ids, delta=1, subset_ids=None):
        """ Move specified sub-objects up by delta in container.
        """

    def moveObjectsDown(ids, delta=1, subset_ids=None):
        """ Move specified sub-objects down by delta in container.
        """

    def moveObjectsToTop(ids, subset_ids=None):
        """ Move specified sub-objects to top of container.
        """

    def moveObjectsToBottom(ids, subset_ids=None):
        """ Move specified sub-objects to bottom of container.
        """

    def moveObjectToPosition(id, position, suppress_events=False):
        """ Move specified object to absolute position.
        """
                
    def orderObjects(key, reverse=None):
        """Order sub-objects by key and direction.
        """