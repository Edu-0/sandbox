# Dataword -> 64 bits
# Codeword Size -> 72 bits
# Overall Parity -> End of the codeword
# Hamming(72, 64) - SECDED

# The first 7 bits locate and correct 1 wrong bit.
# Allows detecting 2 wrong bits.

import secrets
import numpy as np

data = secrets.randbits(64)

bin_str = format(data, '064b')
arr = np.fromiter(bin_str, dtype="u1")

print(arr)
print(arr.shape[0])