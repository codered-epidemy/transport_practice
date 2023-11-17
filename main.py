import sympy as sp


def get_from_file(src):
    with open(src) as f:
        matrix = [list(map(float, row.split())) for row in f.readlines()]
        from_where = matrix[0]
        to_where = []
        coeffs = []
        i = 1
        while i != len(matrix):
            to_where.append(matrix[i][0])
            coeffs.append(matrix[i][1:])
            i += 1
    return from_where, to_where, coeffs


# Функция, которую необходимо минимизировать
# На вход - символы из функции return_symbols
def function_to_minimize(x):
    func = 0
    for i in range(len(x)):
        func += x[i] ** 2
    return func


def constraints_funcs(a_len, b_len, from_where, to_where, coeffs):
    amount = a_len * b_len
    constraints = []
    x_symbols = sp.symbols(' '.join(['x{}'.format(i) for i in range(1, amount + 1)]))
    temp_expression = 0
    k = 0
    for i in range(b_len):
        for j in range(a_len):
            temp_expression = temp_expression + (coeffs[i][j] - x_symbols[k]) * from_where[j]
            k += 1
        temp_expression = temp_expression - to_where[i]
        constraints.append(temp_expression)
        temp_expression = 0
    return constraints


# Зная размер "матрицы", находим количество неизвестных x + количество ограничений b
def return_symbols(a_len, b_len):
    amount = a_len * b_len
    x_symbols = sp.symbols(' '.join(['x{}'.format(i) for i in range(1, amount + 1)]))
    return x_symbols


def lagrange_function(func_minimize, constraints):
    lagrange_func = func_minimize
    l_symbols = sp.symbols(' '.join(['l{}'.format(i) for i in range(1, len(constraints) + 1)]))
    for i in range(len(constraints)):
        lagrange_func = lagrange_func + l_symbols[i]*(constraints[i])
    return lagrange_func, l_symbols


def find_derivatives(func_lagrange, x_symbols, l_symbols):
    derivatives = []
    for i in range(len(x_symbols)):
        temp_func_x = sp.diff(func_lagrange, x_symbols[i])
        derivatives.append(temp_func_x)
    for j in range(len(l_symbols)):
        temp_func_l = sp.diff(func_lagrange, l_symbols[j])
        derivatives.append(temp_func_l)
    return derivatives


def solve_equation_system(derivatives, x_symbols, l_symbols):
    all_symbols = x_symbols + l_symbols
    solutions = sp.solve(derivatives, all_symbols)
    solutions_list = []
    keys_to_remove = l_symbols
    for key in keys_to_remove:
        del solutions[key]
    for key in solutions.keys():
        solutions_list.append(solutions[key])
    return solutions_list


def get_new_coefficients(coeffs, x_values):
    k = 0
    for i in range(len(coeffs)):
        for j in range(len(coeffs[i])):
            coeffs[i][j] -= x_values[k]
            k += 1
    return coeffs


def main():
    a_coef, b_coef, coeffs = get_from_file('example.txt')
    n, m = len(a_coef), len(b_coef)  # нахожу размерность: n - количество a, m - количество b
    x_symbols = return_symbols(n, m)
    func_minimize = function_to_minimize(x_symbols)
    constraints = constraints_funcs(n, m, a_coef, b_coef, coeffs)
    func_lagrange, l_symbols = lagrange_function(func_minimize, constraints)
    derivatives = find_derivatives(func_lagrange, x_symbols, l_symbols)
    solution_list = solve_equation_system(derivatives, x_symbols, l_symbols)
    new_coeffs = get_new_coefficients(coeffs, solution_list)
    print(new_coeffs)


if __name__ == '__main__':
    main()
