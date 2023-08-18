
import importlib
import json
import datetime
import decimal
from typing import Any, Union
from collections.abc import Iterable

class NullMeta(type):

    def __repr__(self):
        return 'null'

    def __str__(self):
        return 'null'

    def __bool__(self):
        return False
    
    def __setattr__(self, __name: str, __value: Any) -> None:
        raise TypeError('Cannot set attribute on null')

    def __getattr__(self, attr):
        return self
    
    def __getitem__(self, __key: Any) -> Any:
        return self

class null(metaclass=NullMeta):
    pass

def dumps(*args, **kws):
    kws['cls'] = kws.get('cls', JSONEncoder)
    return json.dumps(*args, **kws)

def loads(*args, **kws):
    return json.loads(*args, **kws)

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            if '.' in str(obj):
                return float(obj)
            else:
                return int(obj)
        elif isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, set):
            return list(obj)
        elif obj is null:
            return None
        else:
            return super(JSONEncoder, self).default(obj)
        
class SoftyList(list):

    def __repr__(self):
        return f'softy({super().__repr__()})'

    def __get_pydantic_core_schema__(self):
        pydantic_core = importlib.import_module('pydantic_core')
        return pydantic_core.core_schema.any_schema()

    def __getitem__(self, __ix: int):
        try:
            item = super().__getitem__(__ix)
        except IndexError:
            return null
        if isinstance(__ix, slice):
            return soften(item)
        else:
            return item

    def __setattr__(self, __name: str, __value: Any) -> None:
        return super().__setattr__(__name, soften(__value))
    
    def __setitem__(self, __key, __value) -> None:
        if not isinstance(__key, int):
            raise TypeError(f'List indices must be integers')
        elif __key > len(self):
            raise IndexError(f'Cannot set list index out of range: {__key}')
        elif __key == len(self):
            return self.append(__value)
        return super().__setitem__(__key, soften(__value))

    def append(self, item):
        return super().append(soften(item))
    
    def extend(self, __iterable: Iterable) -> None:
        return super().extend(soften(list(__iterable)))

class SoftyMap(dict):

    def __repr__(self):
        return f'softy({super().__repr__()})'

    def __get_pydantic_core_schema__(self):
        pydantic_core = importlib.import_module('pydantic_core')
        return pydantic_core.core_schema.any_schema()

    def __getattr__(self, attr):
        return self.get(attr, null)

    def __getitem__(self, __key: Any) -> Any:
        if __key in self:
            return super().__getitem__(__key)
        else:
            return null

    def __setattr__(self, __name: str, __value: Any) -> None:
        return super().__setitem__(__name, soften(__value))
    
    def __setitem__(self, __key, __value) -> None:
        return super().__setitem__(__key, soften(__value))

def soften(item: Union[dict, list]):
    
    # recursive softening
    if isinstance(item, dict):
        result = SoftyMap()
        for key, value in item.items():
            result[key] = soften(value)
        return result
    elif isinstance(item, list):
        return SoftyList(soften(sv) for sv in item)
    else:
        return item

def harden(item: Union[dict, list]):

    # recursive hardening
    if isinstance(item, dict):
        result = dict(item)
        for key, value in result.items():
            result[key] = harden(value)
        return result
    elif isinstance(item, list):
        return [harden(sv) for sv in item]
    else:
        return item

def isnull(item: Any) -> bool:
    return item is null