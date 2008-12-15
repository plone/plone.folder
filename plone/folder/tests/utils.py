

class DummyObject(object):

    def __init__(self, id, meta_type):
        self.id = id
        self.meta_type = meta_type

    def __of__(self, obj):
        return self

