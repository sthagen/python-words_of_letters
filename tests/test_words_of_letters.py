# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring,unused-import,reimported
import pytest  # type: ignore

import words_of_letters.words_of_letters as wol


def test_read_mixed_case_word_text_minimal_ok():
    wol.LANGUAGE_TEXT_FILE_PATH = "tests/fixture/text/tgerman_title.dict"
    word_length = 2
    assert wol.read_mixed_case_word_text(word_length) == {'AT', 'WC', 'BH', 'WM', 'WG', 'AU'}
