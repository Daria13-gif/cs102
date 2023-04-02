def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    for i in plaintext:  # обход каждой буквы в plaintext
        if "a" <= i <= "z":  # проверка наличия буквы в алфавите
            # находи букву: для этого нахом сдвиг и прибавляем "а" в пределах алфавита
            ciphertext += chr((ord(i) + shift - ord("a")) % 26 + ord("a"))
        elif "A" <= i <= "Z":  # проверка наличия буквы в заглавном алфавите
            ciphertext += chr((ord(i) + shift - ord("A")) % 26 + ord("A"))
        else:
            ciphertext += i
    return ciphertext
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    # расшифрование это то же самое, что и шифрование, только с отрицательным знаком
    plaintext = encrypt_caesar(ciphertext, -shift)
    return plaintext
