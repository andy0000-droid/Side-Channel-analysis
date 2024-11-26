# Ben Ryan
# AES Key Expansion
# Program uses provided key as input, outputs the corresponding keywords w0 - w43 as given in table to cmd

sbox = [
    0x63,
    0x7C,
    0x77,
    0x7B,
    0xF2,
    0x6B,
    0x6F,
    0xC5,
    0x30,
    0x01,
    0x67,
    0x2B,
    0xFE,
    0xD7,
    0xAB,
    0x76,
    0xCA,
    0x82,
    0xC9,
    0x7D,
    0xFA,
    0x59,
    0x47,
    0xF0,
    0xAD,
    0xD4,
    0xA2,
    0xAF,
    0x9C,
    0xA4,
    0x72,
    0xC0,
    0xB7,
    0xFD,
    0x93,
    0x26,
    0x36,
    0x3F,
    0xF7,
    0xCC,
    0x34,
    0xA5,
    0xE5,
    0xF1,
    0x71,
    0xD8,
    0x31,
    0x15,
    0x04,
    0xC7,
    0x23,
    0xC3,
    0x18,
    0x96,
    0x05,
    0x9A,
    0x07,
    0x12,
    0x80,
    0xE2,
    0xEB,
    0x27,
    0xB2,
    0x75,
    0x09,
    0x83,
    0x2C,
    0x1A,
    0x1B,
    0x6E,
    0x5A,
    0xA0,
    0x52,
    0x3B,
    0xD6,
    0xB3,
    0x29,
    0xE3,
    0x2F,
    0x84,
    0x53,
    0xD1,
    0x00,
    0xED,
    0x20,
    0xFC,
    0xB1,
    0x5B,
    0x6A,
    0xCB,
    0xBE,
    0x39,
    0x4A,
    0x4C,
    0x58,
    0xCF,
    0xD0,
    0xEF,
    0xAA,
    0xFB,
    0x43,
    0x4D,
    0x33,
    0x85,
    0x45,
    0xF9,
    0x02,
    0x7F,
    0x50,
    0x3C,
    0x9F,
    0xA8,
    0x51,
    0xA3,
    0x40,
    0x8F,
    0x92,
    0x9D,
    0x38,
    0xF5,
    0xBC,
    0xB6,
    0xDA,
    0x21,
    0x10,
    0xFF,
    0xF3,
    0xD2,
    0xCD,
    0x0C,
    0x13,
    0xEC,
    0x5F,
    0x97,
    0x44,
    0x17,
    0xC4,
    0xA7,
    0x7E,
    0x3D,
    0x64,
    0x5D,
    0x19,
    0x73,
    0x60,
    0x81,
    0x4F,
    0xDC,
    0x22,
    0x2A,
    0x90,
    0x88,
    0x46,
    0xEE,
    0xB8,
    0x14,
    0xDE,
    0x5E,
    0x0B,
    0xDB,
    0xE0,
    0x32,
    0x3A,
    0x0A,
    0x49,
    0x06,
    0x24,
    0x5C,
    0xC2,
    0xD3,
    0xAC,
    0x62,
    0x91,
    0x95,
    0xE4,
    0x79,
    0xE7,
    0xC8,
    0x37,
    0x6D,
    0x8D,
    0xD5,
    0x4E,
    0xA9,
    0x6C,
    0x56,
    0xF4,
    0xEA,
    0x65,
    0x7A,
    0xAE,
    0x08,
    0xBA,
    0x78,
    0x25,
    0x2E,
    0x1C,
    0xA6,
    0xB4,
    0xC6,
    0xE8,
    0xDD,
    0x74,
    0x1F,
    0x4B,
    0xBD,
    0x8B,
    0x8A,
    0x70,
    0x3E,
    0xB5,
    0x66,
    0x48,
    0x03,
    0xF6,
    0x0E,
    0x61,
    0x35,
    0x57,
    0xB9,
    0x86,
    0xC1,
    0x1D,
    0x9E,
    0xE1,
    0xF8,
    0x98,
    0x11,
    0x69,
    0xD9,
    0x8E,
    0x94,
    0x9B,
    0x1E,
    0x87,
    0xE9,
    0xCE,
    0x55,
    0x28,
    0xDF,
    0x8C,
    0xA1,
    0x89,
    0x0D,
    0xBF,
    0xE6,
    0x42,
    0x68,
    0x41,
    0x99,
    0x2D,
    0x0F,
    0xB0,
    0x54,
    0xBB,
    0x16,
]

