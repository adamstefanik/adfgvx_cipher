"""
Test suite pre ADFGVX Cipher
Testuje všetky základné a pokročilé funkcie šifry
"""

from adfgvxcipher import (
    encrypt,
    decrypt,
    ALPHABET_CZECH_25,
    ALPHABET_ENGLISH_25,
    ALPHABET_36,
)

# Farby pre terminál output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


def print_test_header(test_name):
    """Vypíše hlavičku testu"""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{test_name}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")


def print_result(test_name, passed, expected=None, actual=None):
    """Vypíše výsledok testu"""
    if passed:
        print(f"{GREEN}✅ {test_name}: PASS{RESET}")
    else:
        print(f"{RED}❌ {test_name}: FAIL{RESET}")
        if expected and actual:
            print(f"   Expected: {expected}")
            print(f"   Actual:   {actual}")


def test_basic_adfgx_cz():
    """Test 1.1: Základný ADFGX (CZ) encrypt + decrypt"""
    print_test_header("Test 1.1: Základný ADFGX (CZ)")

    plaintext = "HELLO"
    keyword = "KEY"
    matrix = ALPHABET_CZECH_25
    cipher_type = "ADFGX_CZECH"

    print(f"Input: {plaintext}")
    print(f"Keyword: {keyword}")
    print(f"Matrix: {matrix}")

    # Encrypt
    ciphertext, filtered, substituted, _, _ = encrypt(
        plaintext, matrix, keyword, cipher_type
    )
    print(f"Filtered: {filtered}")
    print(f"Ciphertext: {ciphertext}")

    # Decrypt
    decrypted, _, _ = decrypt(ciphertext, matrix, keyword, cipher_type)
    print(f"Decrypted: {decrypted.strip()}")

    # Verify
    passed = plaintext.upper() == decrypted.strip()
    print_result(
        "ADFGX (CZ) Encrypt/Decrypt", passed, plaintext.upper(), decrypted.strip()
    )
    return passed


def test_w_to_v_substitution():
    """Test 1.2: W→V substitúcia (CZ)"""
    print_test_header("Test 1.2: W→V substitúcia")

    plaintext = "WORLD"
    keyword = "TEST"
    matrix = ALPHABET_CZECH_25
    cipher_type = "ADFGX_CZECH"

    print(f"Input: {plaintext}")

    # Encrypt
    ciphertext, filtered, _, _, _ = encrypt(plaintext, matrix, keyword, cipher_type)
    print(f"Filtered: {filtered}")

    # Decrypt
    decrypted, _, _ = decrypt(ciphertext, matrix, keyword, cipher_type)
    print(f"Decrypted: {decrypted.strip()}")

    # Verify (W→V)
    expected = "VORLD"
    passed = expected == decrypted.strip()
    print_result("W→V mapping", passed, expected, decrypted.strip())
    return passed


def test_adfgx_english_j_to_i():
    """Test 2.1: ADFGX (EN) J→I substitúcia"""
    print_test_header("Test 2.1: ADFGX (EN) J→I")

    plaintext = "JUST A TEST"
    keyword = "CIPHER"
    matrix = ALPHABET_ENGLISH_25
    cipher_type = "ADFGX_ENGLISH"

    print(f"Input: {plaintext}")

    # Encrypt
    ciphertext, filtered, _, _, _ = encrypt(plaintext, matrix, keyword, cipher_type)
    print(f"Filtered: {filtered}")

    # Decrypt
    decrypted, _, _ = decrypt(ciphertext, matrix, keyword, cipher_type)
    print(f"Decrypted: {decrypted.strip()}")

    # Verify (J→I, medzery)
    expected_filtered = "IUSTATEST"
    actual_filtered = filtered.replace(" ", "")
    passed = expected_filtered == actual_filtered
    print_result("J→I mapping", passed, expected_filtered, actual_filtered)
    return passed


def test_adfgvx_with_numbers():
    """Test 3.1: ADFGVX s číslami"""
    print_test_header("Test 3.1: ADFGVX (6×6 s číslami)")

    plaintext = "TEST123"
    keyword = "SECRET"
    matrix = ALPHABET_36
    cipher_type = "ADFGVX"

    print(f"Input: {plaintext}")
    print(f"Matrix size: 36 chars (6×6)")

    # Encrypt
    ciphertext, filtered, _, _, _ = encrypt(plaintext, matrix, keyword, cipher_type)
    print(f"Filtered: {filtered}")
    print(f"Ciphertext: {ciphertext}")

    # Decrypt
    decrypted, _, _ = decrypt(ciphertext, matrix, keyword, cipher_type)
    print(f"Decrypted: {decrypted.strip()}")

    # Verify
    passed = plaintext.upper() == decrypted.strip()
    print_result("ADFGVX with numbers", passed, plaintext.upper(), decrypted.strip())
    return passed


