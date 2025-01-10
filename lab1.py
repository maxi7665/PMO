import numpy as np

def simplex(a, b):
    
    return 1;


# 1. определить вводимую переменную
# 1. определить её значение (отношение правой части равенства к коэффициенту при переменной в этом равенстве)

# вариант №4
# x_1+3x_2→max
# 3x_1+2x_2≥10
# -x_1+4x_2≤20
# x_1+2x_2≤16
# -x_1+3x_2≥4
# x_1,x_2≥0

# матрица коэффициентов z,x,s переменных
A = np.array(
    [
    [1, -1, -3,  0,  0,  0,  0,  0],
    [0,  3,  2,  1,  0,  0,  0,  0],
    [0, -1,  4,  0,  1,  0,  0,  0],
    [0,  1,  2,  0,  0,  1,  0,  0],
    [0, -1,  3,  0,  0,  0,  1,  0],
    [0,  1,  1,  0,  0,  0,  0,  1]
    ], 
    dtype = float);

# матрица решений
B = np.array(
    [0, 10, 20, 16, 4, 0], 
    dtype = float);

# тест
# матрица коэффициентов z,x,s переменных
A = np.array(
    [
    [1, -5, -4,  0,  0,  0,  0],
    [0,  6,  4,  1,  0,  0,  0],
    [0,  1,  2,  0,  1,  0,  0],
    [0, -1,  1,  0,  0,  1,  0],
    [0,  0,  1,  0,  0,  0,  1]
    ], 
    dtype = float);

# матрица решений
B = np.array(
    [0, 24, 6, 1, 2], 
    dtype = float);

solve = simplex(A, B);

print(A);
print(solve);
