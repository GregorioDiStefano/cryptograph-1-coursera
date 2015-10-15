import sys


"""
    Assignment #1 for Cryptography / University of Maryland / coursera.org
    Crypto attack on Vigenere cipher
"""

"Calculate the index of coincidence"
def calculate_ic(letters):
    letter_count = {}
    sum = 0.0

    for i in letters:
        letter_count[i] = letter_count.get(i, 0) + 1

    for k, v in letter_count.items():
        lc = len(letters)
        sum += float(v * (v - 1)) / float(lc * (lc - 1))
    return sum

"Perform xor shift"
def xor_shift(first_letters_in_shift):
    new_str = ""

    for a in range(0, 0xFF):
        for l in first_letters_in_shift:
            new_str += chr(int(l, 16) ^ a)
        flag = 0
        for c in new_str:
            cint = int(ord(c))

            #Filter out control characters and numbers
            if cint < 32 or cint >= 127 or cint >= 48 and cint <= 57:
                    flag = 1
                    continue
        if not flag:
            print "Key: %s ===> %s" % (hex(int(a)), new_str)
        new_str = ""

def hex_to_bytes(s):
    b = []
    for i in xrange(0, len(ciphertext), 2):
        hexval = "%s%s" % (ciphertext[i], ciphertext[i+1])
        b.append(hexval)
    return b

if __name__ == "__main__":

    ciphertext = "F96DE8C227A259C87EE1DA2AED57C93FE5DA36ED4EC87EF2C63AAE5B9A7EFFD673BE4ACF7BE8923CAB1ECE7AF2DA3DA44FCF7AE29235A24C963FF0DF3CA3599A70E5DA36BF1ECE77F8DC34BE129A6CF4D126BF5B9A7CFEDF3EB850D37CF0C63AA2509A76FF9227A55B9A6FE3D720A850D97AB1DD35ED5FCE6BF0D138A84CC931B1F121B44ECE70F6C032BD56C33FF9D320ED5CDF7AFF9226BE5BDE3FF7DD21ED56CF71F5C036A94D963FF8D473A351CE3FE5DA3CB84DDB71F5C17FED51DC3FE8D732BF4D963FF3C727ED4AC87EF5DB27A451D47EFD9230BF47CA6BFEC12ABE4ADF72E29224A84CDF3FF5D720A459D47AF59232A35A9A7AE7D33FB85FCE7AF5923AA31EDB3FF7D33ABF52C33FF0D673A551D93FFCD33DA35BC831B1F43CBF1EDF67F0DF23A15B963FE5DA36ED68D378F4DC36BF5B9A7AFFD121B44ECE76FEDC73BE5DD27AFCD773BA5FC93FE5DA3CB859D26BB1C63CED5CDF3FE2D730B84CDF3FF7DD21ED5ADF7CF0D636BE1EDB79E5D721ED57CE3FE6D320ED57D469F4DC27A85A963FF3C727ED49DF3FFFDD24ED55D470E69E73AC50DE3FE5DA3ABE1EDF67F4C030A44DDF3FF5D73EA250C96BE3D327A84D963FE5DA32B91ED36BB1D132A31ED87AB1D021A255DF71B1C436BF479A7AF0C13AA14794"
    ciphertext_as_bytes = hex_to_bytes(ciphertext)

    ic = {}
    for i in range(2, 10):
        ic[i] = calculate_ic(ciphertext_as_bytes[::i])

    for k, v in ic.items():
        print "Key size: %s, IC: %s" % (k, v)

    key_length = max(ic, key=lambda i: ic[i])
    print "Key is probably: ", key_length

    first_letters_in_shift = ciphertext_as_bytes[::key_length]

    shift_bits = {}
    for i in xrange(0, len(ciphertext_as_bytes) - 1, key_length):
        for j in range(0, key_length):
            shift_bits[j] = shift_bits.get(j, [])
            shift_bits[j].append(ciphertext_as_bytes[i+j])
        shift_bits[j].append(ciphertext_as_bytes[-j - 1])

    key = ""
    for i in shift_bits.keys():
        xor_shift((shift_bits[i]))
        print "Select a key >> ",
        key += chr(int(sys.stdin.readline().strip(), 16))

    plaintext = ""
    for i, c in enumerate(ciphertext_as_bytes):
        new_c = int(c, 16) ^ ord(key[i % len(key)])
        plaintext += chr(new_c)

    print "Key :%s" % (key)
    print "Plaintext: ", repr(plaintext)
