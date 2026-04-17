# This script will be written to learn how to use threads
# Comments are written on the other script, it was removed from here to make it cleaner

class ECCError(Exception):
    pass


import secrets
import numpy as np
import time
from numba import jit

DATAWORD_SIZE = 64
CODEWORD_SIZE = 72
PARITY_BITS = 7

H = np.zeros((PARITY_BITS, CODEWORD_SIZE), dtype="u1")


def is_pow_of_2(n):
    return n > 0 and (n & (n - 1)) == 0


@jit(nopython=True)
def calculate_parity_bits(arr):
    for k in range(0, PARITY_BITS):
        p = pow(2, k)
        parity_bit = 0
        for i in range(1, CODEWORD_SIZE + 1):
            if i == p:
                continue
            if ((i >> k) & 1) == 1:
                parity_bit ^= arr[i - 1]
        arr[p - 1] = parity_bit

    overall = 0
    for i in range(CODEWORD_SIZE):
        overall ^= arr[i]
    arr[CODEWORD_SIZE - 1] = overall

    return arr


def data_to_codeword(arr):
    cd_arr = np.zeros(CODEWORD_SIZE, dtype="u1")

    data_i = 0
    for i in range(1, CODEWORD_SIZE + 1):
        if not is_pow_of_2(i):
            cd_arr[i - 1] = arr[data_i]
            data_i += 1
            if data_i == 64:
                break
    return cd_arr


@jit(nopython=True)
def create_parity_check_matrix():
    for j in range(1, CODEWORD_SIZE):
        if j < CODEWORD_SIZE:
            binary = [(j >> k) & 1 for k in range(PARITY_BITS)]
        else:
            binary = [1] * PARITY_BITS
        H[:, j - 1] = binary


@jit(nopython=True)
def mat_vet_mul(mat_a, vet_b):
    vet_res = np.zeros(mat_a.shape[0], dtype=np.uint8)
    for i in range(mat_a.shape[0]):
        for j in range(vet_b.shape[0]):
            vet_res[i] ^= mat_a[i][j] & vet_b[j]
    return vet_res


@jit(nopython=True)
def ecc_global_parity(cd):
    return np.bitwise_xor.reduce(cd)


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


def create_codeword():
    # data_arr = np.fromiter(format(secrets.randbits(DATAWORD_SIZE), f'0{DATAWORD_SIZE}b'), dtype=np.uint8)
    data_arr = np.ones(64, dtype=np.uint8)

    codeword = data_to_codeword(data_arr)

    codeword = calculate_parity_bits(codeword)

    return codeword


if __name__ == "__main__":
    codeword = create_codeword()
    create_parity_check_matrix()

    codeword[7] ^= 1

    try:
        ecc_result, msg = ecc(H, codeword)
        print(f"\n-> Codeword:")
        print_codeword(ecc_result)
        print(msg)
    except ECCError as e:
        print(e)