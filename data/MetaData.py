from abc import ABC, abstractmethod

from .DataHandler import DataHandler


class DictInterface(ABC):
    @classmethod
    @abstractmethod
    def fromDict(cls, d: dict):
        pass

    @abstractmethod
    def toDict(self) -> dict:
        pass

    @staticmethod
    def parse(A, asKey=False):
        if isinstance(A, (bool, int, float, str)):
            return A
        elif asKey:
            raise Exception(f"Can't parse {A.__class__.__name__} as a key in DictInterface context")
        elif isinstance(A, (list, tuple, set)):
            return list(DictInterface.parse(B) for B in A)
        elif isinstance(A, dict):
            r = {}
            for key, val in A.items():
                try:
                    r[DictInterface.parse(key, asKey=True)] = DictInterface.parse(val)
                except:
                    pass
            return r
        elif isinstance(A, DictInterface):
            return A.toDict()
        else:
            raise Exception(f"Can't parse {A.__class__.__name__} objects !")

    @classmethod
    def __subclasshook__(cls, C):
        if cls is DictInterface:
            for B in C.__mro__:
                if "toDict" in B.__dict__ or "fromDict" in B.__dict__:
                    return True
        return NotImplemented


class DataConfig:
    """
        Abstract class to store a dict 'data' as an instance field,
        provides all the methods to get, set and update this dict
        globally you can use the $.data.__call__ method
        or if you want to extend the behaviour of this class in a subclass

        DataConfig also support $.toDict from DictInterface

        This class also provides a $.match method, which can be used to know if the keys of data are
        matching given dict(s).
    """

    def __init__(self, **kwargs):
        f"""{self.__class__.__name__}(**kw) --> initialize the data with **kw"""
        self.data = DataHandler(**kwargs)

    def match(self, *args, **kwargs):
        """
            $.match(cnf1, cnf2, ...) --> find any match for the given cnfs, if cnf is a function call the function on self and use the return value as a validation
            $.match(**cnf)           --> check that all the (key: val) in cnf are in $.data

            The match method verify that each item of a given dict is also present in the data.
            --> if item_from_given == (val1, key1) and item_from_data == (val2, key2)
            --> then it checks that (key1 == key2) and (val1 == val2)
        """
        if len(args):
            return any(self.match(**arg) if isinstance(arg, dict) else arg(self) if hasattr(arg, '__call__') else False
                       for arg in args
                       )
        else:
            return all(self.data(key) == val for key, val in kwargs.items())

    def toDict(self):
        return DictInterface.parse(self.data)


class MetaConfig:
    """
        The behaviour of MetaConfig Abstract Class is the same as DataConfig Abstract Class,
        the only difference if that the dict is named 'meta' in place of 'data'.
        PS: DataConfig and MetaConfig are made compatible, so they can both be super of the same subclass.
    """

    def __init__(self, **kwargs):
        self.meta = DataHandler(**kwargs)

    def toDict(self):
        return DictInterface.parse(self.meta)
