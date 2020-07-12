class Array(list):
    def __init__(self, *items):
        if len(items) == 1 and hasattr(items[0], '__iter__'):
            items = items[0]
        list.__init__(self)
        self.extend(items)

    def apply(self, func):
        for item in self:
            func(item)
        return self

    def flat(self):
        r = Array()
        self.apply(r.extend)
        return r

    def flatmap(self, func):
        return self.map(func).flat()

    def map(self, func):
        r = Array()
        r.extend(func(element) for element in self)
        return r

    def mapenum(self, func):
        r = Array()
        r.extend(func(index, element) for index, element in enumerate(self))
        return r

    def filter(self, func):
        r = Array()
        r.extend(element for element in self if not func(element))
        return r

    def keep(self, func):
        r = Array()
        r.extend(element for element in self if func(element))
        return r

    def sort(self, key, reverse=False):
        if len(self) > 1:
            r = Array()
            r.extend(sorted(self, key=key, reverse=reverse))
            return r
        else:
            return self

    def last(self, func=None):
        if func is None:
            for element in reversed(self):
                return element
        else:
            return self.keep(func).last()

    def first(self, func=None):
        if func is None:
            for element in self:
                return element
        else:
            return self.keep(func).first()

    def dgroup(self, func):
        group_keys = []
        group_vals = Array()
        for val in self:
            key = func(val)
            if key not in group_keys:
                group_keys.append(key)
                group_vals.append(Array())
                group_vals[-1].append(val)
            else:
                index = group_keys.index(key)
                group_vals[index].append(val)
        return dict(zip(group_keys, group_vals))

    def group(self, func):
        group_keys = []
        group_vals = Array()
        for val in self:
            key = func(val)
            if key not in group_keys:
                group_keys.append(key)
                group_vals.append(Array())
                group_vals[-1].append(val)
            else:
                index = group_keys.index(key)
                group_vals[index].append(val)
        return group_vals

    @classmethod
    def pipe(cls, curr, func):
        r = cls()
        while curr:
            r.append(curr)
            curr = func(curr)
        return r

    def max(self, default=0):
        length = len(self)
        if length == 0:
            return default
        elif length == 1:
            return self[0]
        else:
            return max(self)

    def sum(self, default=0):
        length = len(self)
        if length == 0:
            return default
        elif length == 1:
            return self[0]
        else:
            return sum(self)

    def len(self) -> int:
        return len(self)

    def zip(self, *iterables):
        if iterables:
            return ZipArray(self, *iterables)
        else:
            r = ZipArray()
            r.extend((item,) for item in self)
            return r

    def dict(self):
        return dict(self)

    def set(self):
        return set(self)

    def __add__(self, other):
        r = Array()
        r.extend(self)
        r.extend(other)
        return r
