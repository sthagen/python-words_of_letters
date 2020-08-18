# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring,unused-import,reimported
import pytest  # type: ignore

import words_of_letters.cli as cli

LANGUAGE_GRAMMAR = "tgerman"  # Sample for German, new grammar
LANGUAGE_TEXT_FILE_PATH = f"tests/fixture/text/{LANGUAGE_GRAMMAR}_title.dict"


def test_main_nok_empty_array(capsys):
    job = ['[]']
    usage_feedback = (
        'Usage: script <letter> <letter> ... <slots> [<slots> ...]\n'
        "Received (['[]']) argument vector"
    )
    assert cli.main(job) == 2
    out, err = capsys.readouterr()
    assert out.strip() == usage_feedback


def test_main_nok_too_many_slots(capsys):
    job = ["A", "B", "12"]
    usage_feedback = (
        'ERROR Only (2) characters given but requested (12) slots (12) ...'
    )
    assert cli.main(job) == 2
    out, err = capsys.readouterr()
    assert out.strip() == usage_feedback

    
def test_main_ok_init_short_option(capsys):
    wol.LANGUAGE_TEXT_FILE_PATH = LANGUAGE_TEXT_FILE_PATH
    job = ["-i"]
    usage_feedback = (
        'Initializing word databases ...'
    )
    assert cli.main(job) == 0
    out, err = capsys.readouterr()
    assert out.strip() == usage_feedback


def test_main_ok_init_long_option(capsys):
    wol.LANGUAGE_TEXT_FILE_PATH = LANGUAGE_TEXT_FILE_PATH
    job = ["--init"]
    usage_feedback = (
        'Initializing word databases ...'
    )
    assert cli.main(job) == 0
    out, err = capsys.readouterr()
    assert out.strip() == usage_feedback
