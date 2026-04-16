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

# Generating the first 64 bits that will be used
# bin_str = format(secrets.randbits(64), '064b')
# arr = np.fromiter(bin_str, dtype="u1")

arr = np.ones(64, dtype="u1")
print(arr)

# Generating the codeword array
cd_arr = np.zeros(72, dtype="u1")
print(cd_arr)

# Filling codeword array
data_i = 0
for i in range(0, 73):
    if not is_pow_of_2(i):
        cd_arr[i] = arr[data_i]
        data_i += 1
        if data_i == 64: break

print(cd_arr)

for index in np.ndindex(cd_arr.shape):
    print(index, cd_arr[index])
