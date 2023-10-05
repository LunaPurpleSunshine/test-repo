from datetime import datetime

import pytest
from hypothesis import assume, given
from hypothesis import strategies as st

from randopy import rando


@pytest.mark.skip(reason="Too slow")
class TestCustomNamer:
    @given(
        stem=st.text(min_size=1, alphabet=st.characters(categories=["L", "N", "S"])),
        suffix=st.text(
            min_size=1, max_size=10, alphabet=st.characters(categories=["L", "N", "S"])
        ),
    )
    def test_expected_input(self, stem: str, suffix: str):
        assume(all([stem, suffix]))

        input_name = f"{stem}.{suffix}"
        expected_output = f"{stem}.{datetime.now().date()}.{suffix}"

        result = rando.custom_namer(input_name)

        assert result == expected_output

    @given(
        stem=st.text(
            min_size=1,
            alphabet=st.characters(categories=["L", "N", "S"]),
        ),
        suffix=st.text(
            min_size=1,
            max_size=10,
            alphabet=st.characters(categories=["L", "N", "S"]),
        ),
    )
    def test_multiple_suffixes(self, stem, suffix):
        assume(all([stem, suffix]))

        input_name = f"{stem}.{suffix}.{suffix}"
        expected_output = f"{stem}.{suffix}.{datetime.now().date()}.{suffix}"

        result = rando.custom_namer(input_name)

        assert result == expected_output

    @given(name=st.integers() | st.booleans())
    def test_not_str(self, name):
        with pytest.raises(TypeError):
            rando.custom_namer(name)

    @given(
        suffix=st.text(
            min_size=1, max_size=10, alphabet=st.characters(categories=["L", "N"])
        )
    )
    def test_invalid_input_stem(self, suffix):
        name = f".{suffix}"
        with pytest.raises(ValueError):
            rando.custom_namer(name)

    @given(stem=st.text(min_size=1, alphabet=st.characters(categories=["L", "N"])))
    def test_invalid_input_suffix(self, stem):
        name = f"{stem}"
        with pytest.raises(ValueError):
            rando.custom_namer(name)

    @given(name=st.text(min_size=1))
    def test_invalid_input(self, name):
        assume("." not in name)
        with pytest.raises(ValueError):
            rando.custom_namer(name)


class TestRollD6:
    @given(test_count=st.integers(min_value=0))
    def test_count(self, test_count: int):
        result = rando.roll_d6(count=test_count)
        assert len(result) == test_count
