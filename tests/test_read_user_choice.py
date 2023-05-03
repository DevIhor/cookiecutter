"""Tests around prompting for and handling of choice variables."""
import pytest
from unittest.mock import PropertyMock, call
from cookiecutter.prompt import read_user_choice, NO_CHOICE_ELEMENT_NAME

OPTIONS = ['hello', 'world', 'foo', 'bar']
EXPECTED_PROMPT = "Select varname:"


@pytest.mark.parametrize('expected_value', OPTIONS)
def test_click_invocation(mocker, expected_value):
    """Test Terminal menu called correctly by cookiecutter.

    Test for choice type invocation.
    """
    menu = mocker.patch('cookiecutter.prompt.TerminalMenu')
    console_print = mocker.patch('cookiecutter.prompt.print')
    menu._num_lines = PropertyMock(return_value=len(OPTIONS))
    menu().chosen_menu_entry = expected_value

    assert read_user_choice('varname', OPTIONS) == expected_value
    console_print.assert_has_calls([call(EXPECTED_PROMPT)])


def test_click_invocation_with_none_choice(mocker):
    """Test Terminal menu called correctly by cookiecutter with None choice.

    Test for None choice type invocation.
    """
    menu = mocker.patch('cookiecutter.prompt.TerminalMenu')
    console_print = mocker.patch('cookiecutter.prompt.print')
    menu._num_lines = PropertyMock(return_value=len(OPTIONS)+1)
    menu().chosen_menu_entry = NO_CHOICE_ELEMENT_NAME

    assert read_user_choice('varname', OPTIONS, allow_nothing=True) == ''


def test_raise_if_options_is_not_a_non_empty_list():
    """Test function called by cookiecutter raise expected errors.

    Test for choice type invocation.
    """
    with pytest.raises(TypeError):
        read_user_choice('foo', 'NOT A LIST')

    with pytest.raises(ValueError):
        read_user_choice('foo', [])
