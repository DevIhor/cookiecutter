"""Verify correct work of `_ignore` context option."""
import os
from pathlib import Path

import pytest

from cookiecutter import generate
from cookiecutter import utils

TEST_PROJECT_DIR_NAME = 'test_ignore'


@pytest.fixture
def remove_test_dir():
    """Fixture. Remove the folder that is created by the test."""
    yield
    if os.path.exists(TEST_PROJECT_DIR_NAME):
        utils.rmtree(TEST_PROJECT_DIR_NAME)


@pytest.mark.usefixtures('clean_system', 'remove_test_dir')
def test_generate_ignore_extensions():
    """Verify correct work of `_ignore` context option.

    Some files/directories should be rendered during invocation,
    some not copied.
    """
    generate.generate_files(
        context={
            'cookiecutter': {
                'repo_name': TEST_PROJECT_DIR_NAME,
                'render_test': 'I have been rendered!',
                '_ignore': [
                    '*ignored',
                    'rendered/ignored-file.yml',
                    '*.txt',
                    '{{cookiecutter.repo_name}}-rendered/README.md',
                ],
            }
        },
        repo_dir='tests/test-generate-ignore',
    )

    dir_contents = os.listdir(TEST_PROJECT_DIR_NAME)

    assert f'{TEST_PROJECT_DIR_NAME}-ignored' not in dir_contents
    assert f'{TEST_PROJECT_DIR_NAME}-rendered' in dir_contents
    assert f'rendered' in dir_contents
    assert f'README.txt' not in dir_contents

    file = Path(
        f'{TEST_PROJECT_DIR_NAME}/README.rst'
    ).read_text()
    assert 'I have been rendered!' in file

    project_rendered_dir_contents = os.listdir(
        f'{TEST_PROJECT_DIR_NAME}/{TEST_PROJECT_DIR_NAME}-rendered'
    )
    assert 'README.txt' not in project_rendered_dir_contents
    assert 'README.md' not in project_rendered_dir_contents

    file = Path(
        f'{TEST_PROJECT_DIR_NAME}/{TEST_PROJECT_DIR_NAME}-rendered/README.rst'
    ).read_text()
    assert 'I have been rendered' in file

    rendered_dir_contents = os.listdir(
        f'{TEST_PROJECT_DIR_NAME}/rendered'
    )
    assert 'ignored-file.yml' not in rendered_dir_contents
