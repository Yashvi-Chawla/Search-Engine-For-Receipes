from VariableByteEncoder import *

deltas = get_deltas([5, 200, 201, 1000])
print(deltas)

deltaBytes = encode(deltas)
print(deltaBytes)

deltas = decode(deltaBytes)
print(deltas)

numbers = get_numbers(deltas)
print(numbers)
