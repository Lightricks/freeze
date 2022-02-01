from copy import deepcopy
from typing import Sequence, AbstractSet, Mapping


def thawed(obj):
    if isinstance(obj, Sequence) and not isinstance(obj, str):
        return [thawed(value) for value in obj]
    elif isinstance(obj, AbstractSet):
        return {thawed(value) for value in obj}
    if isinstance(obj, Mapping):
        return {key: thawed(value) for key, value in obj.items()}

    return deepcopy(obj)
