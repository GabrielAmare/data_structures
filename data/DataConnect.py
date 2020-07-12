from .MetaData import DataHandler


class DataConnect(DataHandler):
    """
        DataConnect class extend the DataHandler class and provide methods to subscribe and send events
        The event manager is the class itself
    """

    def __init__(self, **kwargs):
        self.subscribes = {}
        super().__init__(**kwargs)

    def subscribe(self, ope, key, func):
        """
            For a given operation (set/get/update/delete) and a given key,
            store a function to be called each time the operation involve this key
            and call the stored list of functions with the key, val pair corresponding
        """
        assert ope in ['set', 'get', 'update', 'delete', 'append', 'remove']
        self.subscribes.setdefault(ope, {})
        self.subscribes[ope].setdefault(key, [])
        self.subscribes[ope][key].append(func)
        return lambda: self.subscribes[ope][key].remove(func)

    def onSet(self, key, val):
        for func in self.subscribes.get('set', {}).get(key, []):
            func(key, val)

    def onGet(self, key, val):
        for func in self.subscribes.get('get', {}).get(key, []):
            func(key, val)

    def onUpdate(self, **kwargs):
        for key, val in kwargs.items():
            for func in self.subscribes.get('update', {}).get(key, []):
                func(key, val)

    def onDelete(self, key, val):
        for func in self.subscribes.get('delete', {}).get(key, []):
            func(key, val)

    def onAppend(self, key, val):
        for func in self.subscribes.get('append', {}).get(key, []):
            func(key, val)

    def onRemove(self, key, val):
        for func in self.subscribes.get('remove', {}).get(key, []):
            func(key, val)
