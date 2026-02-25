a = 0b1011
b = 0b0110
c = (a ^ b)

print(bin(c))

f = 0b1111
f = f << 1

print(bin(f)) # Output 0b11110. Adds a zero to the first position, to the LSB

g = 0b1010
g = g >> 1

print(bin(g)) # Output 0b101. Removes the LSB

x = 0b11010011 # 8 bits, 1 byte

print(bin(x))

overflow = x & 0x80

print(bin(overflow))

# print(len(bin(overflow)[2:])-1) # Getting the size of the binary. Removing the 0b and keeping the last bit

overflow = overflow >> len(bin(overflow)[2:])-1 # Takes the MSB to work with
print(overflow) # Prints the MSB that would overflow if done a shift left

def overflow(binary): # A default function
    return bin((binary & 0x80) >> 7)[2:]

y = 0b11011011 # 8 bits, one bit overflowed
print(overflow(y))