# Renan Campos
# January 19 2023
#
# A recursive procedure to compute an element of Pascal's triangle
# This is pretty fun to think about
#              1
#             1 1
#            1 2 1
#           1 3 3 1
#          1 4 6 4 1
# The nth row are the coefficients of the terms in the expansion:
# (x+y)^n
# For example:
# (x+y)^3 = (1)x^3 + (3)x^2y^1 + (3)x^1y^2 +(1)y^2
#
# Blaise Pascal (1653) Traite Du Triangle Arithmetiq
# Exercise 1.12 in Structure and Interpretation of Computer Programs.
#
# This shows the beauty of recursion: An elaborate pattern, concisely expressed.
#
# Call this script with a number and you'll get that many rows of Pascal's triange pretty-printed.
#

def pascal_element(r, c):
    if (r == 0) or (r == c) or (c == 0):
        return 1
    return pascal_element((r-1), (c-1)) + pascal_element((r-1), c)


if __name__ == '__main__':
    assert(pascal_element(0, 0) == 1)
    assert(pascal_element(1, 0) == 1)
    assert(pascal_element(1, 1) == 1)
    assert(pascal_element(2, 0) == 1)
    assert(pascal_element(2, 1) == 2)
    assert(pascal_element(2, 2) == 1)
    assert(pascal_element(4, 2) == 6)

    from sys import argv

    total=0
    if len(argv) >= 2:
        total = int(argv[1])

    # To align the triange, for pretty printing, take the log10 of the largest element.
    # This will be the amount of padding each element needs.
    import math
    from math import floor, log
    digit_width = 1+floor(log(pascal_element(total-1, floor(total/2)), 10))

    for row in range(total):
        print(" "*((total-row)*digit_width), end="")
        for col in range(row+1):
            print(f"{pascal_element(row,col):{digit_width}}", end=" "*digit_width)
        print()
