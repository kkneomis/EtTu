def shifttext(text, shift):
    a = ord('a')
    return ''.join(chr((ord(char) - a + shift) % 26 + a) for char in text.lower())

print shifttext(raw_input('Input text here: '), 3)
