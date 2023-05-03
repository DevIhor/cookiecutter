"""Tests around prompting for and handling of multiple choice variables."""
import random

import pytest
from unittest.mock import PropertyMock, call
from cookiecutter.prompt import read_multiple_user_choice, NO_CHOICE_ELEMENT_NAME

OPTIONS = ['hello', 'world', 'foo', 'bar']
EXPECTED_PROMPT = "Select varname:"
OPTIONS_CASES = [random.sample(OPTIONS, 1),
                 random.sample(OPTIONS, 2),
                 random.sample(OPTIONS, 3),
                 OPTIONS]


@pytest.mark.parametrize('expected_value', OPTIONS_CASES)
def test_click_invocation(mocker, expected_value):
    """Test Terminal menu called correctly by cookiecutter.

    Test for choice type invocation.
    """
    menu = mocker.patch('cookiecutter.prompt.TerminalMenu')
    console_print = mocker.patch('cookiecutter.prompt.print')
    menu._num_lines = PropertyMock(return_value=len(OPTIONS))
    menu().chosen_menu_entries = expected_value

    assert read_multiple_user_choice('varname', OPTIONS) == expected_value
    console_print.assert_has_calls([call(EXPECTED_PROMPT)])


def test_click_invocation_with_none_choice(mocker):
    """Test Terminal menu called correctly by cookiecutter with None choice.

    Test for None choice type invocation.
    """
    menu = mocker.patch('cookiecutter.prompt.TerminalMenu')
    menu._num_lines = PropertyMock(return_value=len(OPTIONS)+1)
    menu().chosen_menu_entries = [NO_CHOICE_ELEMENT_NAME]

    assert read_multiple_user_choice('varname', OPTIONS, allow_nothing=True) == []


def test_multiple_click_invocation_with_none_choice(mocker):
    """Test Terminal menu called correctly by cookiecutter with None choice.

    Test for None choice type invocation.
    """
    menu = mocker.patch('cookiecutter.prompt.TerminalMenu')
    menu._num_lines = PropertyMock(return_value=len(OPTIONS)+1)
    menu().chosen_menu_entries = [NO_CHOICE_ELEMENT_NAME, OPTIONS[0]]

    assert read_multiple_user_choice('varname', OPTIONS, allow_nothing=True) == [OPTIONS[0]]


def test_raise_if_options_is_not_a_non_empty_list():
    """Test function called by cookiecutter raise expected errors.

    Test for choice type invocation.
    """
    with pytest.raises(TypeError):
        read_multiple_user_choice('foo', 'NOT A LIST')

    with pytest.raises(ValueError):
        read_multiple_user_choice('foo', [])
