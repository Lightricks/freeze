# Freeze

Freeze provides frozen (immutable) implementations of the basic Python collections - `dict`, `set` and `list`.

While there are built-in immutable versions for `list` (`tuple`) and `set` (`frozenset`), 
they are not always a good drop-in replacement for their mutable counterparts.
`tuple` can store mutable objects so its immutability is not guaranteed.
`frozenset` will raise an exception if you try to initialize it with any mutable object.
`dict` doesn't have a built-in immutable version.

Enter `FDict`, `FSet` and `FList`, which are immutable, hashable, type-hinted, and will attempt to store even 
mutable data whenever an equivalent immutable representation is available.

Freezing is achieved by following a simple logic recursively:
- Immutable objects stay the same.
- Any `Mapping` (e.g. `dict`) is stored as an `FDict`.
- Any `AbstractSet` (e.g. `set`) is stored as an `FSet`.
- Any `Sequence`(e.g. `list` or `tuple`) is stored as an `FList`.

Attempting to initialize any of the frozen collections with objects that don't have an obvious immutable 
representation (e.g. most classes) will raise an exception.  

Issues:
- Type hints are only accurate when the stored data did not require freezing.

Future Plans:
- add support for thawing (converting the object back into its original form).
- add support for freezing classes when possible.