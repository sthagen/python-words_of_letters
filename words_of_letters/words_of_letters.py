# encoding: utf-8
# pylint: disable=invalid-name,line-too-long
"""Find words withing letters given."""
import pickle
import string
import sys

ENCODING = "utf-8"
ASCII_LETTERS = string.ascii_uppercase
EXTRA_LETTERS = ("Ä", "Ö", "Ü")

PICTURE_LETTERS = 12
SWIPE_LETTERS = 25
MAX_LETTERS = SWIPE_LETTERS

LANGUAGE_GRAMMAR = "ngerman"  # Sample for German, new grammar
LANGUAGE_TEXT_FILE_PATH = f"data/text/{LANGUAGE_GRAMMAR}.dict" 
DB_BASE_PATH = f"data/db/{LANGUAGE_GRAMMAR}_dict_"


def read_mixed_case_word_text(word_length):
    """Setup the database ..."""
    with open(LANGUAGE_TEXT_FILE_PATH, "rt", encoding=ENCODING) as handle:
        wl = word_length
        ld = handle.readlines
        return {
            x.strip().upper() for x in ld() if len(x.strip()) == wl and "ß" not in x
        }


def dump(word_set):
    """Dump the database ..."""
    word_length = len(next(iter(word_set)))  # HACK A DID ACK get some element
    db_path = f"{DB_BASE_PATH}{word_length}.pickle"
    with open(db_path, "wb") as handle:
        pickle.dump(word_set, handle)


def load(word_length, letter_set):
    """Load database for word length."""
    db_path = f"{DB_BASE_PATH}{word_length}.pickle"
    params = dict(encoding=ENCODING)
    l_s = letter_set
    ld = pickle.load
    with open(db_path, "rb") as handle:
        return (word for word in ld(handle, **params) for x in l_s if x in word)


def derive_databases():
    """Load words of typical word lengths from text and dump as pickle databases."""
    for slots in range(2, 20):
        dump(read_mixed_case_word_text(slots))


def match_gen(candidates, material):
    """DRY and streaming."""
    uniq_ch = set(material)
    l_c = {u_ch: material.count(u_ch) for u_ch in uniq_ch}
    for word in set(candidates):
        if all(u_ch in uniq_ch and l_c[u_ch] >= word.count(u_ch) for u_ch in set(word)):
            yield word


def display_letters(letters):
    n_letters = len(letters)
    print(f"{n_letters} Letters available:")
    print()
    if n_letters in (PICTURE_LETTERS, SWIPE_LETTERS):
        if n_letters == PICTURE_LETTERS:
            print(f"    {' '.join(letters[:6])}")
            print(f"    {' '.join(letters[6:])}")
        else:  # SWIPE_LETTERS
            print(f"    {' '.join(letters[:5])}")
            print(f"    {' '.join(letters[5:10])}")
            print(f"    {' '.join(letters[10:15])}")
            print(f"    {' '.join(letters[15:20])}")
            print(f"    {' '.join(letters[20:])}")
    else:
        print(f"    {' '.join(letters)}")
    print()


def display_solutions(letters, matches, slots):
    print(
        f"Found {len(matches)} candidates of length({slots}) from "
        f"letters({' '.join(letters)}):"
    )
    col_n = 1 if len(matches) < 26 else 5
    for n, match in enumerate(matches):
        if not n % col_n:
            print()
        print(f"  {n:3d}) {match}", end="")
    print("\n\n")


def solve(argv=None):
    """Drive the solver."""
    argv = argv if argv else sys.argv[1:]
    if "-i" in argv or "--init" in argv:
        print("Initializing word databases ...")
        derive_databases()
        return 0

    if len(argv) < 3:
        print("Usage: script <letter> <letter> ... <slots> [<slots> ...]")
        print(f"Received ({argv}) argument vector")
        return 2

    letters = []
    n_slots = []
    for char in argv:
        cand = char.upper()
        if cand in ASCII_LETTERS or cand in EXTRA_LETTERS:
            letters.append(cand)
        elif cand in string.digits and 0 < int(cand) < 10:
            n_slots.append(int(cand))
        elif len(cand) == 2 and 9 < int(cand) < 17:
            n_slots.append(int(cand))
        else:
            print(f"WARNING Ignoring character/slot ({char}) ...")

    n_letters = len(letters)
    if n_letters > SWIPE_LETTERS:
        print(f"ERROR More than {SWIPE_LETTERS} letters given ({n_letters})")
        return 2

    n_slots.sort(reverse=True)
    if len(n_slots) > 4:
        print(f"ERROR More than 4 slots given ({len(n_slots)})")
        return 2

    sum_slots = sum(n_slots)
    if sum_slots > n_letters:
        print(
            f"ERROR Only ({n_letters}) characters given but requested ({sum_slots}) slots ({', '.join(str(n) for n in n_slots)}) ..."
        )
        return 2

    unique_letters = set(letters)
    if not sum_slots:
        print(
            f"ERROR ({n_letters}) character{'' if n_letters == 1 else 's'} given but requested no ({sum_slots}) slots ({', '.join(str(n) for n in n_slots)}) ..."
        )
        return 2

    slots = n_slots[0]
    n_candidates = load(slots, unique_letters)

    display_letters(letters)

    matches = sorted(set(match_gen(n_candidates, letters)))
    display_solutions(letters, matches, slots)
    return 0
