import math

from pysat.solvers import Glucose3

n = 6
clauses = []
new_var_index_start = n * n + 1


def print_solution(solution):
    if solution is None:
        print("No solution found.")
    else:
        for row in solution:
            print(" ".join("Q" if cell else "." for cell in row))


def binomial_at_least_one(a: list):
    return [a]


def binomial_at_most_one(a: list):
    expr = []
    for i in range(len(a)):
        for j in range(i + 1, len(a)):
            expr.append([-a[i], -a[j]])
    return expr


def binomial_exactly_one(a: list):
    return binomial_at_most_one(a) + binomial_at_least_one(a)


def flattening(row, column, n):
    return row * n + column + 1


def at_least_one(a: list):
    return [a]


def at_most_one(a: list, start: int):
    number_of_column = math.ceil(math.sqrt(len(a)))
    number_of_row = len(a) // number_of_column
    if (number_of_row*number_of_column<len(a)):
        number_of_row+=1

    column_var = [i for i in range(start, start + number_of_column)]
    start += number_of_column
    row_var = [i for i in range(start, start + number_of_row)]
    start += number_of_row

    exprs = []
    exprs += binomial_at_most_one(column_var)
    exprs += binomial_at_most_one(row_var)

    # for i in range(number_of_column):
    #     for j in range(number_of_row):
    #         t = i * number_of_row + j
    #         if t < len(a):
    #             exprs += [[row_var[j], -a[t]], [column_var[i], -a[t]]]

    for i in range(number_of_row):
        for j in range(number_of_column):
            t = i * number_of_column + j
            if t < len(a):
                exprs += [[row_var[i], -a[t]], [column_var[j], -a[t]]]

    return exprs, start


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
