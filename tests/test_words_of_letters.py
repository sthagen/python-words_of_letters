# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring,unused-import,reimported
import pytest  # type: ignore

import words_of_letters.words_of_letters as wol

LANGUAGE_GRAMMAR = "tgerman"  # Sample for German, new grammar
LANGUAGE_TEXT_FILE_PATH = f"tests/fixture/text/{LANGUAGE_GRAMMAR}_title.dict"
DB_BASE_PATH = f"tests/fixture/db/{LANGUAGE_GRAMMAR}_dict_"


def test_read_mixed_case_word_text_ok_minimal():
    wol.LANGUAGE_TEXT_FILE_PATH = LANGUAGE_TEXT_FILE_PATH
    word_length = 2
    assert wol.read_mixed_case_word_text(word_length) == {'at', 'wc', 'bh', 'wm', 'wg', 'au'}


def test_dump_ok_minimal():
    wol.LANGUAGE_TEXT_FILE_PATH = LANGUAGE_TEXT_FILE_PATH
    wol.DB_BASE_PATH = DB_BASE_PATH
    assert wol.dump({'at', 'wc', 'bh', 'wm', 'wg', 'au'}) is None


def test_load_ok_minimal():
    wol.LANGUAGE_TEXT_FILE_PATH = LANGUAGE_TEXT_FILE_PATH
    wol.DB_BASE_PATH = DB_BASE_PATH
    word_length = 2
    assert set(wol.load(word_length, {"a"})) == {'at', 'au'}


def test_display_solutions_ok_minimal(capsys):
    letters = ["A", "B"]
    matches = ["AB"]
    slots = 2
    screen_display = (
        'Found 1 candidates of length(2) from letters(A B):\n'
        '\n'
        '    0) AB'
    )
    assert wol.display_solutions(letters, matches, slots) is None
    out, err = capsys.readouterr()
    assert out.strip() == screen_display


def test_match_gen_ok_minimal():
    letters = ["a", "t", "w"]
    word_length = 2
    n_candidates = wol.read_mixed_case_word_text(word_length)
    matches = sorted(set(wol.match_gen(n_candidates, letters)))
    assert matches == ["at"]


def test_match_gen_ok_small_wildcard_placeholders():
    letters = ["a", "t", "w"]
    places = {}
    word_length = 2
    n_candidates = wol.read_mixed_case_word_text(word_length)
    matches = sorted(set(wol.match_gen(n_candidates, letters, places)))
    assert matches == ["at"]


def test_match_gen_ok_small_mixed_matching_placeholders():
    letters = ["a", "t", "w"]
    places = {0: "a"}
    word_length = 2
    n_candidates = wol.read_mixed_case_word_text(word_length)
    matches = sorted(set(wol.match_gen(n_candidates, letters, places)))
    assert matches == ["at"]


def test_match_gen_ok_small_mixed_failing_placeholders():
    letters = ["A", "T", "W"]
    places = {1: "W"}
    word_length = 2
    n_candidates = wol.read_mixed_case_word_text(word_length)
    matches = sorted(set(wol.match_gen(n_candidates, letters, places)))
    assert matches == []


def test_match_gen_ok_small_complete_matching_placeholders():
    letters = ["a", "t", "w"]
    places = {0: "a", 1: "t"}
    word_length = 2
    n_candidates = wol.read_mixed_case_word_text(word_length)
    matches = sorted(set(wol.match_gen(n_candidates, letters, places)))
    assert matches == ["at"]


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
    stanzas = [["A", "A", "A", "A", "A", "A"], ["A", "A", "A", "A", "A", "A"]]
    n_letters = sum(len(ch) for ch in stanzas)
    screen_display = (
        f"{n_letters} Letters available:\n\n"
        "    A A A A A A\n"
        "    A A A A A A"
    )
    assert wol.display_stanzas(stanzas) is None
    out, err = capsys.readouterr()
    assert out.strip() == screen_display.strip()


def test_display_letters_ok_swipe(capsys):
    stanzas = [
        ["A", "A", "A", "A", "A"], ["A", "A", "A", "A", "A"],
        ["A", "A", "A", "A", "A"], ["A", "A", "A", "A", "A"],
        ["A", "A", "A", "A", "A"], ["A", "A", "A", "A", "A"],
    ]
    n_letters = sum(len(ch) for ch in stanzas)
    screen_display = (
        f"{n_letters} Letters available:\n\n"
        "    A A A A A\n"
        "    A A A A A\n"
        "    A A A A A\n"
        "    A A A A A\n"
        "    A A A A A\n"
        "    A A A A A\n"
    )
    assert wol.display_stanzas(stanzas) is None
    out, err = capsys.readouterr()
    assert out.strip() == screen_display.strip()


