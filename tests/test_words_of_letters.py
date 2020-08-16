# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring,unused-import,reimported
import pytest  # type: ignore

import words_of_letters.words_of_letters as wol

LANGUAGE_GRAMMAR = "tgerman"  # Sample for German, new grammar
LANGUAGE_TEXT_FILE_PATH = f"tests/fixture/text/{LANGUAGE_GRAMMAR}_title.dict"


def test_read_mixed_case_word_text_ok_minimal():
    wol.LANGUAGE_TEXT_FILE_PATH = LANGUAGE_TEXT_FILE_PATH
    word_length = 2
    assert wol.read_mixed_case_word_text(word_length) == {'AT', 'WC', 'BH', 'WM', 'WG', 'AU'}


def test_match_gen_ok_minimal():
    letters = ["A", "T", "W"]
    word_length = 2
    n_candidates = wol.read_mixed_case_word_text(word_length)
    matches = sorted(set(wol.match_gen(n_candidates, letters)))
    assert matches == ["AT"]


def test_solve_nok_too_many_slots(capsys):
    job = ["A", "B", "12"]
    chars = len(job[:2])
    n_slots = [int(n) for n in job[2:]]
    sum_slots = sum(n_slots)
    usage_feedback = (
        f'ERROR Only ({chars}) characters given but requested ({sum_slots}) slots ({", ".join(str(n) for n in n_slots)}) ...'
    )
    assert wol.solve(job) == 2
    out, err = capsys.readouterr()
    assert out.strip() == usage_feedback


def test_solve_nok_too_many_words(capsys):
    job = ["A", "B", "C", "D", "E", "1", "1", "1", "1", "1"]
    chars = len(job[:5])
    n_slots = [int(n) for n in job[5:]]
    usage_feedback = (
        f'ERROR More than 4 slots given ({len(n_slots)})'
    )
    assert wol.solve(job) == 2
    out, err = capsys.readouterr()
    assert out.strip() == usage_feedback


def test_solve_nok_too_many_letters(capsys):
    job = ["A" for _ in range(wol.SWIPE_LETTERS + 1)]
    chars = len(job)
    usage_feedback = (
        f"ERROR More than {wol.SWIPE_LETTERS} letters given ({chars})"
    )
    assert wol.solve(job) == 2
    out, err = capsys.readouterr()
    assert out.strip() == usage_feedback


def test_solve_nok_no_slots(capsys):
    job = ["A" for _ in range(wol.SWIPE_LETTERS)]
    chars = len(job)
    usage_feedback = (
        f"ERROR ({chars}) character{'' if chars == 1 else 's'} given but requested no ({0}) slots () ..."
    )
    assert wol.solve(job) == 2
    out, err = capsys.readouterr()
    assert out.strip() == usage_feedback


def test_solve_nok_no_slots_with_warning(capsys):
    bad = "99"
    job = ["A", "B", bad]
    chars = len(job) - 1
    usage_feedback = (
        f"WARNING Ignoring character/slot ({bad}) ...\n"
        f"ERROR ({chars}) character{'' if chars == 1 else 's'} given but requested no ({0}) slots () ..."
    )
    assert wol.solve(job) == 2
    out, err = capsys.readouterr()
    assert out.strip() == usage_feedback


def test_solve_nok_no_slots_with_warnings_singular(capsys):
    bad = "99"
    job = ["A", bad, bad]
    chars = len(job) - 2
    usage_feedback = (
        f"WARNING Ignoring character/slot ({bad}) ...\n"
        f"WARNING Ignoring character/slot ({bad}) ...\n"
        f"ERROR ({chars}) character{'' if chars == 1 else 's'} given but requested no ({0}) slots () ..."
    )
    assert wol.solve(job) == 2
    out, err = capsys.readouterr()
    assert out.strip() == usage_feedback