def test_spaces_preservation():
    """Test 4.1: Medzery (XMEZERAX marker)"""
    print_test_header("Test 4.1: Zachovanie medzier")

    plaintext = "HELLO WORLD"
    keyword = "KEY"
    matrix = ALPHABET_CZECH_25
    cipher_type = "ADFGX_CZECH"

    print(f"Input: {plaintext}")

    # Encrypt
    ciphertext, filtered, _, _, _ = encrypt(plaintext, matrix, keyword, cipher_type)
    print(f"Filtered: {filtered}")

    # Decrypt
    decrypted, _, _ = decrypt(ciphertext, matrix, keyword, cipher_type)
    print(f"Decrypted: {decrypted.strip()}")

    # Verify (W→V, medzery zachované)
    expected = "HELLO VORLD"
    passed = expected == decrypted.strip()
    print_result("Space preservation", passed, expected, decrypted.strip())
    return passed


def test_manual_matrix():
    """Test 5.2: Manuálna matica"""
    print_test_header("Test 5.2: Custom manuálna matica")

    plaintext = "ABC"
    keyword = "KEY"
    custom_matrix = "ZYXVUTSRQPONMLKJIHGFEDCBA"  # Reverzná abeceda (bez W)
    cipher_type = "ADFGX_CZECH"

    print(f"Input: {plaintext}")
    print(f"Custom matrix: {custom_matrix}")

    # Encrypt
    ciphertext, _, _, _, _ = encrypt(plaintext, custom_matrix, keyword, cipher_type)
    print(f"Ciphertext: {ciphertext}")

    # Decrypt
    decrypted, _, _ = decrypt(ciphertext, custom_matrix, keyword, cipher_type)
    print(f"Decrypted: {decrypted.strip()}")

    # Verify
    passed = plaintext.upper() == decrypted.strip()
    print_result("Manual matrix", passed, plaintext.upper(), decrypted.strip())
    return passed


def test_validation_errors():
    """Test 6: Validácia chýb"""
    print_test_header("Test 6: Validácia vstupov")

    all_passed = True

    # Test 6.2: Neúplná matica
    try:
        encrypt("TEST", "ABC", "KEY", "ADFGX_CZECH")
        print_result("Incomplete matrix validation", False)
        all_passed = False
    except ValueError as e:
        if "must have exactly 25 characters" in str(e):
            print_result("Incomplete matrix validation", True)
        else:
            print_result("Incomplete matrix validation", False)
            all_passed = False

    # Test 6.3: Nesprávna dĺžka pre ADFGVX
    try:
        encrypt("TEST", ALPHABET_CZECH_25, "KEY", "ADFGVX")
        print_result("Wrong matrix size for ADFGVX", False)
        all_passed = False
    except ValueError as e:
        if "must have exactly 36 characters" in str(e):
            print_result("Wrong matrix size for ADFGVX", True)
        else:
            print_result("Wrong matrix size for ADFGVX", False)
            all_passed = False

    return all_passed


def test_diacritics():
    """Test 9.1: Diakritika"""
    print_test_header("Test 9.1: Odstránenie diakritiky")

    plaintext = "Příliš žluťoučký"
    keyword = "CZECH"
    matrix = ALPHABET_CZECH_25
    cipher_type = "ADFGX_CZECH"

    print(f"Input: {plaintext}")

    # Encrypt
    ciphertext, filtered, _, _, _ = encrypt(plaintext, matrix, keyword, cipher_type)
    filtered_clean = filtered.replace(" ", "")
    print(f"Filtered: {filtered_clean}")

    # Verify že diakritika je odstránená
    has_diacritics = any(ord(c) > 127 for c in filtered_clean)
    passed = not has_diacritics
    print_result("Diacritics removal", passed)

    # Decrypt
    decrypted, _, _ = decrypt(ciphertext, matrix, keyword, cipher_type)
    print(f"Decrypted: {decrypted.strip()}")

    return passed


