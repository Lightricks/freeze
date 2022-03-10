from __future__ import annotations

from typing import (
    TypeVar,
    Mapping,
    Dict,
    Sequence,
    Iterator,
    overload,
    Any,
    Iterable,
    AbstractSet,
)

TYPE = TypeVar("TYPE")
KEY_TYPE = TypeVar("KEY_TYPE")
VALUE_TYPE = TypeVar("VALUE_TYPE")


class FList(Sequence[TYPE]):
    def __init__(self, iterable: Iterable[TYPE]):
        self._tuple = tuple(_frozen(value) for value in iterable)
        self._hash = hash((type(self), self._tuple))

    def __repr__(self) -> str:
        return f"FList: {self}"

    def __str__(self) -> str:
        return str(self._tuple)

    def __len__(self) -> int:
        return len(self._tuple)

    def __add__(self, other: Sequence[TYPE]) -> FList[TYPE]:
        return FList(self._tuple + tuple(other))

    def __radd__(self, other: Sequence[TYPE]) -> FList[TYPE]:
        return FList(tuple(other) + self._tuple)

    def __eq__(self, other) -> bool:
        if not isinstance(other, FList):
            return False
        return self._tuple == other._tuple

    @overload
    def __getitem__(self, idx: int) -> TYPE:
        ...

    @overload
    def __getitem__(self, s: slice) -> FList[TYPE]:
        ...

    def __getitem__(self, item):
        if isinstance(item, slice):
            return FList(self._tuple[item])
        return self._tuple[item]

    def __copy__(self) -> FList[TYPE]:
        return self

    def __deepcopy__(self, memodict={}) -> FList[TYPE]:
        return self

    def __hash__(self) -> int:
        return self._hash


class FSet(AbstractSet[TYPE]):
    def __init__(self, iterable: Iterable[TYPE]):
        self._frozenset = frozenset(_frozen(value) for value in iterable)
        self._hash = hash((type(self), self._frozenset))

    def __repr__(self) -> str:
        return f"FSet: {self}"

    def __str__(self) -> str:
        return str(set(self._frozenset))

    def __contains__(self, x: object) -> bool:
        return x in self._frozenset

    def __len__(self) -> int:
        return len(self._frozenset)

    def __iter__(self) -> Iterator[TYPE]:
        return iter(self._frozenset)

    def __copy__(self) -> FSet[TYPE]:
        return self

    def __deepcopy__(self, memodict={}) -> FSet[TYPE]:
        return self

    def __hash__(self) -> int:
        return self._hash


class FDict(Mapping[KEY_TYPE, VALUE_TYPE]):
    def __init__(self, mapping: Mapping[KEY_TYPE, VALUE_TYPE]):
        self._dict: Dict[KEY_TYPE, VALUE_TYPE] = {
            key: _frozen(value) for key, value in mapping.items()
        }
        self._hash = hash((type(self), tuple(self._dict.items())))

    def __repr__(self) -> str:
        return f"FDict: {self}"

    def __str__(self) -> str:
        return f"{str(self._dict)}"

    def __getitem__(self, k: KEY_TYPE) -> VALUE_TYPE:
        return self._dict.__getitem__(k)

    def __len__(self) -> int:
        return self._dict.__len__()

    def __iter__(self) -> Iterator[KEY_TYPE]:
        return iter(self._dict)

    def __eq__(self, other):
        if not isinstance(other, FDict):
            return False
        return self._dict == other._dict

    def __copy__(self) -> FDict[KEY_TYPE, VALUE_TYPE]:
        return self

    def __deepcopy__(self, memodict={}) -> FDict[KEY_TYPE, VALUE_TYPE]:
        return self

    def __hash__(self):
        return self._hash


@overload
def _frozen(obj: Sequence[TYPE]) -> FList[TYPE]:
    ...


@overload
def _frozen(obj: AbstractSet[TYPE]) -> FSet[TYPE]:
    ...


@overload
def _frozen(obj: Mapping[KEY_TYPE, VALUE_TYPE]) -> FDict[KEY_TYPE, VALUE_TYPE]:
    ...


@overload
def _frozen(obj: Any) -> Any:
    ...


def _frozen(obj):
    if isinstance(obj, (FList, FSet, FDict, str)):
        return obj

    if isinstance(obj, AbstractSet):
        return FSet(obj)

    if isinstance(obj, Sequence):
        return FList(obj)

    if isinstance(obj, Mapping):
        return FDict(obj)

    if _is_immutable(obj):
        return obj

    raise ValueError(f"Can't freeze object of type: {type(obj)}")


def _is_immutable(obj) -> bool:
    try:
        _ = hash(obj)
        return True
    except Exception:
        return False
