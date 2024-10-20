import math

from pysat.solvers import Glucose3

n = 8
clauses = []
new_var_index_start = n * n + 1

def print_solution(solution):
    if solution is None:
        print("No solution found.")
    else:
        for row in solution:
            print(" ".join("Q" if cell else "." for cell in row))

def flattening(row, column, n):
    return row * n + column + 1


def at_least_one(a: list):
    return [a]


def at_most_one(a: list, start: int):
    number_of_new_variable = math.ceil(math.log2(len(a)))
    expr = []
    for i in a:
        binary = bin(a.index(i))
        count = 1
        start_temp = start
        for j in range(len(binary) - 1, 1, -1):
            temp = [-i]
            bin_char = binary[j]
            temp.append(start_temp if int(bin_char) == 1 else -start_temp)
            expr.append(temp)
            count += 1
            start_temp += 1
        while count <= number_of_new_variable:
            temp = [-i, -start_temp]
            count += 1
            expr.append(temp)
            start_temp += 1
    return expr, start+number_of_new_variable


def exactly_one(a: list, start: int):
    t, end = at_most_one(a, start)
    return t + at_least_one(a), end


# Exactly one queen in a row
for i in range(n):
    t, new_var_index_start = (exactly_one([flattening(i, j, n) for j in range(n)], new_var_index_start))
    clauses += t

# Exactly one queen in a column
for j in range(n):
    t, new_var_index_start = (exactly_one([flattening(i, j, n) for i in range(n)], new_var_index_start))
    clauses += t

# At most one queen in a left negative diagonal
for row in range(n):
    i = row
    j = 0
    diagonal = []
    while i >= 0:
        diagonal.append(flattening(i, j, n))
        i -= 1
        j += 1
    t, new_var_index_start = (at_most_one(diagonal, new_var_index_start))
    clauses += t

# At most one queen in a right negative diagonal
for row in range(n - 1, 0, -1):
    i = row
    j = n - 1
    diagonal = []
    while i < n:
        diagonal.append(flattening(i, j, n))
        i += 1
        j -= 1
    t, new_var_index_start = (at_most_one(diagonal, new_var_index_start))
    clauses += t

# At most one queen in a lower positive diagonal
for row in range(0, n):
    i = row
    j = 0
    diagonal = []
    while i < n:
        diagonal.append(flattening(i, j, n))
        i += 1
        j += 1
    t, new_var_index_start = (at_most_one(diagonal, new_var_index_start))
    clauses += t

# At most one queen in an upper positive diagonal
for row in range(0, n - 1):
    i = row
    j = n - 1
    diagonal = []
    while i >= 0:
        diagonal.append(flattening(i, j, n))
        i -= 1
        j -= 1
    t, new_var_index_start = (at_most_one(diagonal, new_var_index_start))
    clauses += t

print(clauses)

solver = Glucose3()
for clause in clauses:
    solver.add_clause(clause)

if solver.solve():
    model = solver.get_model()
    print_solution([[int(model[i * n + j] > 0) for j in range(n)] for i in range(n)])

