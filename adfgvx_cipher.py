import unicodedata
import random
from typing import List, Tuple, Optional

ALPHABET_CZECH_25 = "ABCDEFGHIJKLMNOPQRSTUVXYZ"  # bez W
ALPHABET_ENGLISH_25 = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # bez J
ALPHABET_36 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
ADFGX_INDICES = ["A", "D", "F", "G", "X"]
ADFGVX_INDICES = ["A", "D", "F", "G", "V", "X"]
SPACE_MARKER = "XMEZERAX"


def remove_diacritics(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text)
    return "".join(c for c in normalized if not unicodedata.combining(c))


def normalize_by_language(text: str, alphabet: str) -> str:
    if "W" not in alphabet:
        text = text.replace("W", "V")
    if "J" not in alphabet:
        text = text.replace("J", "I")
    return text


def filter_input(text: str, alphabet: str) -> Tuple[str, str]:
    text = remove_diacritics(text).upper()
    text = normalize_by_language(text, alphabet)

    result = []
    display = []

    for char in text:
        if char == " ":
            result.append(" ")
            display.append(" ")
        elif char.isdigit():
            result.append(char)
            display.append(char)
        elif char in alphabet:
            result.append(char)
            display.append(char)

    filtered_text = "".join(result)
    display_text = " ".join(display)

    return filtered_text, display_text


def generate_random_alphabet(alphabet: str) -> str:
    chars = list(alphabet)
    random.shuffle(chars)
    return "".join(chars)


def create_matrix(alphabet: str, size: int) -> List[List[str]]:
    if len(alphabet) != size * size:
        raise ValueError(
            f"Alphabet must have {size*size} characters, got {len(alphabet)}"
        )

    matrix = []
    for i in range(size):
        row = list(alphabet[i * size : (i + 1) * size])
        matrix.append(row)
    return matrix


# Najde poziciu znaku v matici, vracia riadok alebo stlpec alebo None ak znak nie je v matici
def find_position(matrix: List[List[str]], char: str) -> Optional[Tuple[int, int]]:
    for i, row in enumerate(matrix):
        for j, c in enumerate(row):
            if c == char:
                return (i, j)
    return None


def substitute_encrypt(
    plaintext: str, matrix: List[List[str]], indices: List[str]
) -> str:
    result = []

    plaintext = plaintext.replace(" ", SPACE_MARKER)

    i = 0
    while i < len(plaintext):
        if plaintext[i : i + len(SPACE_MARKER)] == SPACE_MARKER:
            for char in SPACE_MARKER:
                pos = find_position(matrix, char)
                if pos:
                    row, col = pos
                    result.append(indices[row])
                    result.append(indices[col])
            i += len(SPACE_MARKER)
        else:
            pos = find_position(matrix, plaintext[i])
            if pos:
                row, col = pos
                result.append(indices[row])
                result.append(indices[col])
            i += 1

    return "".join(result)


def transpose_encrypt(substituted: str, keyword: str) -> Tuple[str, List[str]]:
    clean_text = "".join(c for c in substituted if c.isalpha())

    key_len = len(keyword)

    # Vytvori stlpce
    columns = [""] * key_len
    for i, char in enumerate(clean_text):
        columns[i % key_len] += char

    # Zoradi indexy podla keyword abecedne
    sorted_indices = sorted(range(key_len), key=lambda k: keyword[k])
    result = []
    column_display = []

    for idx in sorted_indices:
        result.append(columns[idx])
        column_display.append(f"{keyword[idx]}: {columns[idx]}")

    return "".join(result), column_display


def transpose_decrypt(ciphertext: str, keyword: str, substituted_len: int) -> str:
    key_len = len(keyword)

    base_len = substituted_len // key_len
    extra = substituted_len % key_len

    # Zoradene indexy podla keyword
    sorted_indices = sorted(range(key_len), key=lambda k: keyword[k])

    # Rozdelíme ciphertext do stlpcov
    columns = [""] * key_len
    pos = 0

    for sorted_pos, original_idx in enumerate(sorted_indices):
        col_len = base_len + (1 if original_idx < extra else 0)
        columns[original_idx] = ciphertext[pos : pos + col_len]
        pos += col_len

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

    plaintext = plaintext.replace(SPACE_MARKER, " ")

    return plaintext


def encrypt(
    plaintext: str, matrix_str: str, keyword: str, cipher_type: str
) -> Tuple[str, str, str, List[List[str]], List[str]]:

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

    filtered_text, display_text = filter_input(plaintext, alphabet)

    if matrix_str and len(matrix_str) == size * size:
        matrix = create_matrix(matrix_str, size)
    else:
        raise ValueError(f"Matrix must have exactly {size*size} characters")

    # Faza 1 Substitucia
    substituted = substitute_encrypt(filtered_text, matrix, indices)

    # Faza 2 Transpozicia
    ciphertext, column_display = transpose_encrypt(substituted, keyword.upper())

    return ciphertext, display_text, substituted, matrix, column_display


def decrypt(
    ciphertext: str, matrix_str: str, keyword: str, cipher_type: str
) -> Tuple[str, str, List[List[str]]]:

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

    if matrix_str and len(matrix_str) == size * size:
        matrix = create_matrix(matrix_str, size)
    else:
        raise ValueError(f"Matrix must have exactly {size*size} characters")

    # Odstranim vsetko okrem ADFGX/ADFGVX znakov
    clean_cipher = "".join(c for c in ciphertext.upper() if c in indices)

    # Faza 2 Reverzna transpozicia
    substituted = transpose_decrypt(clean_cipher, keyword.upper(), len(clean_cipher))

    # Faza 1 Reverzna substitucia
    plaintext = substitute_decrypt(substituted, matrix, indices)

    return plaintext, substituted, matrix


def format_five(text: str) -> str:
    text = text.replace(" ", "")
    return " ".join(text[i : i + 5] for i in range(0, len(text), 5))


def get_remaining_chars(matrix_input: str, alphabet: str) -> str:
    used = set(matrix_input.upper())
    remaining = [c for c in alphabet if c not in used]
    return "".join(remaining)
