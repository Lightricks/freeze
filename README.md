# Freeze


Freeze introduces 3 frozen collections: `FDict`, `FSet` and `FList`.
They are **immutable**, **hashable**, support **type-hinting**, and will attempt to recursively convert mutable 
collections into frozen counterparts on initialization.

### Motivation 
While there are built-in immutable versions for **list** (**tuple**) and **set** (**frozenset**), 
they have some issues:
- **tuple** can store mutable objects so its immutability is not guaranteed.
- **frozenset** can't be initialized with mutable objects.
- **dict** doesn't have a built-in immutable version at all.

### Installation
```shell
pip install frz 
```

### Usage
```python
from freeze import FDict, FList, FSet

a_mutable_dict = {
    "list": [1, 2],
    "set": {3, 4},
}

a_frozen_dict = FDict(a_mutable_dict)

print(repr(a_frozen_dict)) # FDict: {'list': FList: (1, 2), 'set': FSet: {3, 4}}
```

### How Freeze Works
Freezing a collection is achieved by following the following logic recursively:
- Immutable objects (except for collections) stay the same.
- **Mapping** (e.g. **dict**) frozen with **FDict**.
- **Sequence** (e.g. **list** or **tuple**) frozen as **FList**s.
- **AbstractSet** (e.g. **set**) frozen as **FSet**s.
- If any value in the collection can't be frozen, an exception is raised.

### Known Issues:
- Type hints are only accurate as long as no data conversion was performed.

### Future Plans:
- support for thawing frozen collections.
- support for freezing more mutable types.
