import time

from pysat.solvers import Glucose3

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

def at_most_one(a: list):
    expr = []
    for i in range(len(a)):
        for j in range(i + 1, len(a)):
            expr.append([-a[i], -a[j]])
    return expr


def exactly_one(a: list):
    return at_most_one(a) + at_least_one(a)

n = 8
clauses =[]

# Exactly one queen in a row
for i in range(n):
    clauses+=(exactly_one([flattening(i, j, n) for j in range(n)]))

# Exactly one queen in a column
for j in range(n):
    clauses+=(exactly_one([flattening(i, j, n) for i in range(n)]))

# At most one queen in a left negative diagonal
for row in range(n):
    i = row
    j = 0
    diagonal = []
    while i >= 0:
        diagonal.append(flattening(i, j, n))
        i -= 1
        j += 1
    clauses+=(at_most_one(diagonal))

# At most one queen in a right negative diagonal
for row in range(n - 1, 0, -1):
    i = row
    j = n - 1
    diagonal = []
    while i < n:
        diagonal.append(flattening(i, j, n))
        i += 1
        j -= 1
    clauses+=(at_most_one(diagonal))

# At most one queen in a lower positive diagonal
for row in range(0, n):
    i = row
    j = 0
    diagonal = []
    while i < n:
        diagonal.append(flattening(i, j, n))
        i += 1
        j += 1
    clauses+=(at_most_one(diagonal))

# At most one queen in an upper positive diagonal
for row in range(0, n - 1):
    i = row
    j = n - 1
    diagonal = []
    while i >= 0:
        diagonal.append(flattening(i, j, n))
        i -= 1
        j -= 1
    clauses+=(at_most_one(diagonal))

print(clauses)

solver = Glucose3()
for clause in clauses:
    solver.add_clause(clause)

if solver.solve():
    model = solver.get_model()
    print_solution([[int(model[i * n + j] > 0) for j in range(n)] for i in range(n)])

