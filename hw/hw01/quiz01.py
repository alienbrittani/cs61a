def multiple(a, b):
    """Return the smallest number n that is a multiple of both a and b.

    >>> multiple(3, 4)
    12
    >>> multiple(14, 21)
    42
    """
    "*** YOUR CODE HERE ***"
    r1 = a % b
    if (r1 == 0):
        GCD = b
    else:
        r2 = b % r1
        while (r2 != 0):
            r1, r2 = r2, r1 % r2
        GCD = r1
    return (a * b) // GCD

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
    count = 0
    for k in range(0, 10):
        if has_digit(n, k):
            count = count + 1
    return count

# Returns whether any of the digits within 'n' is 'k' (true/false)
def has_digit(n, k):
    cur_len = len(str(n))
    while cur_len > 0:
        units_dig = n - ((n // 10) * 10)
        if (units_dig == k):
            return True
        else:  # Units digit is not 'k'
            n = n // 10
            cur_len = cur_len - 1
    return False

