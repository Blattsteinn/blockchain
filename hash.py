
def hash_function(word_to_hash):
    bits = encode_word(word_to_hash)
    MODULO = 2 ** 256

    PRIME_INIT = 104395301
    PRIME_1 = 373587913
    PRIME_2 = 104729
    PRIME_3 = 961748941
    PRIME_4 = 2147483647

    calculated = PRIME_INIT
    temp_index = 0
    bit_duo = []
    ones_count = 0  # To introduce conditional nonlinear mixing later

    BIT_DUO_CONSTANTS = {
        (0, 0): 5938474430905413401767207523544980081,
        (0, 1): 2268752756812624175100564572640790511,
        (1, 1): 9808407823880205631311916183101774079,
        (1, 0): 8190922290267339622366176529252862003,
    }

    for i, bit in enumerate(bits):

        if bit == 1:
            ones_count += 1

        base = 67429 if bit == 0 else 91997
        calculated ^= pow(base, temp_index + (i // 8) + (1 if bit else 0), MODULO)

        if i >= 6 and i % 6 in (0, 1):
            bit_duo.append(bit)
            if len(bit_duo) == 2:
                calculated ^= BIT_DUO_CONSTANTS[tuple(bit_duo)]
                calculated %= MODULO
                bit_duo = []

        if (i + 1) % 8 == 0:
            calculated = (calculated * PRIME_2 + PRIME_1) % MODULO
            calculated = ((calculated << 13) | (calculated >> (256 - 13))) % MODULO
            temp_index = 0
        else:
            temp_index += 1

        # EXTRA MID-ROUND MIXING EVERY 32 BITS
        if (i + 1) % 32 == 0:
            calculated ^= pow(PRIME_3, (i // 32) + ones_count, MODULO)
            calculated = (calculated * PRIME_4) % MODULO
            calculated = ((calculated >> 17) | (calculated << (256 - 17))) % MODULO

    # FINALIZATION STAGE — STRONG AVALANCHE
    calculated ^= (calculated >> 33)
    calculated = (calculated * 0xff51afd7ed558ccd) % MODULO
    calculated ^= (calculated >> 29)
    calculated = (calculated * 0xc4ceb9fe1a85ec53) % MODULO
    calculated ^= (calculated >> 32)

    # CONDITIONAL CHAOTIC END MIX
    if ones_count % 2 == 0:
        calculated = pow(calculated, 2, MODULO)
    else:
        calculated = pow(calculated, 3, MODULO)

    calculated = calculated % MODULO
    hex_value = format(calculated, "064x")
    return hex_value

def encode_word(word_):
    encoded_text = word_.encode('utf-8')
    array_of_bits = []
    for letter in encoded_text:
        byte_form = format(letter, '08b')
        for bit in byte_form:
            array_of_bits.append(int(bit))
    return array_of_bits