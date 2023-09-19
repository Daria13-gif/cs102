# функция выполняет шифрование текста с использованием шифра Виженера
def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    # Создается пустая строка ciphertext, которая будет содержать зашифрованный текст
    ciphertext = ""
    for i in range(len(plaintext)):  # обход каждой буквы в plaintext
        if "a" <= plaintext[i] <= "z":  # проверка наличия буквы в алфавите
            # находим сдвиг для каждой буквы относительно индексов обоих слов
            ciphertext += chr(
                (ord(plaintext[i]) + ord(keyword.lower()[i % len(keyword)]) - 2 * ord("a")) % 26 + ord("a")
            )
        elif "A" <= plaintext[i] <= "Z":  # проверка наличия буквы в заглавном алфавите
            ciphertext += chr(
                (ord(plaintext[i]) + ord(keyword.upper()[i % len(keyword)]) - 2 * ord("A")) % 26 + ord("A")
            )
        else:
            ciphertext += plaintext[i]
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    for i in range(len(ciphertext)):  # обход каждой буквы в ciphertext
        if "a" <= ciphertext[i] <= "z":  # проверка наличия буквы в алфавите
            # находим сдвиг для каждой буквы относительно индексов обоих слов
            plaintext += chr((ord(ciphertext[i]) - ord(keyword.lower()[i % len(keyword)])) % 26 + ord("a"))
        elif "A" <= ciphertext[i] <= "Z":  # проверка наличия буквы в заглавном алфавите
            plaintext += chr((ord(ciphertext[i]) - ord(keyword.upper()[i % len(keyword)])) % 26 + ord("A"))
        else:
            plaintext += ciphertext[i]
    return plaintext
