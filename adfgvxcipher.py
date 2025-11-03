"""
ADFGVX Cipher - implementácia šifry používanej počas 1. svetovej vojny
Kombinuje substitúciu (náhrada znakov) a transpozíciu (preusporiadanie stĺpcov)
"""

import unicodedata
import random
from typing import List, Tuple, Optional

# Abecedy
ALPHABET_CZECH_25 = "ABCDEFGHIJKLMNOPQRSTUVXYZ"  # bez W (W→V)
ALPHABET_ENGLISH_25 = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # bez J (J→I)
ALPHABET_36 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"  # pre ADFGVX

# Indexy pre maticu
ADFGX_INDICES = ["A", "D", "F", "G", "X"]
ADFGVX_INDICES = ["A", "D", "F", "G", "V", "X"]

# Značka pre medzery
SPACE_MARKER = "XMEZERAX"


def remove_diacritics(text: str) -> str:
    """Odstráni diakritiku z textu (č→c, á→a, atď.)"""
    normalized = unicodedata.normalize("NFKD", text)
    return "".join(c for c in normalized if not unicodedata.combining(c))


def normalize_by_language(text: str, alphabet: str) -> str:
    """Normalizuje text podľa zvolenej abecedy (W→V alebo J→I)"""
    if "W" not in alphabet:
        text = text.replace("W", "V")
    if "J" not in alphabet:
        text = text.replace("J", "I")
    return text


def filter_input(
    text: str, alphabet: str, preserve_spaces: bool = True, preserve_digits: bool = True
) -> Tuple[str, str]:
    """
    Filtruje vstupný text - odstráni neplatné znaky, zachová medzery a čísla
    Vracia: (filtrovaný_text, zobrazovací_text_BEZ_markerov)
    """
    text = remove_diacritics(text).upper()
    text = normalize_by_language(text, alphabet)

    result = []
    display = []

    for char in text:
        if char == " " and preserve_spaces:
            result.append(" ")
            display.append(" ")  # ✅ Zobraz medzeru namiesto XMEZERAX
        elif char.isdigit() and preserve_digits:
            result.append(char)
            display.append(char)
        elif char in alphabet:
            result.append(char)
            display.append(char)

    filtered_text = "".join(result)
    display_text = " ".join(display)  # Toto pridá medzery medzi znaky pre zobrazenie

    return filtered_text, display_text


def generate_random_alphabet(alphabet: str) -> str:
    """Vygeneruje náhodne zamiešanú abecedu pre maticu"""
    chars = list(alphabet)
    random.shuffle(chars)
    return "".join(chars)


def create_matrix(alphabet: str, size: int) -> List[List[str]]:
    """
    Vytvorí maticu zo zadanej abecedy
    size: 5 pre ADFGX, 6 pre ADFGVX
    """
    if len(alphabet) != size * size:
        raise ValueError(
            f"Alphabet must have {size*size} characters, got {len(alphabet)}"
        )

    matrix = []
    for i in range(size):
        row = list(alphabet[i * size : (i + 1) * size])
        matrix.append(row)
    return matrix


def find_position(matrix: List[List[str]], char: str) -> Optional[Tuple[int, int]]:
    """Nájde pozíciu znaku v matici, vracia (riadok, stĺpec) alebo None ak znak nie je v matici"""
    for i, row in enumerate(matrix):
        for j, c in enumerate(row):
            if c == char:
                return (i, j)
    return None


def substitute_encrypt(
    plaintext: str, matrix: List[List[str]], indices: List[str]
) -> str:
    """
    Fáza 1: Substitúcia (náhrada)
    Každý znak nahradí dvojicou indexov (riadok + stĺpec)
    """
    result = []

    # Najprv nahradíme medzery markerom
    plaintext = plaintext.replace(" ", SPACE_MARKER)

    i = 0
    while i < len(plaintext):
        # Kontrola markera medzery
        if plaintext[i : i + len(SPACE_MARKER)] == SPACE_MARKER:
            # Zašifrujeme každý znak markera
            for char in SPACE_MARKER:
                pos = find_position(matrix, char)
                if pos:
                    row, col = pos
                    result.append(indices[row])
                    result.append(indices[col])
            i += len(SPACE_MARKER)
        else:
            # ✅ Všetky znaky (vrátane číslic) zašifruj
            pos = find_position(matrix, plaintext[i])
            if pos:
                row, col = pos
                result.append(indices[row])
                result.append(indices[col])
            i += 1

    return "".join(result)


def transpose_encrypt(substituted: str, keyword: str) -> Tuple[str, List[str]]:
    """
    Fáza 2: Transpozícia (preusporiadanie stĺpcov)
    1. Zapíše substituted text do riadkov pod keyword
    2. Zoradí stĺpce podľa abecedného poradia keyword
    3. Prečíta stĺpce zhora dolu
    Vracia: (šifrovaný_text, zobrazenie_stĺpcov)
    """
    # Odstránime medzery a číslice pre transpozíciu
    clean_text = "".join(c for c in substituted if c.isalpha())

    key_len = len(keyword)

    # Vytvoríme stĺpce
    columns = [""] * key_len
    for i, char in enumerate(clean_text):
        columns[i % key_len] += char

    # Zoradíme indexy podľa keyword abecedne
    sorted_indices = sorted(range(key_len), key=lambda k: keyword[k])

    # Prečítame stĺpce v zoradenom poradí
    result = []
    column_display = []

    for idx in sorted_indices:
        result.append(columns[idx])
        column_display.append(f"{keyword[idx]}: {columns[idx]}")

    return "".join(result), column_display


