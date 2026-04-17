# Dataword -> 64 bits
# Codeword Size -> 72 bits
# Overall Parity -> End of the codeword
# Hamming(72, 64) - SECDED

# The first 7 bits locate and correct 1 wrong bit.
# Allows detecting 2 wrong bits.

class ECCError(Exception):
    pass

import secrets
import numpy as np

DATAWORD_SIZE = 64
CODEWORD_SIZE = 72
PARITY_BITS = 7

H = np.zeros((PARITY_BITS, CODEWORD_SIZE), dtype="u1")

def is_pow_of_2(n):
    return n > 0 and (n & (n-1)) == 0


def calculate_parity_bits(arr):
    # Calculating parity bits

    # It needs to XOR every number which:
    # -> Isn't a power of 2 / parity position
    # -> The i th bit of the position number is = 1.

    for k in range(0, PARITY_BITS):
        p = pow(2, k)
        parity_bit = 0
        for i in range(1, CODEWORD_SIZE+1):
            if i == p:
                continue
            if ((i >> k) & 1) == 1:
                parity_bit ^= arr[i - 1]
        arr[p - 1] = parity_bit

    # Calculating Overall Parity:
    overall = 0
    for i in range(CODEWORD_SIZE):
        overall ^= arr[i]
    arr[CODEWORD_SIZE-1] = overall

    return arr


def data_to_codeword(arr):
    # Generating the codeword array
    cd_arr = np.zeros(CODEWORD_SIZE, dtype="u1")

    # Filling codeword array
    data_i = 0
    for i in range(1, CODEWORD_SIZE+1):
        if not is_pow_of_2(i): # Skips powers of 2
            cd_arr[i - 1] = arr[data_i]
            data_i += 1
            if data_i == 64:
                break
    return cd_arr


def create_parity_check_matrix():
    for j in range(1, CODEWORD_SIZE):
        # For j = 5 (0000101) and 7 parity bits, I separate 1 bit for each K. Binary = [1,0,1,0,0,0,0]
        # Does it 72 times as there are 72 columns and all need to receive the binary version
        if j < CODEWORD_SIZE:
            binary = [(j >> k) & 1 for k in range(PARITY_BITS)] # Verifies their specific line/characteristic
        else:
            binary = [1]*PARITY_BITS # It'll serve as a verifying column that participates on every equation, a general supervisor
        # Each column of the matrix receives the binary of j, as it has the same height as number os lines
        H[:, j-1] = binary

        # Visual explaining extracted from a print:
        # [[1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0]
        #  [0 1 1 0 0 1 1 0 0 1 1 0 0 1 1 0 0 1 1 0 0 1 1 0 0 1 1 0 0 1 1 0 0 1 1 0 0 1 1 0 0 1 1 0 0 1 1 0 0 1 1 0 0 1 1 0 0 1 1 0 0 1 1 0 0 1 1 0 0 1 1 0]
        #  [0 0 0 1 1 1 1 0 0 0 0 1 1 1 1 0 0 0 0 1 1 1 1 0 0 0 0 1 1 1 1 0 0 0 0 1 1 1 1 0 0 0 0 1 1 1 1 0 0 0 0 1 1 1 1 0 0 0 0 1 1 1 1 0 0 0 0 1 1 1 1 0]
        #  [0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 1]
        #  [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0]
        #  [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0]
        #  [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1]]
        # As it can be seen, the first column is = 1, 1000000 | The last column: 1001000, which is equal to 72


def mat_vet_mul(mat_a, vet_b):
    vet_res = np.zeros(mat_a.shape[0], dtype=int)
    for i in range(mat_a.shape[0]):
        for j in range(vet_b.shape[0]):
            vet_res[i] ^= mat_a[i][j] & vet_b[j]
    return vet_res


def ecc(h, cd):
    syndrome_vec = mat_vet_mul(h, cd)
    global_parity = np.bitwise_xor.reduce(cd) # Checking global parity
    syndrome_value = int("".join(map(str, syndrome_vec[::-1])), 2)

    if global_parity == 0 and syndrome_value == 0: # Everything is correct
        return cd, "OK, No Error Found!"

    if global_parity == 1 and syndrome_value != 0: # Global Parity - error | Codeword - wrong
        error_index = syndrome_value - 1
        cd[error_index] ^= 1
        return cd, f"Codeword Corrected! - Error found on pos. {syndrome_value}" # Global parity bit error caused by a codeword error

    if global_parity == 1 and syndrome_value == 0: # Global Parity - error | Codeword - correct
        cd[-1] ^= 1
        return cd, "Global Parity Bit Corrected!" # Corrects global parity bit

    if global_parity == 0 and syndrome_value != 0:
        raise ECCError("Multiple errors detected - Corrupted data (SECDED)") # Global parity bit is correct while codeword error, 2 errors detected.


def print_codeword(cd):
    for i, val in enumerate(cd):
        print(f"{i + 1:2d} - {val}", end="\t")
        if (i + 1) % 9 == 0:
            print()


if __name__ == "__main__":
    # Generating the first 64 bits that will be used
    data_arr = np.fromiter(format(secrets.randbits(DATAWORD_SIZE), f'0{DATAWORD_SIZE}b'), dtype="u1")

    codeword = data_to_codeword(data_arr)

    codeword = calculate_parity_bits(codeword)

    create_parity_check_matrix()

    codeword[7] ^= 1

    try:
        ecc_result, msg = ecc(H, codeword)
        print(f"\n-> Codeword:")
        print_codeword(ecc_result)
        print(msg)
    except ECCError as e:
        print(e)