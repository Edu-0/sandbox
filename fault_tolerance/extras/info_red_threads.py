# This script will be written to learn how to use threads
# Comments are written on the other script, it was removed from here to make it cleaner
# As data is small, the threads overhead is higher than the time to execute the scripts

class ECCError(Exception):
    pass

import secrets
import numpy as np
import threading

DATAWORD_SIZE = 64
CODEWORD_SIZE = 72
PARITY_BITS = 7

H = np.zeros((PARITY_BITS, CODEWORD_SIZE), dtype="u1")

lock = threading.Lock()
results = {}

def is_pow_of_2(n):
    return n > 0 and (n & (n-1)) == 0


def calculate_parity_bits(arr):
    for k in range(0, PARITY_BITS):
        p = pow(2, k)
        parity_bit = 0
        for i in range(1, CODEWORD_SIZE+1):
            if i == p:
                continue
            if ((i >> k) & 1) == 1:
                parity_bit ^= arr[i - 1]
        arr[p - 1] = parity_bit

    overall = 0
    for i in range(CODEWORD_SIZE):
        overall ^= arr[i]
    arr[CODEWORD_SIZE-1] = overall

    return arr


def data_to_codeword(arr):
    cd_arr = np.zeros(CODEWORD_SIZE, dtype="u1")

    data_i = 0
    for i in range(1, CODEWORD_SIZE+1):
        if not is_pow_of_2(i):
            cd_arr[i - 1] = arr[data_i]
            data_i += 1
            if data_i == 64:
                break
    return cd_arr


def create_parity_check_matrix():
    for j in range(1, CODEWORD_SIZE):
        if j < CODEWORD_SIZE:
            binary = [(j >> k) & 1 for k in range(PARITY_BITS)]
        else:
            binary = [1]*PARITY_BITS
        H[:, j-1] = binary

def mat_vet_mul(mat_a, vet_b):
    vet_res = np.zeros(mat_a.shape[0], dtype=int)
    for i in range(mat_a.shape[0]):
        for j in range(vet_b.shape[0]):
            vet_res[i] ^= mat_a[i][j] & vet_b[j]
    with lock:
        results["syndrome"] = vet_res

def ecc_global_parity(cd):
    global_parity = np.bitwise_xor.reduce(cd)
    with lock:
        results["global_parity"] = global_parity

def ecc(h, cd):
    t3 = threading.Thread(target=mat_vet_mul, args=(h, cd))
    t4 = threading.Thread(target=ecc_global_parity, args=(cd,))

    t3.start()
    t4.start()
    t3.join()
    t4.join()

    syndrome_value = int("".join(map(str, results["syndrome"][::-1])), 2)

    if results["global_parity"] == 0 and syndrome_value == 0:
        results["ecc_result"] = cd, "OK, No Error Found!"

    if results["global_parity"] == 1 and syndrome_value != 0:
        error_index = syndrome_value - 1
        cd[error_index] ^= 1
        results["ecc_result"] = cd, f"Codeword Corrected! - Error found on pos. {syndrome_value}"

    if results["global_parity"] == 1 and syndrome_value == 0:
        cd[-1] ^= 1
        results["ecc_result"] = cd, "Global Parity Bit Corrected!"

    if results["global_parity"] == 0 and syndrome_value != 0:
        raise ECCError("Multiple errors detected - Corrupted data (SECDED)")


def print_codeword(cd):
    for i, val in enumerate(cd):
        print(f"{i + 1:2d} - {val}", end="\t")
        if (i + 1) % 9 == 0:
            print()

def create_codeword():
    # data_arr = np.fromiter(format(secrets.randbits(DATAWORD_SIZE), f'0{DATAWORD_SIZE}b'), dtype="u1")
    data_arr = np.ones(64, dtype=np.uint8)

    codeword = data_to_codeword(data_arr)

    codeword = calculate_parity_bits(codeword)

    with lock:
        results["codeword"] = codeword


if __name__ == "__main__":
    # Generating the first 64 bits that will be used

    t1 = threading.Thread(target=create_codeword)
    t2 = threading.Thread(target=create_parity_check_matrix)

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    results["codeword"][7] ^= 1

    try:
        ecc(H, results["codeword"])
        print(f"\n-> Codeword:")
        print_codeword(results["ecc_result"][0])
        print(results["ecc_result"][1])
    except ECCError as e:
        print(e)