def multiple(a, b):
    """Return the smallest number n that is a multiple of both a and b.

    >>> multiple(3, 4)
    12
    >>> multiple(14, 21)
    42
    """
    "*** YOUR CODE HERE ***"
    n = max(a, b)
    while ((n % a != 0) or (n % b != 0)):
        n = n + 1
    return n

def unique_digits(n):
    """Return the number of unique digits in positive integer n

    >>> unique_digits(8675309) # All are unique
    7
    >>> unique_digits(1313131) # 1 and 3
    2
    >>> unique_digits(13173131) # 1, 3, and 7
    3
    >>> unique_digits(10000) # 0 and 1
    2
    >>> unique_digits(101) # 0 and 1
    2
    >>> unique_digits(10) # 0 and 1
    2
    """
    "*** YOUR CODE HERE ***"
    num_unique_digits = 0
    for k in range(10):
        if (has_digit(n, k)):
            num_unique_digits = num_unique_digits + 1
    return num_unique_digits

# Returns whether any of the digits within 'n' is 'k'
def has_digit(n, k):
    while (n >= 10):  # More than 1 digit remaining
        all_but_ones_digit = ((n // 10) * 10)
        ones_digit = n - all_but_ones_digit
        if (ones_digit == k):
            return True
        else:
            n = n // 10
    return (n == k)

