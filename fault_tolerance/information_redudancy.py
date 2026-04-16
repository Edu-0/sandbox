# Dataword -> 64 bits
# Codeword Size -> 72 bits
# Overall Parity -> End of the codeword
# Hamming(72, 64) - SECDED

# The first 7 bits locate and correct 1 wrong bit.
# Allows detecting 2 wrong bits.

import secrets
import numpy as np


def is_pow_of_2(n):
    return n > 0 and (n & (n-1)) == 0


def calculate_parity_bits(arr):
    # Calculating parity bits

    # It needs to XOR every number which:
    # -> Isn't a power of 2 / parity position
    # -> The i th bit of the position number is = 1.

    for k in range(0, 7):
        p = pow(2, k)
        parity_bit = 0
        for i in range(1, 73):
            if i == p:
                continue
            if ((i >> k) & 1) == 1:
                parity_bit ^= arr[i - 1]
        arr[p - 1] = parity_bit

    # Calculating Overall Parity:
    overall = 0
    for i in range(72):
        overall ^= arr[i]
    arr[71] = overall

    return arr


def data_to_codeword(arr):
    # Generating the codeword array
    cd_arr = np.zeros(72, dtype="u1")

    # Filling codeword array
    data_i = 0
    for i in range(1, 73):
        if not is_pow_of_2(i):
            cd_arr[i - 1] = arr[data_i]
            data_i += 1
            if data_i == 64:
                break
    return cd_arr


if __name__ == "__main__":
    # Generating the first 64 bits that will be used
    data_arr = np.fromiter(format(secrets.randbits(64), '064b'), dtype="u1")

    codeword = data_to_codeword(data_arr)

    codeword = calculate_parity_bits(codeword)

    print(f"Codeword Array Finished: \n{codeword}")

    for index in np.ndindex(codeword.shape):
        print(index[0] + 1, codeword[index])