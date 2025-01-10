import numpy as np

def start_basis(a, number_of_main):
    
    # размерность базиса
    basis_len = a.shape[0];

    basis = [];

    for i in range(number_of_main, number_of_main + basis_len):
        basis.append(i); 

    return set(basis);


def simplex(a, number_of_main):

    # базис
    basis_set = start_basis(a, number_of_main);
    basis_size = len(basis_set);

    width = a.shape(1);
    length = a.shape(2);    

    print("Размер базиса " + str(len(basis_set)));

    # print(A.shape[0]);

    cnt = 1;

    # цикл решения 
    while (1):

        # небазисные переменные
        no_basis_set = set(range(0, number_of_main + basis_size - 1));
        no_basis_set = no_basis_set - set(basis_set);

        # определяем какую переменную делаем базисной (вводимой) - 
        # имеющей наибольший отрицательный коэффициент в z-строке
        z = a[0];

        next_basis = -1;
        min = 1;

        for no_basis in no_basis_set:
            if (z[no_basis] < 0 
            and z[no_basis] < min):
                next_basis = no_basis;
                min = z[no_basis];
        
        # нет больше кандидатов в базис - завершаем выполнение
        if next_basis == -1:
            break;
        
        next_no_basis = -1;
        min = -1;
        
        # определяем исключаемый элемент
        for basis in basis_set:
            if (a[basis + 1][next_basis] > 0):
                rel = a[basis + 1][width -1] + a[basis + 1][next_basis];
        
                if rel > 0:
                    if rel < min or min == -1:
                        next_no_basis = basis;
                        min = rel;

        # если нет кандитатов на выход из базиса
        if next_no_basis == -1:
            break;

        # далее расчет нового базисного решения


        # Для этого определим ведущий столбец, ассоциируемый с 
        # вводимой переменной, и ведущую строку, 
        # ассоциируемую с исключаемой переменной. 
        # Элемент, находящийся на пересечении ведущего столбца 
        # и ведущей строки называется ведущим элементом

        main_column = next_basis;
        main_row = next_no_basis + 1; # первая строка - z, поэтому смещение

        # Вычисление элементов новой ведущей строки:
        # Новая ведущая строка = Текущая ведущая строка / Ведущий элемент.
        # Вычисление элементов остальных строк, включая z-строку:
        # Новая строка = Текущая строка - ее коэффициент в ведущем столбце* новая ведущая строка.

        # todo отсюда

        print("Шаг " + str(cnt) 
              + ", вводимая переменная " 
              + str(next_basis));

        
    
        print("Шаг " + str(cnt));
        print(a);

        cnt += 1;
    
        break;


    

    


    
    return a;


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
# начальное условие
A = np.array(
    [
    [-1, -3,  0,  0,  0,  0,  0,  0], #z
    [ 3,  2,  1,  0,  0,  0,  0, 10], #s1
    [-1,  4,  0,  1,  0,  0,  0, 20], #s2
    [ 1,  2,  0,  0,  1,  0,  0, 16], #s3
    [-1,  3,  0,  0,  0,  1,  0,  4], #s4
    [ 1,  1,  0,  0,  0,  0,  1,  0]  #s5
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
    [-5, -4,  0,  0,  0,  0,  0],
    [ 6,  4,  1,  0,  0,  0, 24],
    [ 1,  2,  0,  1,  0,  0,  6],
    [-1,  1,  0,  0,  1,  0,  1],
    [ 0,  1,  0,  0,  0,  1,  2]
    ], 
    dtype = float);

# матрица решений
B = np.array(
    [0, 24, 6, 1, 2], 
    dtype = float);

solve = simplex(A, 2);

#print(A);
print(solve);
