# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring,unused-import,reimported
import pytest  # type: ignore

import words_of_letters.cli as cli


def test_main_nok_empty_array(capsys):
    job = ['[]']
    usage_feedback = (
        'Usage: sys.args[0] <letter> <letter> ... <slots> [<slots> ...]\n'
        "Received (['[]']) argument vector"
    )
    assert cli.main(job) is 2
    out, err = capsys.readouterr()
    assert out.strip() == usage_feedback


def test_main_nok_too_many_slots(capsys):
    job = ["A", "B", 12]
    usage_feedback = (
        'ERROR Only (2) characters given but requested (12) slots (12) ...\n'
    )
    assert cli.main(job) is 2
    out, err = capsys.readouterr()
    assert out.strip() == usage_feedback
