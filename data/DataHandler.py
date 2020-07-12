import json
import os


class DataHandler(dict):
    """
        Abstract class to store a dict 'data' as an instance field,
        provides all the methods to get, set and update this dict
        globally you can use the $.data method
        or if you want to extend the behaviour of this class in a subclass
        you can super the $._data_getall / $._data_get / $._data_set / $._data_del / $._data_update methods !

        DataConfig also support $.toDict from DictInterface

        This class also provides a $.match method, which can be used to know if the keys of data are
        matching given dict(s).
    """

    def __init__(self, **kwargs):
        f"""{self.__class__.__name__}(**kw) --> initialize the data with **kw"""
        super().__init__()
        self._data = {}
        self(**kwargs)

    def onSet(self, key, val):
        pass

    def onGet(self, key, val):
        pass

    def onUpdate(self, **kwargs):
        pass

    def onDelete(self, key, val):
        pass

    def onAppend(self, key, val):
        pass

    def onRemove(self, key, val):
        pass

    def append(self, key, val):
        assert key in self
        assert isinstance(self[key], list)
        self.onAppend(key, val)
        self[key].append(val)

    def extend(self, key, *vals):
        for val in vals:
            self.append(key, val)

    def remove(self, key, val):
        assert key in self
        assert isinstance(self[key], list)
        assert val in self[key]
        self.onRemove(key, val)
        self[key].remove(val)

    def removeall(self, key):
        l = self(key)
        while l:
            self.remove(key, l[0])

    def __call__(self, *args, **kwargs):
        """
            $(key, val)  --> set data[key] = val
            $(key, None) --> del data[key]
            $(key)       --> get data[key]
            $()          --> get the data as dict
            $(**kw)      --> update data
        """
        if len(args) == 0 and len(kwargs.keys()) == 0:
            return dict(self)
        elif len(args) == 1:
            r = self.get(args[0])
            self.onGet(args[0], r)
            return r
        elif len(args) == 2:
            if args[1] is None:
                r = self.pop(args[0], None)
                self.onDelete(args[0], r)
                return r
            else:
                self.onSet(args[0], args[1])
                self[args[0]] = args[1]
        elif len(args) > 2:
            raise Exception(f"DataHandler(...) input sign doesn't allow more than 2 unnamed arguments")
        else:
            for key, val in kwargs.items():
                self.onUpdate(**kwargs)
                if val is None:
                    if key in self:
                        self.onDelete(key, self.get(key))
                        del self[key]
                else:
                    self.onSet(key, val)
                    self[key] = val
            return self

    def toFile(self, filepath):
        json.dump(self(), open(filepath, mode='w', encoding='utf-8'))

    @classmethod
    def fromFile(cls, filepath):
        assert os.path.exists(filepath)
        return cls(**json.load(open(filepath, mode='r', encoding='utf-8')))