def transpose_decrypt(ciphertext: str, keyword: str, substituted_len: int) -> str:
    """
    Reverzná fáza 2: Dekódovanie transpozície
    1. Vypočíta dĺžky stĺpcov
    2. Rekonštruuje stĺpce v zoradenom poradí
    3. Vráti stĺpce do pôvodného poradia keyword
    4. Prečíta po riadkoch
    """
    key_len = len(keyword)

    # Vypočítame dĺžky stĺpcov
    base_len = substituted_len // key_len
    extra = substituted_len % key_len

    # Zoradené indexy podľa keyword
    sorted_indices = sorted(range(key_len), key=lambda k: keyword[k])

    # Rozdelíme ciphertext do stĺpcov (sú v zoradenom poradí)
    columns = [""] * key_len
    pos = 0

    for sorted_pos, original_idx in enumerate(sorted_indices):
        # Prvých 'extra' stĺpcov v ORIGINÁLNOM poradí má extra znak
        col_len = base_len + (1 if original_idx < extra else 0)
        columns[original_idx] = ciphertext[pos : pos + col_len]
        pos += col_len

    # Prečítame po riadkoch (z originálneho poradia stĺpcov)
    result = []
    max_len = max(len(col) for col in columns) if columns else 0

    for i in range(max_len):
        for col in columns:
            if i < len(col):
                result.append(col[i])

    return "".join(result)


def substitute_decrypt(
    substituted: str, matrix: List[List[str]], indices: List[str]
) -> str:
    """
    Reverzná fáza 1: Dekódovanie substitúcie
    Prevádza dvojice indexov späť na znaky
    Obnoví SPACE_MARKER späť na medzery
    """
    result = []

    i = 0
    while i < len(substituted):
        if i + 1 < len(substituted):
            row_idx = substituted[i]
            col_idx = substituted[i + 1]

            if row_idx in indices and col_idx in indices:
                row = indices.index(row_idx)
                col = indices.index(col_idx)
                result.append(matrix[row][col])
                i += 2
            else:
                i += 1
        else:
            i += 1

    plaintext = "".join(result)

    # Nahradíme SPACE_MARKER späť na medzery
    plaintext = plaintext.replace(SPACE_MARKER, " ")

    return plaintext


def encrypt(
    plaintext: str, matrix_str: str, keyword: str, cipher_type: str
) -> Tuple[str, str, str, List[List[str]], List[str]]:
    """
    Hlavná šifrovacia funkcia
    Vracia: (šifrovaný_text, filtrovaný_text, substituted_text, matica, zobrazenie_stĺpcov)
    """
    # Určíme abecedu a indexy podľa typu šifry
    if cipher_type == "ADFGX_CZECH":
        alphabet = ALPHABET_CZECH_25
        indices = ADFGX_INDICES
        size = 5
    elif cipher_type == "ADFGX_ENGLISH":
        alphabet = ALPHABET_ENGLISH_25
        indices = ADFGX_INDICES
        size = 5
    elif cipher_type == "ADFGVX":
        alphabet = ALPHABET_36
        indices = ADFGVX_INDICES
        size = 6
    else:
        raise ValueError(f"Unknown cipher type: {cipher_type}")

    # Filtrujeme vstup
    filtered_text, display_text = filter_input(plaintext, alphabet)

    # Vytvoríme maticu
    if matrix_str and len(matrix_str) == size * size:
        matrix = create_matrix(matrix_str, size)
    else:
        raise ValueError(f"Matrix must have exactly {size*size} characters")

    # Fáza 1: Substitúcia
    substituted = substitute_encrypt(filtered_text, matrix, indices)

    # Fáza 2: Transpozícia
    ciphertext, column_display = transpose_encrypt(substituted, keyword.upper())

    return ciphertext, display_text, substituted, matrix, column_display


def decrypt(
    ciphertext: str, matrix_str: str, keyword: str, cipher_type: str
) -> Tuple[str, str, List[List[str]]]:
    """
    Hlavná dešifrovacia funkcia
    Vracia: (otvorený_text, substituted_text, matica)
    """
    # Určíme abecedu a indexy podľa typu šifry
    if cipher_type == "ADFGX_CZECH":
        alphabet = ALPHABET_CZECH_25
        indices = ADFGX_INDICES
        size = 5
    elif cipher_type == "ADFGX_ENGLISH":
        alphabet = ALPHABET_ENGLISH_25
        indices = ADFGX_INDICES
        size = 5
    elif cipher_type == "ADFGVX":
        alphabet = ALPHABET_36
        indices = ADFGVX_INDICES
        size = 6
    else:
        raise ValueError(f"Unknown cipher type: {cipher_type}")

    # Vytvoríme maticu
    if matrix_str and len(matrix_str) == size * size:
        matrix = create_matrix(matrix_str, size)
    else:
        raise ValueError(f"Matrix must have exactly {size*size} characters")

    # Vyčistíme ciphertext - odstránime všetko okrem ADFGX/ADFGVX znakov
    clean_cipher = "".join(c for c in ciphertext.upper() if c in indices)

    # Fáza 2: Reverzná transpozícia
    substituted = transpose_decrypt(clean_cipher, keyword.upper(), len(clean_cipher))

    # Fáza 1: Reverzná substitúcia
    plaintext = substitute_decrypt(substituted, matrix, indices)

    return plaintext, substituted, matrix


def format_five(text: str) -> str:
    """Formátuje text do skupín po 5 znakoch oddelených medzerou"""
    text = text.replace(" ", "")
    return " ".join(text[i : i + 5] for i in range(0, len(text), 5))


def get_remaining_chars(matrix_input: str, alphabet: str) -> str:
    """Vráti zostávajúce znaky, ktoré ešte nie sú použité v matici"""
    used = set(matrix_input.upper())
    remaining = [c for c in alphabet if c not in used]
    return "".join(remaining)