def test_long_text():
    """Test 10.1: Dlhý text"""
    print_test_header("Test 10.1: Dlhý text (stress test)")

    plaintext = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
    keyword = "LONGKEYWORD"
    matrix = ALPHABET_36
    cipher_type = "ADFGVX"

    print(f"Input: {plaintext} ({len(plaintext)} chars)")

    # Encrypt
    ciphertext, filtered, _, _, _ = encrypt(plaintext, matrix, keyword, cipher_type)
    print(f"Ciphertext length: {len(ciphertext)} chars")

    # Decrypt
    decrypted, _, _ = decrypt(ciphertext, matrix, keyword, cipher_type)
    print(f"Decrypted: {decrypted.strip()}")

    # Verify
    expected = plaintext.replace(" ", " ")  # Medzery zachované
    passed = expected == decrypted.strip()
    print_result(
        "Long text", passed, expected[:30] + "...", decrypted.strip()[:30] + "..."
    )
    return passed


def test_edge_cases():
    """Test 12: Edge cases"""
    print_test_header("Test 12: Edge cases")

    all_passed = True

    # Test 12.2: Jeden znak
    plaintext = "A"
    keyword = "K"
    matrix = ALPHABET_CZECH_25
    cipher_type = "ADFGX_CZECH"

    print(f"Test: Single character '{plaintext}'")
    ciphertext, _, _, _, _ = encrypt(plaintext, matrix, keyword, cipher_type)
    decrypted, _, _ = decrypt(ciphertext, matrix, keyword, cipher_type)

    passed = plaintext == decrypted.strip()
    print_result("Single character", passed, plaintext, decrypted.strip())
    all_passed = all_passed and passed

    # Test 12.3: Keyword dĺžky 1
    plaintext = "HELLO"
    keyword = "A"

    print(f"Test: Keyword length 1 ('{keyword}')")
    ciphertext, _, _, _, _ = encrypt(plaintext, matrix, keyword, cipher_type)
    decrypted, _, _ = decrypt(ciphertext, matrix, keyword, cipher_type)

    passed = plaintext == decrypted.strip()
    print_result("Keyword length 1", passed, plaintext, decrypted.strip())
    all_passed = all_passed and passed

    return all_passed


def run_all_tests():
    """Spustí všetky testy"""
    print(f"\n{YELLOW}{'='*60}{RESET}")
    print(f"{YELLOW}ADFGVX Cipher - Kompletný test suite{RESET}")
    print(f"{YELLOW}{'='*60}{RESET}")

    tests = [
        ("Test 1.1: Základný ADFGX (CZ)", test_basic_adfgx_cz),
        ("Test 1.2: W→V substitúcia", test_w_to_v_substitution),
        ("Test 2.1: ADFGX (EN) J→I", test_adfgx_english_j_to_i),
        ("Test 3.1: ADFGVX s číslami", test_adfgvx_with_numbers),
        ("Test 4.1: Zachovanie medzier", test_spaces_preservation),
        ("Test 5.2: Manuálna matica", test_manual_matrix),
        ("Test 6: Validácia vstupov", test_validation_errors),
        ("Test 9.1: Diakritika", test_diacritics),
        ("Test 10.1: Dlhý text", test_long_text),
        ("Test 12: Edge cases", test_edge_cases),
    ]

    results = []

    for test_name, test_func in tests:
        try:
            passed = test_func()
            results.append((test_name, passed))
        except Exception as e:
            print(f"{RED}❌ {test_name}: ERROR - {e}{RESET}")
            results.append((test_name, False))

    # Výsledky
    print(f"\n{YELLOW}{'='*60}{RESET}")
    print(f"{YELLOW}VÝSLEDKY TESTOV:{RESET}")
    print(f"{YELLOW}{'='*60}{RESET}")

    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)

    for test_name, passed in results:
        status = f"{GREEN}✅ PASS{RESET}" if passed else f"{RED}❌ FAIL{RESET}"
        print(f"{status} - {test_name}")

    print(f"\n{YELLOW}{'='*60}{RESET}")
    percentage = (passed_count / total_count) * 100

    if passed_count == total_count:
        print(
            f"{GREEN}🎉 VŠETKY TESTY PREŠLI! ({passed_count}/{total_count}) - 100%{RESET}"
        )
        print(f"{GREEN}✅ Aplikácia je pripravená na odovzdanie (10/10 bodov){RESET}")
    else:
        print(
            f"{YELLOW}⚠️  PREŠLO: {passed_count}/{total_count} testov ({percentage:.1f}%){RESET}"
        )
        print(f"{RED}❌ Oprav chyby pred odovzdaním!{RESET}")

    print(f"{YELLOW}{'='*60}{RESET}\n")

    return passed_count == total_count


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
