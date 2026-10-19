def encrypt(text: str, shift: int) -> str:
    # result = "" 
    chars = [] # Build a list instead of a string to reduce the time complexity to always O(n), guaranteed.
    for char in text:
        if char.islower():
            # shift lowercase and use 97 (unicode point for 'a') as the base
            # result += chr((ord(char) - 97 + shift) % 26 + 97)
            chars.append(chr((ord(char) - 97 + shift) % 26 + 97))
        elif char.isupper():
            # shift uppercase and use 65 (unicode point for 'A') as the base
            # result += chr((ord(char) - 65 + shift) % 26 + 65)
            chars.append(chr((ord(char) - 65 + shift) % 26 + 65))
        else:
            # if not a letter, leave it as is
            # result += char
            chars.append(char)
    return "".join(chars)

def decrypt(text: str, shift: int) -> str:
    return encrypt(text, -shift)

"""
#
# DRY (DO NOT REPEAT YOURSELF)
# decrypt() differs from encrypt() by only `- shift`
#
def decrypt(text: str, shift: int) -> str:
    result = ""
    for char in text:
        if char.islower():
            # shift lowercase and use 97 (unicode point for 'a') as the base
            result += chr((ord(char) - 97 - shift) % 26 + 97)
        elif char.isupper():
            # shift uppercase and use 65 (unicode point for 'A') as the base
            result += chr((ord(char) - 65 - shift) % 26 + 65)
        else:
            # if not a letter, leave it as is
            result += char
    return result
"""

def main():
    text = input("Enter a text: ")
    shift = int(input("Enter a shift: "))

    encrypted = encrypt(text, shift)
    decrypted = decrypt(encrypted, shift)

    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")

if __name__ == "__main__":
    main()