def test_parse_nok_empty():
    job = []
    letters, stanzas, n_slots, placeholders, errors, warnings = wol.parse(job)
    assert letters == []
    assert stanzas == []
    assert n_slots == []
    assert placeholders == {}
    assert errors == [
        'Usage: script <letters> ... <slots> [<placeholders> <slots> ...]\n'
        'Received ([]) argument vector'
    ]
    assert warnings == []


def test_parse_ok_minimal():
    job = ["A", "T", "2"]
    letters, stanzas, n_slots, placeholders, errors, warnings = wol.parse(job)
    assert letters == [ch.lower() for ch in job[:2]]
    assert stanzas == []
    assert n_slots == [int(job[-1])]
    assert placeholders == {}
    assert errors == []
    assert warnings == []


def test_parse_ok_minimal_stanzas():
    job = ["AT", "AT", "2"]
    letters, stanzas, n_slots, placeholders, errors, warnings = wol.parse(job)
    assert letters == ['a', 't', 'a', 't']
    assert stanzas == [['a', 't'], ['a', 't']]
    assert n_slots == [int(job[-1])]
    assert placeholders == {}
    assert errors == []
    assert warnings == []


def test_parse_ok_minimal_ignored_placeholder():
    job = ["A", "_", "T", "2"]
    letters, stanzas, n_slots, placeholders, errors, warnings = wol.parse(job)
    assert letters == [ch.lower() for ch in job[:3:2]]
    assert stanzas == []
    assert n_slots == [int(job[-1])]
    assert placeholders == {}
    assert errors == []
    assert warnings == ['WARNING Ignoring placeholder as letter (_) ...']


def test_parse_ok_minimal_wildcard_placeholders():
    job = ["A", "T", "2", "_", "_"]
    letters, stanzas, n_slots, placeholders, errors, warnings = wol.parse(job)
    assert letters == [ch.lower() for ch in job[:2]]
    assert stanzas == []
    assert n_slots == [int(job[2])]
    assert placeholders == {int(job[2]): [ch.lower() for ch in job[2+1:]]}
    assert errors == []
    assert warnings == []


def test_parse_ok_small_mixed_placeholders():
    job = ["A", "B", "T", "3", "A", "_", "_"]
    letters, stanzas, n_slots, placeholders, errors, warnings = wol.parse(job)
    assert letters == [ch.lower() for ch in job[:3]]
    assert stanzas == []
    assert n_slots == [int(job[3])]
    assert placeholders == {int(job[3]): [ch.lower() for ch in job[3+1:]]}
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
    job = ["A", "B", "C", "D", "E"]
    job.extend(["1"] * (wol.MAX_SLOTS + 1))
    n_slots = [int(n) for n in job[5:]]
    usage_feedback = (
        f'ERROR More than {wol.MAX_SLOTS} slots given ({len(n_slots)})'
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
        f"WARNING Ignoring characters/slot ({bad}) ...\n"
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
        f"WARNING Ignoring characters/slot ({bad}) ...\n"
        f"WARNING Ignoring characters/slot ({bad}) ...\n"
        f"ERROR ({chars}) character{'' if chars == 1 else 's'} given but requested no ({0}) slots () ..."
    )
    assert wol.solve(job) == 2
    out, err = capsys.readouterr()
    assert out.strip() == usage_feedback


def test_solve_ok_minimal(capsys):
    wol.LANGUAGE_TEXT_FILE_PATH = LANGUAGE_TEXT_FILE_PATH
    wol.DB_BASE_PATH = DB_BASE_PATH
    word_length = 2
    job = ["a", "t", f"{word_length}"]
    screen_display = (
        '2 Letters available:\n'
        '\n'
        '    a t\n'
        '\n'
        'Found 1 candidates of length(2) from letters(a t):\n'
        '\n'
        '    0) at'
    )
    assert wol.solve(job) == 0
    out, err = capsys.readouterr()
    assert out.strip() == screen_display


def test_solve_ok_minimal_with_placeholders(capsys):
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
    assert wol.solve(job) == 0
    out, err = capsys.readouterr()
    assert out.strip() == screen_display
