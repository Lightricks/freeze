from copy import copy, deepcopy
from dataclasses import dataclass

import pytest

from src.freeze.freeze import FDict, FList, FSet


class TestFList:
    def test_init(self):
        frozen_list = FList([1, "a"])

        assert len(frozen_list) == 2
        assert frozen_list[0] == 1
        assert frozen_list[1] == "a"

    def test_mutable_init(self):
        frozen_list = FList([[1, [2]], {3, (4,)}, {5: [6]}])

        assert len(frozen_list) == 3
        assert frozen_list[0] == FList([1, [2]])
        assert frozen_list[1] == FSet({3, (4,)})
        assert frozen_list[2] == FDict({5: [6]})

    def test_raise_on_mutable_class_init(self):
        @dataclass
        class Foo:
            bar: int = 0

        with pytest.raises(ValueError):
            _ = FList([Foo()])

    def test_frozen_dataclass_init(self):
        @dataclass(frozen=True)
        class Foo:
            bar: int = 0

        _ = FList([Foo()])

    def test_equals(self):
        frozen_list = FList([1, 2, 3])
        same = FList([1, 2, 3])
        different = FList([1, 2, 4])

        assert frozen_list == same
        assert frozen_list != different

    def test_add(self):
        added_list = FList([1, 2]) + [3, 4]
        assert added_list == FList([1, 2, 3, 4])

    def test_radd(self):
        added_list = [1, 2] + FList([3, 4])
        assert added_list == FList([1, 2, 3, 4])

    def test_get_index(self):
        frozen_list = FList([1, 2, 3])

        assert frozen_list[0] == 1
        assert frozen_list[1] == 2
        assert frozen_list[2] == 3

    def test_get_slice(self):
        frozen_list = FList([1, 2, 3])

        assert frozen_list[0:2] == FList([1, 2])
        assert frozen_list[1:2] == FList([2])

    def test_copy(self):
        frozen_list = FList([1, 2, 3])

        assert copy(frozen_list) is frozen_list
        assert deepcopy(frozen_list) is frozen_list

    def test_hash(self):
        frozen_list = FList([1, 2, 3])
        same = FList([1, 2, 3])
        different = FList([1, 2, 4])

        assert hash(frozen_list) == hash(same)
        assert hash(frozen_list) != hash(different)


class TestFSet:
    def test_init(self):
        frozen_set = FSet([1, "a"])

        assert len(frozen_set) == 2
        assert 1 in frozen_set
        assert "a" in frozen_set

    def test_mutable_init(self):
        frozen_set = FSet([(1, (1,)), frozenset([2, 3])])

        assert len(frozen_set) == 2
        assert FList((1, (1,))) in frozen_set
        assert FSet([2, 3]) in frozen_set

    def test_frozen_dataclass_init(self):
        @dataclass(frozen=True)
        class Foo:
            bar: int = 0

        _ = FSet({Foo()})

    def test_equals(self):
        frozen_set = FSet([1, 2, 3])
        same = FSet([1, 2, 3])
        different = FSet([1, 2, 4])

        assert frozen_set == same
        assert frozen_set != different

    def test_or(self):
        or_set = FSet([1, 2]) | {3, 4}
        assert or_set == FSet({1, 2, 3, 4})

    def test_ror(self):
        or_set = {3, 4} | FSet([1, 2])
        assert or_set == FSet({1, 2, 3, 4})

    def test_and(self):
        and_set = FSet([1, 2, 3]) & {3, 4}
        assert and_set == FSet({3})

    def test_rand(self):
        and_set = {3, 4} & FSet([1, 2, 3])
        assert and_set == FSet({3})

    def test_copy(self):
        frozen_set = FSet([1, 2, 3])

        assert copy(frozen_set) is frozen_set
        assert deepcopy(frozen_set) is frozen_set

    def test_hash(self):
        frozen_set = FSet([1, 2, 3])
        same = FSet([1, 2, 3])
        different = FSet([1, 2, 4])

        assert hash(frozen_set) == hash(same)
        assert hash(frozen_set) != hash(different)


class TestFDict:
    def test_init(self):
        frozen_dict = FDict({1: 2, "3": "4"})

        assert len(frozen_dict) == 2
        assert frozen_dict[1] == 2
        assert frozen_dict["3"] == "4"

    def test_mutable_init(self):
        frozen_dict = FDict({1: [2], "3": {"4": ["5"]}})

        assert len(frozen_dict) == 2
        assert frozen_dict[1] == FList([2])
        assert frozen_dict["3"] == FDict({"4": FList(["5"])})

    def test_frozen_dataclass_init(self):
        @dataclass(frozen=True)
        class Foo:
            bar: int = 0

        _ = FDict({Foo(): 3})

    def test_raise_on_mutable_class_init(self):
        @dataclass
        class Foo:
            bar: int = 0

        with pytest.raises(ValueError):
            _ = FDict({3: Foo()})

    def test_iteration(self):
        frozen_dict = FDict({"a": 1, "b": 2})

        assert list(iter(frozen_dict)) == ["a", "b"]

    def test_equals(self):
        frozen_dict = FDict({"a": 1, "b": 2})
        same = FDict({"a": 1, "b": 2})
        different = FDict({"c": 3, "d": 4})

        assert frozen_dict == same
        assert frozen_dict != different

    def test_copy(self):
        frozen_dict = FDict({"a": 1, "b": 2})

        assert copy(frozen_dict) is frozen_dict
        assert deepcopy(frozen_dict) is frozen_dict

    def test_hash(self):
        frozen_dict = FDict({"a": 1, "b": 2})
        same = FDict({"a": 1, "b": 2})
        different = FDict({"c": 3, "d": 4})

        assert hash(frozen_dict) == hash(same)
        assert hash(frozen_dict) != hash(different)
