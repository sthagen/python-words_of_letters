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
MAX_SLOTS = 4

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


def derive_databases(first, last):
    """Load words of typical word lengths from text and dump as pickle databases."""
    for slots in range(first, last + 1):
        dump(read_mixed_case_word_text(slots))


def match_gen(candidates, material, places=None):
    """DRY and streaming."""
    uniq_ch = set(material)
    l_c = {u_ch: material.count(u_ch) for u_ch in uniq_ch}
    for word in set(candidates):
        if all(u_ch in uniq_ch and l_c[u_ch] >= word.count(u_ch) for u_ch in set(word)):
            if not places or all(word[c] == m for c, m in places.items()):
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


def parse(argv):
    letters = []
    n_slots = []
    placeholders = {}
    errors, warnings = [], []

    if len(argv) < 3:
        errors.append(
            "Usage: script <letter> <letter> ... <slots> [<placeholders> <slots> ...]\n"
            f"Received ({argv}) argument vector"
        )
        return letters, n_slots, placeholders, errors, warnings

    slot_active = False
    for char in argv:
        u_char = char.upper()
        if u_char in ASCII_LETTERS or u_char in EXTRA_LETTERS or u_char == "_":
            if not slot_active:
                if u_char != "_":
                    letters.append(u_char)
                else:
                    warnings.append(f"WARNING Ignoring placeholder as letter ({char}) ...")
            else:
                cs = n_slots[-1]
                placeholders.setdefault(cs, []).append(u_char)
                ph_cs = placeholders[cs]
                if len(ph_cs) > cs:
                    errors.append(f"ERROR {len(ph_cs) - cs} too many placeholders ({ph_cs}) for slot {cs}")
                    return letters, n_slots, placeholders, errors, warnings
        elif u_char in string.digits and 0 < int(u_char) < 10:
            n_slots.append(int(u_char))
            slot_active = True
        elif len(u_char) == 2 and 9 < int(u_char) < 17:
            n_slots.append(int(u_char))
            slot_active = True
        else:
            warnings.append(f"WARNING Ignoring character/slot ({char}) ...")

    return letters, n_slots, placeholders, errors, warnings


def apply_rules(letters, n_slots, placeholders, errors, warnings):
    if errors:
        return letters, n_slots, placeholders, errors, warnings
    n_letters = len(letters)
    if n_letters > SWIPE_LETTERS:
        errors.append(f"ERROR More than {SWIPE_LETTERS} letters given ({n_letters})")
        return letters, n_slots, placeholders, errors, warnings

    n_slots.sort(reverse=True)
    if len(n_slots) > MAX_SLOTS:
        errors.append(f"ERROR More than {MAX_SLOTS} slots given ({len(n_slots)})")
        return letters, n_slots, placeholders, errors, warnings

    sum_slots = sum(n_slots)
    if sum_slots > n_letters:
        errors.append(
            f"ERROR Only ({n_letters}) characters given but requested ({sum_slots}) slots ({', '.join(str(n) for n in n_slots)}) ..."
        )
        return letters, n_slots, placeholders, errors, warnings

    if not sum_slots:
        errors.append(
            f"ERROR ({n_letters}) character{'' if n_letters == 1 else 's'} given but requested no ({sum_slots}) slots ({', '.join(str(n) for n in n_slots)}) ..."
        )
        return letters, n_slots, placeholders, errors, warnings

    return letters, n_slots, placeholders, errors, warnings


def solve(argv=None):
    """Drive the solver."""
    argv = argv if argv else sys.argv[1:]
    if argv[0] in ("-i", "--init"):
        min_size, max_size = int(argv[1]), int(argv[2])
        print(f"Initializing word databases for sizes in [{min_size}, {max_size}] ...")
        derive_databases(min_size, max_size)
        return 0

    letters, n_slots, placeholders, errors, warnings = apply_rules(*parse(argv))

    for warning in warnings:
        print(warning)

    if errors:
        print(errors[0])  # Early exit guarantees only one entry
        return 2

    for slots in n_slots:
        places = {k: v for k, v in enumerate(placeholders.get(slots)) if v != "_"}
        n_candidates = load(slots, set(letters))

        display_letters(letters)

        matches = sorted(set(match_gen(n_candidates, letters, places)))
        display_solutions(letters, matches, slots)
    return 0
