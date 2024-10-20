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


def flattening(row, column, n):
    return row * n + column + 1


def at_least_one(a: list):
    return [a]


# def at_most_one(a: list, start: int):
#     number_of_new_variable = len(a) - 1
#     expr = [[-a[0], start], [-a[-1], - (start + number_of_new_variable - 1)]]
#     count = 1
#     for i in range(1, len(a)-1):
#         expr += [[-a[i], start + count], [-(start + count - 1), start + count],[-(start+count-1),-a[i]]]
#         count += 1
#     return expr,start + number_of_new_variable

def at_most_k(a: list, k: int, start: int):
    new_var = []
    exprs = []
    for i in range(len(a)):
        temp = []
        for j in range(k):
            temp.append(start + i * k + j)
        new_var.append(temp)
    start += k * len(a)

    # Xi is true then the first bit of register i must be true
    for i in range(len(a) - 1):
        exprs.append([-a[i], new_var[i][0]])

    # Ensures that in the first register only the first bit can be true
    for i in range(1, k):
        exprs.append([-new_var[0][i]])

    # Constrain each register i (1<i<n) to contain the value of the previous register plus Xi.
    for i in range(1, len(a) - 1):
        for j in range(k):
            exprs.append([-new_var[i - 1][j], new_var[i][j]])

    for i in range(1, len(a) - 1):
        for j in range(1, k):
            exprs.append([-a[i], -new_var[i - 1][j - 1], new_var[i][j]])

    for i in range(len(a)):
        exprs.append([-a[i], -new_var[i - 1][k - 1]])

    return exprs, start


def exactly_one(a: list, start: int):
    t, end = at_most_k(a, 1, start)
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
    t, new_var_index_start = (at_most_k(diagonal, 1, new_var_index_start))
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
    t, new_var_index_start = (at_most_k(diagonal, 1, new_var_index_start))
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
    t, new_var_index_start = (at_most_k(diagonal, 1, new_var_index_start))
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
    t, new_var_index_start = (at_most_k(diagonal, 1, new_var_index_start))
    clauses += t

print(clauses)

solver = Glucose3()
for clause in clauses:
    solver.add_clause(clause)

if solver.solve():
    model = solver.get_model()
    print_solution([[int(model[i * n + j] > 0) for j in range(n)] for i in range(n)])
