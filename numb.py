from fractions import Fraction

x = Fraction(1, 3)
y = Fraction(3, 5)
z = x / y
print "%r / %r" % (z.numerator, z.denominator)