Rcon = [
    0x00000000,
    0x01000000,
    0x02000000,
    0x04000000,
    0x08000000,
    0x10000000,
    0x20000000,
    0x40000000,
    0x80000000,
    0x1B000000,
    0x36000000,
]


def keyExpansion(key):
    # prep w list to hold 44 tuples
    w = [()] * 44

    # fill out first 4 words based on the key
    for i in range(4):
        w[i] = (key[4 * i], key[4 * i + 1], key[4 * i + 2], key[4 * i + 3])

    # fill out the rest based on previews words, rotword, subword and rcon values
    for i in range(4, 44):
        # get required previous keywords
        temp = w[i - 1]
        word = w[i - 4]

        # if multiple of 4 use rot, sub, rcon etc
        if i % 4 == 0:
            x = RotWord(temp)
            y = SubWord(x)
            rcon = Rcon[int(i / 4)]

            temp = hexor(y, hex(rcon)[2:])

        # creating strings of hex rather than tuple
        word = "".join(word)
        temp = "".join(temp)

        # xor the two hex values
        xord = hexor(word, temp)
        w[i] = (xord[:2], xord[2:4], xord[4:6], xord[6:8])

    return w


# takes two hex values and calculates hex1 xor hex2
def hexor(hex1, hex2):
    # convert to binary
    bin1 = hex2binary(hex1)
    bin2 = hex2binary(hex2)

    # calculate
    xord = int(bin1, 2) ^ int(bin2, 2)

    # cut prefix
    hexed = hex(xord)[2:]

    # leading 0s get cut above, if not length 8 add a leading 0
    if len(hexed) != 8:
        hexed = "0" + hexed

    return hexed


# takes a hex value and returns binary
def hex2binary(hex):
    return bin(int(str(hex), 16))


# takes from 1 to the end, adds on from the start to 1
def RotWord(word):
    return word[1:] + word[:1]


# selects correct value from sbox based on the current word
def SubWord(word):
    sWord = ()

    # loop throug the current word
    for i in range(4):

        # check first char, if its a letter(a-f) get corresponding decimal
        # otherwise just take the value and add 1
        if word[i][0].isdigit() == False:
            row = ord(word[i][0]) - 86
        else:
            row = int(word[i][0]) + 1

        # repeat above for the seoncd char
        if word[i][1].isdigit() == False:
            col = ord(word[i][1]) - 86
        else:
            col = int(word[i][1]) + 1

        # get the index base on row and col (16x16 grid)
        sBoxIndex = (row * 16) - (17 - col)

        # get the value from sbox without prefix
        piece = hex(sbox[sBoxIndex])[2:]

        # check length to ensure leading 0s are not forgotton
        if len(piece) != 2:
            piece = "0" + piece

        # form tuple
        sWord = (*sWord, piece)

    # return string
    return "".join(sWord)


# used to display the keywords neatly in this form: w0 = 0f 15 71 c9
def prettyPrint(w):
    print("\n\nKeywords: \n")

    for i in range(len(w)):
        print("w" + str(i), "=", w[i][0], w[i][1], w[i][2], w[i][3])


def main():
    # hardcoding input key for demonstration purposes, could be read in from user/program via cmd/gui etc.
    """
    key = [
        "01",
        "23",
        "45",
        "67",
        "89",
        "ab",
        "cd",
        "ef",
        "12",
        "34",
        "56",
        "78",
        "9a",
        "bc",
        "de",
        "f0",
    ]
    """
    key = [
        "00",
        "01",
        "02",
        "03",
        "04",
        "05",
        "06",
        "07",
        "08",
        "09",
        "0a",
        "0b",
        "0c",
        "0d",
        "0e",
        "0f",
    ]

    # expand key
    w = keyExpansion(key)

    # display nicely
    print("Key provided: " + "".join(key))
    prettyPrint(w)


if __name__ == "__main__":
    main()
