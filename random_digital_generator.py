# Matplotlib, scipy & numpy only needed for plotting PSD
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from collections import deque


def simulator(logic_statement, initial_input=0, bitsize=8):
    """Simulates the outputs of a shift register with an input that is a logical combination of its outputs."""
    output = deque([0]*bitsize)
    input = initial_input
    output.appendleft(logic_statement(output))
    output.pop()
    q = []
    q.append(output.copy())
    for i in range(2**(bitsize+1)):
        output.appendleft(logic_statement(output))
        output.pop()
        if output == q[0]:
            # Repeating sequence since first state reached again.
            break
        q.append(output.copy())
    return q


def half_bit_unicode(a, b):
    """Returns Unicode tuple, (upper, lower) to represent an edge between bits"""
    if (not a) and (not b):
        # Staying low
        return (" ", u"\u2500")
    elif (not a) and b:
        # Low to high transition
        return (u"\u250C", u"\u2518")
    elif a and (not b):
        # High to low transition
        return (u"\u2510", u"\u2514")
    elif a and b:
        # Staying high
        return (u"\u2500", " ")


def logicprinter(levels):
    """Prints a logic trace in an easier to read format."""
    # As Unicode box characters are used, need two lines for
    # the top and bottom of the trace
    upper = ""
    lower = ""
    for i in range(len(levels)):
        a = levels[i]
        if i == len(levels) - 1:
            # For the last bit, assume circuit remains in state.
            b = a
        else:
            b = levels[i+1]
        result = half_bit_unicode(a, b)
        # Split the tuple returned into upper and lower lines
        upper += result[0]
        lower += result[1]
    i = 0
    while i < len(upper):
        # Only print 50 Characters at a time
        print("{:50}".format(upper[0+i:50+i]))
        print("{:50}".format(lower[0+i:50+i]))
        print(" ")
        i += 50


def logicprinter2(logic_levels):
    """Old logic printing function, kept for testing Unicode implementation"""
    line = ""
    for i in range(len(logic_levels)):
        if i != 0:
            if logic_levels[i-1] != logic_levels[i]:
                # Tranisition
                line += "|"
        if logic_levels[i]:
            # Opposite of an underscore
            line += u"\u203E"
        else:
            line += "_"
    print(line)


def list_sum(x):
    total = 0
    for i in x:
        total += i
    return total


def mean_estimate(x):
    return list_sum(x)/len(x)


def variance_estimate(x):
    y = [(i - mean_estimate(x))**2 for i in x]
    return mean_estimate(y)


def analyse(logic, initial_input=False, bitsize=8):
    if initial_input:
        init_input_txt = "high"
    else:
        init_input_txt = "low"
    print("Analysing {} Bit Sequence Generator, with input initially {} and a logic function for a {}".format(
        bitsize, init_input_txt, logic.__doc__))
    outputs = simulator(logic, initial_input, bitsize)
    first_output = [x[0] for x in outputs]
    logicprinter(first_output)
    print("Length of Sequence: ", len(first_output))
    # print("Mean: ",mean_estimate(first_output))
    # print("Variance: ", variance_estimate(first_output))
    return first_output


def plot_power_spectral_density(logic_levels, frequency, title):
    x = np.array(logic_levels)
    # To represent the 5/0V logic levels when measured we multiply 1/0 by 5, to give a more accurate PSD
    x = 5*x
    # Not using a window, only applying a periodogram method
    f, Pxx_den = signal.periodogram(x, frequency)
    plt.semilogy(f, Pxx_den)
    plt.xlabel('frequency [Hz]')
    plt.ylabel('PSD [V**2/Hz]')
    plt.title(title)
    plt.show()


def test_match_expected(testdata, expected):
    """Returns Boolean value if [testdata] is a subsequence of [expected] data"""
    match = False
    print("Finding the sequence:")
    logicprinter(testdata)
    print("In the expected output of the generator:")
    logicprinter(expected)
    for i in range(len(expected)):
        if expected[i] == testdata[0] and expected[i:i+len(testdata)] == testdata:
            print("Match found at index ", i)
            match = True
    if not match:
        print("Sequence Not Found")
    return match


def logic_statement1(q):
    """Fibonacci Sequence Generator"""
    return (q[5] ^ q[4] ^ q[7] ^ q[3] ^ 1)
    # return ((((q[5] != q[4]) != q[7] ) != q[3]) != True)


def fibonacci16(q):
    """16 bit Fibonacci Sequence Generator"""
    # return ((((q[15] != q[14]) != q[12] ) != q[3]) != True)
    return (q[15] ^ q[14] ^ q[12] ^ q[3] ^ 1)


# others = analyse(fibonacci16,bitsize =16)
s = analyse(logic_statement1)

test_result1 = [True, True, False, False, True, False, False, False, True, True, False, True, True, True, True, True,
                False, True, False, True, False, False, True, False, False, True, False, True, False, False, True, True, False, True]
test_match_expected(test_result1, s)


raw_data_test2 = [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1,
                  1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0]
# Since our second test result was via an inverter:
# test_result2 = [not x for x in raw_data_test2]
s_inverse = [not x for x in s]
test_match_expected(raw_data_test2, s_inverse)


plot_power_spectral_density(raw_data_test2, 1e6, 'Power Spectral Density Plot of Test Data 2')
plot_power_spectral_density(s, 2e6, 'Power Spectral Density Plot of Sequence (No Window)')

# Length of Sequence:  65535
# Mean:  0.49999237048905165
# Variance:  0.2499999999417888
# Now much quicker
# logicprinter2(test_result)
