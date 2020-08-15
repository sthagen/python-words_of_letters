# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring,unused-import,reimported
import pytest  # type: ignore

import words_of_letters.cli as cli


def test_main_ok_empty_array():
    job = ['[]']
    assert cli.main(job) is 2
