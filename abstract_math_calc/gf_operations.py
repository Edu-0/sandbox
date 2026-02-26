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
    return result


def gf2_mul(f, g):  # This function had 0xFF, 0x80 and Overflow because here it doesn't matter if it goes beyond x^8
    result = 0
    for i in range(8):
        if (g >> i) & 1:
            temp = f
            for _ in range(i):
                temp = temp << 1

            result ^= temp
    return result


f = 0b01010111
g = 0b10000011

m = 0b00011011  # Irreducible for GF(2^8)

# + -> Sum

sum_bin = f ^ g
print(f"Sum of {bin(f)} + {bin(g)} = {bin(sum_bin)}")

# * -> Multiplication

print(f"Multiplication of {bin(f)} * {bin(g)} = {bin(gf_mul(f, g, m))}")

# GF(2) Multiplication (No reduction, needed for multiplicative inverse)

x = 0b10000011  # (x^7 + x + 1)
y = 0b10000000  # (x^7)
print(f"Multiplication in GF(2) of {bin(x)} * {bin(y)} = {bin(gf2_mul(x, y))}")  # (x^7 + x + 1)*(x^7) = x^14 + x^8 + x^7

# Polynomial division

# Takes the highest degree of a polynom
def deg(b):
    for i in range(len(bin(b)[2:]) -1, -1, -1):
        if (b >> i) & 1:
            return i
    return 0


print(deg(m))  # x^4 + x^3 + x + 1 -> Degree of 4
print(deg(gf2_mul(x, y)))  # x^14 + x^8 + x^7 -> degree of 14
print(deg(x))  # x^7 + x + 1 -> degree of 7
print(deg(f))  # 0b01010111 -> degree of 6
print(deg(0b00000000))  # degree 0
print(deg(0b11111111))  # degree 7


# A is the dividend. The dividend will become the remainder and is updated in each step of the division
# B the divisor. The divisor is shifted an amount of times until the highest degree of both are the same for elimination
def gf2_div(a, b):

    """
    How does division works?
    I take the difference in degrees between two dividing binaries
    I shift left b the same amount of times as the difference
    XOR is applied between the value shifted and a

    q |= 1 << diff, uses OR to set the binary quotient
    r ^= b << diff, uses XOR because I need to subtract in GF(2), and XOR can be used to sum and subtract (1 XOR 1 = 0)

    All while degree of a is >= degree of b

    Starting variables:
    q = 0, then it'll be incrementing while the loop is dividing
    r = a, to keep the value of a intact, as it'll be used
    """

    q = 0
    r = a
    while deg(r) >= deg(b):
        shift = deg(r) - deg(b)
        q |= (1 << shift)
        r ^= (b << shift)
        if r == 0:
            break
    return q, r


a = 0b10000011
b = 0b00011101
print(gf2_div(a, b))