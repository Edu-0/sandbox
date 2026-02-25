def gf_mul(f, g, m):
    result = 0
    for i in range(8):
        if (g >> i) & 1:  # If the i th value of g is 1 (Dislocation done through shift right, from MSB to LSB)
            temp = f  # f(x) will be used more times, so I save on a temp
            for _ in range(
                    i):  # Depending on the position of the 1 in the binary number, it'll do shift lefts for the same number as position
                of = bin((temp & 0x80) >> 7)[2:]  # Verifying if there will be an overflow each time
                temp = (temp << 1) & 0xFF  # I cap the maximum size to 8 bits and shift left
                if of == "1":
                    temp ^= m  # If it leads to an OF, reduce

            result ^= temp  # Sum to the final result with an XOR
    return bin(result)

f = 0b01010111
g = 0b10000011

m = 0b00011011 # Irreducible for GF(2^8)

# + -> Sum

sum_bin = f^g
print(f"Sum of {bin(f)} + {bin(g)} = {bin(sum_bin)}")

# * -> Multiplication

print(f"Multiplication of {bin(f)} + {bin(g)} = {gf_mul(f, g, m)}")