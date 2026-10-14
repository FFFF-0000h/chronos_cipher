def encrypt(text: str, shift: int) -> str:
    for everychar in text:
        (ord(everychar) + shift) % 26

def decrypt(text: str, shift: int) -> str:
    for everychar in text:
        (ord(everychar) + shift) % 26

def main():
    text = input("Enter a text: ")
    shift = int(input("Enter a shift: "))

    print(encrypt(text, shift), decrypt(text, shift))

if __name__ == "__main__":
    return main()
