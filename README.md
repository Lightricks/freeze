# Freeze

This package introduces the frozen collections `FDict`, `FSet` and `FList` which are 
opinionated immutable type-hinted versions of `dict`, `set` and `list`.

The opinionated part comes into play on initialization.
Where frozen types like `frozenset` will simply raise an exception if initialized with 
mutable types, the new frozen types will try to convert these mutable types into immutable
equivalents before raising an exception.
