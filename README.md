# Freeze

Freeze provides frozen (immutable) implementations of the basic Python collections - **dict**, **set** and **list**.

While there are built-in immutable versions for **list** (**tuple**) and **set** (**frozenset**), 
they are not always a good replacement for their mutable counterparts:
- `tuple` can store mutable objects so its immutability is not guaranteed.
- `frozenset` will raise an exception if you try to initialize it with any mutable object.
- `dict` doesn't have a built-in immutable version.

Freeze introduces the following collections: `FDict`, `FSet` and `FList`.

They are immutable, hashable, type-hinted, and will attempt to convert mutable data to an equivalent 
immutable representation on initialization.

Freezing is achieved by following a simple logic recursively:
- Immutable objects stay the same (except for collections).
- Any **Mapping** (e.g. **dict**) is converted to an **FDict**.
- Any **AbstractSet** (e.g. **set**) is converted to an **FSet**.
- Any **Sequence** (e.g. **list** or **tuple**) is converted to an **FList**.

Attempting to initialize any Freeze collection with un-freezable objects will raise an exception.  

## Issues:
- Type hints are only accurate as long as no data conversion was performed.

## Future Plans:
- support for thawing.
- support for freezing more types.
