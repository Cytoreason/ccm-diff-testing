import pytest

from sample_pkg.sample import Sample


@pytest.mark.unittest
def test_something():
    did_something = Sample().do_something(input1='a')
    assert did_something is False


@pytest.mark.integration
def test_something_int():
    did_something = Sample().do_something(input1='a')
    assert did_something is False
