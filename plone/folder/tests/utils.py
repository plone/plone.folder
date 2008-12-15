from OFS.CopySupport import CopySource


class DummyObject(CopySource):

    def __init__(self, id, meta_type):
        self.id = id
        self.meta_type = meta_type

    def cb_isMoveable(self):
        return 1

    def manage_afterAdd(self, item, container):
        return

    def manage_beforeDelete(self, item, container):
        return

    manage_afterAdd.__five_method__ = True
    manage_beforeDelete.__five_method__ = True

    def wl_isLocked(self):
        return 0

    def __of__(self, obj):
        return self

