# All those other files just to train, learn and make everything ready for Multiplicative Inverse

# Comments and explanations of what is being done on each function can be found in euclid.py and gf_operations.py

# Euclid with Binary GF(2^8)

def gf_mul(f, g):
    result = 0
    for i in range(8):
        if (g >> i) & 1:
            temp = f
            for _ in range(i):
                of = bin((temp & 0x80) >> 7)[2:]
                temp = (temp << 1) & 0xFF
                if of == "1":
                    temp ^= 0b11011

            result ^= temp
    return result


def gf2_mul(f, g):
    result = 0
    for i in range(8):
        if (g >> i) & 1:
            temp = f
            for _ in range(i):
                temp = temp << 1
            result ^= temp
    return result


def deg(b):
    for i in range(len(bin(b)[2:]) - 1, -1, -1):
        if (b >> i) & 1:
            return i
    return 0


def gf2_div(a, b):
    q = 0
    r = a

    while deg(r) >= deg(b):
        shift = deg(r) - deg(b)
        q |= (1 << shift)
        r ^= (b << shift)
        if r == 0:
            break
    return q, r


# From this code previously done on euclid.py I just needed to change:
# The // to the gf2_div, getting q for that operation as 1st returned value
# And r for the a % b operation, as 2nd returned value
# Changed - to ^ (XOR) too, as there is no sum or subtraction on GF(2)
# Instead of q*y1, it was changed to gf2_mul(q, y1) to follow the GF(2) rules
def gf_egcd(a, b):
    if b == 0:
        return a, 1, 0

    q, r = gf2_div(a, b)
    g, x1, y1 = gf_egcd(b, r)

    x = y1
    y = x1 ^ gf2_mul(q, y1)

    return g, x, y


a = 0b100011011
b = 0b10000011
g, xf, yf = gf_egcd(a, b)

g_bin, xf_bin, yf_bin = bin(g), bin(xf), bin(yf)
print(f"ax + by = gcd(a, b) -> {bin(a)}*{xf_bin} + {bin(b)}*{yf_bin} = {g_bin}")

# Multiplicative Inverse through Extended Euclid

# Now that I have ax + by = gcd(a, b) I follow the rules:
# g must be 1 to have multiplicative inverse, however as we're using the irreducible polynom it's always true
# (ax) mod a + (by) mod a = 1 mod a
# by mod a = 1 mod a
# b is the given polynom and y is the inverse, which b*y = 1

multiplicative_inverse  = yf

print(f"\nTesting if y is the multiplicative inverse of b: {bin(b)} * {bin(yf)} = {gf_mul(b, yf)}")

print(f"\nAnother proof: (b*b^-1)/irreducible -> ({bin(b)} * {bin(yf)})/{bin(a)} = "
      f"{bin(gf2_mul(b, yf))}/{bin(a)} = "
      f"{gf2_div(gf2_mul(b, yf), a)[1]}")