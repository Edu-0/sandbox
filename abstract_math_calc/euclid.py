# GCD through Euclid:

def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)


a1 = 1005
b1 = 105
answer = gcd(a1, b1)
print(f"gcd({a1}, {b1}) = {answer}" if (answer != 1) else f"Both numbers ({a1}, {b1}) are relatively prime: {answer}")


# Extended Euclid:

#   How do we get to the formula?
#
#   It's a derived formula from the original
#
#   Euclid: a = bq + r
#
#   On Extended Euclid, we separate r: r = a - bq
#
#   The recursive call gives: bx1 + ry1 = g
#
#   We then start the substitutions:
#
#   bx1 + (a - bq)*y1 = g
#   bx1 + ay1 - b*q*y1 = g
#
#   Group terms:
#
#   b(x1 - qy1) + ay1 = g
#   Arranging the terms
#   ay1 + b(x1 - qy1) = g
#
#   We compare with the original formula: ax + by = g
#
#   x = y1 -> The coefficient of "a" is now y1 | (ax -> ay1)
#   y = x1 - qy1 -> The coefficient of "b" is (x1 - qy1) | (by -> b(x1 - qy1)
#
#   But q is a//b from the original formula
#
#   Then, final answer:
#
#   x = y1
#   y = x1 - (a//b) * y1

def egcd(a, b):
    if b == 0:
        return a, 1, 0  # After the GCD is found, it's put on the first value of the return that won't change

    g, x1, y1 = egcd(b, a % b)  # Pushes a and b onto the stack to be used later

    # After the GCD is found, it's time to do the extended part, which begins to bring past values of a and b, besides new x1, y1 calculated starting from a, 1, 0
    x = y1  # Coefficient of "a"
    y = x1 - (a // b) * y1  # Coefficient of "b"

    return g, x, y  # Returns x and y as in a*x + b*y


print(egcd(1180, 482))