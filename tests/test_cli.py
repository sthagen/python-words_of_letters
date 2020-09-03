# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring,unused-import,reimported
import pytest  # type: ignore

import words_of_letters.cli as cli
import words_of_letters.words_of_letters as wol

LANGUAGE_GRAMMAR = "tgerman"  # Sample for German, new grammar
LANGUAGE_TEXT_FILE_PATH = f"tests/fixture/text/{LANGUAGE_GRAMMAR}_title.dict"
DB_BASE_PATH = f"tests/fixture/db/{LANGUAGE_GRAMMAR}_dict_"


def test_main_nok_empty_array(capsys):
    job = ['[]']
    usage_feedback = (
        'Usage: script <letters> ... <slots> [<placeholders> <slots> ...]\n'
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


def test_main_nok_too_many_placeholders(capsys):
    job = ["A", "B", "T", "3", "A", "_", "_", "_"]
    usage_feedback = (
        "ERROR 1 too many placeholders (['a', '_', '_', '_']) for slot 3"
    )
    assert cli.main(job) == 2
    out, err = capsys.readouterr()
    assert out.strip() == usage_feedback


def test_main_nok_too_many_placeholders_same_size_slots(capsys):
    job = ["A", "B", "A", "B", "2", "A", "_", "2", "_", "B"]
    usage_feedback = (
        "ERROR 1 too many placeholders (['a', '_', '_']) for slot 2"
    )
    assert cli.main(job) == 2
    out, err = capsys.readouterr()
    assert out.strip() == usage_feedback


def test_main_ok_init_short_option(capsys):
    wol.LANGUAGE_TEXT_FILE_PATH = LANGUAGE_TEXT_FILE_PATH
    job = ["-i", 2, 2]
    usage_feedback = (
        'Initializing word databases for sizes in [2, 2] ...'
    )
    assert cli.main(job) == 0
    out, err = capsys.readouterr()
    assert out.strip() == usage_feedback


def test_main_ok_init_long_option(capsys):
    wol.LANGUAGE_TEXT_FILE_PATH = LANGUAGE_TEXT_FILE_PATH
    job = ["--init", 2, 3]
    usage_feedback = (
        'Initializing word databases for sizes in [2, 3] ...'
    )
    assert cli.main(job) == 0
    out, err = capsys.readouterr()
    assert out.strip() == usage_feedback


def test_main_ok_minimal_with_placeholders(capsys):
    wol.LANGUAGE_TEXT_FILE_PATH = LANGUAGE_TEXT_FILE_PATH
    wol.DB_BASE_PATH = DB_BASE_PATH
    word_length = 2
    job = ["a", "t", f"{word_length}", "a", "_"]
    screen_display = (
        '2 Letters available:\n'
        '\n'
        '    a t\n'
        '\n'
        'Found 1 candidates of length(2) from letters(a t):\n'
        '\n'
        '    0) at'
    )
    assert cli.main(job) == 0
    out, err = capsys.readouterr()
    assert out.strip() == screen_display


def test_main_ok_minimal_with_placeholders_stanzas(capsys):
    wol.LANGUAGE_TEXT_FILE_PATH = LANGUAGE_TEXT_FILE_PATH
    wol.DB_BASE_PATH = DB_BASE_PATH
    word_length = 2
    job = ["at", f"{word_length}", "a", "_"]
    screen_display = (
        '2 Letters available:\n'
        '\n'
        '    a t\n'
        '\n'
        'Found 1 candidates of length(2) from letters(a t):\n'
        '\n'
        '    0) at'
    )
    assert cli.main(job) == 0
    out, err = capsys.readouterr()
    assert out.strip() == screen_display
