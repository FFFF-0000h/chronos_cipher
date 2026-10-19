from datetime import datetime

def get_shift(dt: datetime) -> int:
    # Multiply hours by 60 to convert to minutes, then add the minute component.
    # This gives "minutes since midnight" (0..1439) — a value that uniquely
    # identifies each minute of the day. Simple hour+minute collides
    # (12:01 and 1:12 both → 13), which would let the same message decrypt
    # at different times. % 26 then squeezes the value into 0..25 for Caesar.
    #
    # We use `dt` (the parameter), not a global — that's what makes this
    # function pure and testable. Anyone can call get_shift(datetime(2026,1,1,14,32))
    # and get a deterministic answer.
    return (dt.hour * 60 + dt.minute) % 26

def encrypt_with_time(text: str) -> str:
    now = datetime.now() # capture time once, at call time
    shift = get_shift(now) # derive shift from that time
    ciphertext = encrypt(text, shift)
    time_str = f"{now:%H:%M}" # format for embedding in payload
    payload = f"[{time_str}]{ciphertext}"
    return payload

def extract_timestamp(payload: str) -> str:
    if not payload.startswith("["):
        raise ValueError("No timestamp prefix")
    # .index() raises ValueError if ']' is missing. We deliberately avoid
    # .find(), which returns -1 on miss, and payload[1:-1] would then
    # silently slice off the last character instead of erroring.
    end = payload.index("]")
    return payload[1:end]

def decrypt_with_time(payload: str) -> str:
    parsedd = datetime.strptime(extract_timestamp(payload), "%H:%M")
    shift = get_shift(parsedd)
    indexx = payload.index("]")
    extractt = payload[indexx + 1:]
    return decrypt(extractt, shift)

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
    # shift = int(input("Enter a shift: "))

    encrypted = encrypt_with_time(text)
    decrypted = decrypt_with_time(encrypted)

    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")

if __name__ == "__main__":
     # Smoke tests — run before main(). If any assert fails, you get an
    # AssertionError naming the exact failing line. Cheap, fast, catches
    # regressions when you edit the code next week.
    assert encrypt("abc", 1) == "bcd"                          # simple shift
    assert encrypt("xyz", 3) == "abc"                          # wrap-around forward
    assert decrypt(encrypt("Hello!", 7), 7) == "Hello!"        # round-trip w/ punctuation
    assert encrypt_with_time("").startswith("[")               # empty body allowed
    assert decrypt_with_time(encrypt_with_time("test")) == "test"  # full round-trip

    # Negative path: malformed payload should raise ValueError, not silently
    # return garbage. We assert the error fires AND that it's the right type.
    try:
        decrypt_with_time("no-brackets")
        raise AssertionError("should have raised ValueError")
    except ValueError:
        pass  # expected

    main()
