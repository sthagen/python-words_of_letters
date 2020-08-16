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
    n_slots = [int(n) for n in job[-1:]]
    sum_slots = sum(n_slots)
    usage_feedback = (
        f'ERROR Only ({chars}) characters given but requested ({sum_slots}) slots ({", ".join(str(n) for n in n_slots)}) ...'
    )
    assert wol.solve(job) == 2
    out, err = capsys.readouterr()
    assert out.strip() == usage_feedback
