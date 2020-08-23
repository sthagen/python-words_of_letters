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


def test_match_gen_ok_small_wildcard_placeholders():
    letters = ["A", "T", "W"]
    places = {}
    word_length = 2
    n_candidates = wol.read_mixed_case_word_text(word_length)
    matches = sorted(set(wol.match_gen(n_candidates, letters, places)))
    assert matches == ["AT"]


def test_match_gen_ok_small_mixed_matching_placeholders():
    letters = ["A", "T", "W"]
    places = {0: "A"}
    word_length = 2
    n_candidates = wol.read_mixed_case_word_text(word_length)
    matches = sorted(set(wol.match_gen(n_candidates, letters, places)))
    assert matches == ["AT"]


def test_match_gen_ok_small_mixed_failing_placeholders():
    letters = ["A", "T", "W"]
    places = {1: "W"}
    word_length = 2
    n_candidates = wol.read_mixed_case_word_text(word_length)
    matches = sorted(set(wol.match_gen(n_candidates, letters, places)))
    assert matches == []


def test_match_gen_ok_small_complete_matching_placeholders():
    letters = ["A", "T", "W"]
    places = {0: "A", 1: "T"}
    word_length = 2
    n_candidates = wol.read_mixed_case_word_text(word_length)
    matches = sorted(set(wol.match_gen(n_candidates, letters, places)))
    assert matches == ["AT"]


def test_match_gen_ok_small_complete_failing_placeholders():
    letters = ["A", "T", "W"]
    places = {0: "A", 1: "W"}
    word_length = 2
    n_candidates = wol.read_mixed_case_word_text(word_length)
    matches = sorted(set(wol.match_gen(n_candidates, letters, places)))
    assert matches == []


def test_display_letters_ok_minimal(capsys):
    letters = ["A", "B"]
    screen_display = (
        f"{len(letters)} Letters available:\n\n"
        f"    {' '.join(letters)}"
    )
    assert wol.display_letters(letters) is None
    out, err = capsys.readouterr()
    assert out.strip() == screen_display


def test_display_letters_ok_pictures(capsys):
    letters = ["A" for _ in range(wol.PICTURE_LETTERS)]
    screen_display = (
        f"{len(letters)} Letters available:\n\n"
        f"    {' '.join(letters[:6])}\n"
        f"    {' '.join(letters[6:])}"
    )
    assert wol.display_letters(letters) is None
    out, err = capsys.readouterr()
    assert out.strip() == screen_display


def test_display_letters_ok_swipe(capsys):
    letters = ["A" for _ in range(wol.SWIPE_LETTERS)]
    screen_display = (
        f"{len(letters)} Letters available:\n\n"
        f"    {' '.join(letters[:5])}\n"
        f"    {' '.join(letters[5:10])}\n"
        f"    {' '.join(letters[10:15])}\n"
        f"    {' '.join(letters[15:20])}\n"
        f"    {' '.join(letters[20:])}"
    )
    assert wol.display_letters(letters) is None
    out, err = capsys.readouterr()
    assert out.strip() == screen_display


def test_parse_ok_empty():
    job = []
    letters, n_slots, placeholders, errors, warnings = wol.parse(job)
    assert letters == []
    assert n_slots == []
    assert placeholders == {}
    assert errors == []
    assert warnings == []


def test_parse_ok_minimal():
    job = ["A", "T", "2"]
    letters, n_slots, placeholders, errors, warnings = wol.parse(job)
    assert letters == job[:2]
    assert n_slots == [int(job[-1])]
    assert placeholders == {}
    assert errors == []
    assert warnings == []


def test_parse_ok_minimal_wildcard_placeholders():
    job = ["A", "T", "2", "_", "_"]
    letters, n_slots, placeholders, errors, warnings = wol.parse(job)
    assert letters == job[:2]
    assert n_slots == [int(job[2])]
    assert placeholders == {int(job[2]): job[2+1:]}
    assert errors == []
    assert warnings == []


def test_parse_ok_small_mixed_placeholders():
    job = ["A", "B", "T", "3", "A", "_", "_"]
    letters, n_slots, placeholders, errors, warnings = wol.parse(job)
    assert letters == job[:3]
    assert n_slots == [int(job[3])]
    assert placeholders == {int(job[3]): job[3+1:]}
    assert errors == []
    assert warnings == []


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
