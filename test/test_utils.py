import pytest
from utils.config import read_stack_file

def test_read_stack_file():
    """ Test read default tech stacks data file """

    target_stacks = read_stack_file()

    # Check if Python is in the file and Java is not.
    # NOTE: These checks create a depdency between
    # this test and the default tech stack files.
    # If we remove Python (or add Java) into this file,
    # this test MUST BE updated.
    assert "Python" in target_stacks
    assert "Java" not in target_stacks

def test_non_existing_stack_file():
    """ Test try to read a non-existing file """

    with pytest.raises(FileNotFoundError):
        read_stack_file("dummy.dat")