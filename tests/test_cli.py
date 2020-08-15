# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring,unused-import,reimported
import pytest  # type: ignore

import words_of_letters.cli as cli


def test_main_ok_empty_array(capsys):
    job = ['[]']
    usage_feedback = (
        'Usage: sys.args[0] <letter> <letter> ... <slots> [<slots> ...]\n'
        "\n Received (['[]']) argument vector"
    )
    assert cli.main(job) is None
    out, err = capsys.readouterr()
    assert out.strip() == usage_feedback
