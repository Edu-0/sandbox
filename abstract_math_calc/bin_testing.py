a = 0b1011
b = 0b0110
c = (a ^ b)

print(bin(c))

f = 0b1111
f = f << 1

print(bin(f))  # Output 0b11110. Adds a zero to the first position, to the LSB

g = 0b1010
g = g >> 1

print(bin(g))  # Output 0b101. Removes the LSB

x = 0b11010011  # 8 bits, 1 byte

print(bin(x))

overflow = x & 0x80

print(bin(overflow))

# print(len(bin(overflow)[2:])-1) # Getting the size of the binary. Removing the 0b and keeping the last bit

overflow = overflow >> len(bin(overflow)[2:]) - 1  # Takes the MSB to work with
print(overflow)  # Prints the MSB that would overflow if done a shift left


def overflow(binary):  # A default function
    return bin((binary & 0x80) >> 7)[2:]


y = 0b11011011  # 8 bits, one bit overflowed
print(overflow(y))

m = 0b00011011  # AES irreducible binary

# Doing 1 SL:
of = overflow(y)
y = y << 1
# We then remove the MSB, because AES works with 8 bits. The easiest way is:
y = y & 0xff  # y AND 11111111, everything beyond that will be 0, removing the MSB
print(bin(y))  # Output: 0b10110110

if of == bin(1)[2:]:  # Reducing y to m (the irreducible)
    y ^= m  # 10110110 XOR 00011011 = 10101101

print(bin(y))  # Output: 0b10101101, same answer as before
