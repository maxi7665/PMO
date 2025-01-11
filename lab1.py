import numpy as np
import matplotlib.pyplot as plt

# начальный базис
def start_basis(a, number_of_main):
    
    # размерность базиса
    basis_len = a.shape[0];

    basis = [];

    for i in range(number_of_main, number_of_main + basis_len - 1):
        basis.append(i); 

    return set(basis);


def simplex(a, number_of_main):

    # базис
    basis_list = list(start_basis(a, number_of_main));
    basis_size = len(basis_list);

    width = a.shape[1];
    height = a.shape[0];    

    print("Размер базиса " + str(len(basis_list)));

    cnt = 1;

    # цикл решения 
    while (1):

        print("Шаг " + str(cnt));

        print("Симплекс-таблица");
        print(np.round(a, 2));

        print("Базисные переменные");
        print(basis_list);

        # небазисные переменные
        no_basis_set = set(range(0, number_of_main + basis_size));
        no_basis_set = no_basis_set - set(basis_list);

        print("Небазисные переменные");
        print(no_basis_set);

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
            print("Не определено вводимой переменной - завершение");
            break;
        
        print("Вводимая переменная: " + str(next_basis));
        
        next_no_basis = -1;
        min = -1;
        
        # определяем исключаемый элемент
        for row in range(1, height):
            if (a[row][next_basis] > 0):

                # решение строки делим на элемент в столбце
                # вводимой переменной
                rel = a[row][width -1] / a[row][next_basis];
        
                if rel > 0:
                    if rel < min or min == -1:
                        next_no_basis = basis_list[row - 1];
                        min = rel;

        # если нет кандитатов на выход из базиса
        if next_no_basis == -1:
            print("Не определено исключаемой переменной - завершение")
            break;
        
        print("Исключаемая переменная: " + str(next_no_basis) + ", значение " + str(min));        
        
        swap_index = basis_list.index(next_no_basis);       
        basis_list[swap_index] = next_basis;

        print("Новый базис:" + str(basis_list));

        # далее расчет нового базисного решения
        # Для этого определим ведущий столбец, ассоциируемый с 
        # вводимой переменной, и ведущую строку, 
        # ассоциируемую с исключаемой переменной. 
        # Элемент, находящийся на пересечении ведущего столбца 
        # и ведущей строки называется ведущим элементом

        # ведущий столбец
        main_column = next_basis; 

        # ведущая строка
        main_row = swap_index + 1; # первая строка - z, поэтому смещение

        # ведущий элемент
        main_element = a[main_row][main_column];# ведущий элемент

        print("Ведущий столбец: " + str(main_column));
        print("Ведущая строка: " + str(main_row));
        print("Ведущий элемент: " + str(main_element));

        #1. Вычисление элементов новой ведущей строки:
        for column in range(width):

            # Новая ведущая строка = Текущая ведущая строка / Ведущий элемент.
            a[main_row][column] = a[main_row][column] / main_element;
        
        print("Новая ведущая строка: " + str(np.round(a[main_row], 2)));

        #2. Вычисление элементов остальных строк, включая z-строку:
        for row in set(range(height)) - set([main_row]): # по всем строкам кроме главной
            
            # коэффициент строки в ведущем столбце
            row_main_coeff = a[row][main_column];
        
            for column in range(width):               

                # Новая строка = Текущая строка - 
                # ее коэффициент в ведущем столбце* новая ведущая строка.
                a[row][column] = (a[row][column] - 
                    row_main_coeff * a[main_row][column]);

        cnt += 1;
    
        #break;


    print("Произведено шагов: " + str(cnt - 1));
    print("Итоговая таблица:");
    print(np.round(a, 2));
    
    # искомый коэффициент z
    z = a[0][width - 1];
    
    return [z, a];

# вариант №4
# x_1+3x_2→max
# 3x_1+2x_2≥10
# -x_1+4x_2≤20
# x_1+2x_2≤16
# -x_1+3x_2≥4
# x_1,x_2≥0

# кол-во основных переменных
main_variables = 2;

# матрица коэффициентов z,x,s переменных
# начальное условие
A = np.array(
    [
    [-1, -3,  0,  0,  0,  0,  0], #z
    [ 3,  2,  1,  0,  0,  0, 10], #s1
    [-1,  4,  0,  1,  0,  0, 20], #s2
    [ 1,  2,  0,  0,  1,  0, 16], #s3
    [-1,  3,  0,  0,  0,  1,  4] #s4
    ], 
    dtype = float);

# тест
# матрица коэффициентов z,x,s переменных
# A = np.array(
#     [
#     [-5, -4,  0,  0,  0,  0,  0],
#     [ 6,  4,  1,  0,  0,  0, 24],
#     [ 1,  2,  0,  1,  0,  0,  6],
#     [-1,  1,  0,  0,  1,  0,  1],
#     [ 0,  1,  0,  0,  0,  1,  2]
#     ], 
#     dtype = float);

# A = np.array(
#     [
#     [-2, -3,  0,  0,  0,  0,  0],
#     [ 1,  3,  1,  0,  0,  0, 18],
#     [ 2,  1,  0,  1,  0,  0, 16],
#     [ 0,  1,  0,  0,  1,  0,  5],
#     [ 3,  0,  0,  0,  0,  1, 21]
#     ], 
#     dtype = float);

solve = simplex(A.copy(), main_variables);

#print(A);
print(solve);

# границы для отрисовки графиков - указаны вручную
x_min = 0;
x_max = 10;
y_min = 0;
y_max = 10;

# определяем границы для отрисовки графика на основе ограничений
# for row in range(A.shape[0]):
#     x = A[row][0];
#     y = A[row][1];
#     z = A[row][A.shape[1] - 1];

#     if (x == 0 and y != 0):
#         # y_min = min(y_min, z/y);
#         y_max = max(y_max, z/y);

#     if (y == 0 and x != 0):
#         # x_min = min(x_min, z/x);
#         x_max = max(x_max, z/x);
    
plot_dimension = 100;

# координаты для отрисовки графиков
xdata = np.linspace(x_min - 1, x_max + 1, plot_dimension);
ydata = np.linspace(y_min - 1, y_max + 1, plot_dimension);

fig,ax = plt.subplots();

for row in range(A.shape[0]):
    x = A[row][0];
    y = A[row][1];
    z = A[row][A.shape[1] - 1];
    col = '';

    if (row == 0):
        x = -x;
        y = -y;
        z = solve[1][0][A.shape[1] - 1];
        col = '';

    if (y != 0):
        y_dat = (z - xdata * x);
        y_dat = y_dat / y;
        x_dat = xdata;
    elif (x != 0):
        x_dat = np.linspace(z/x, z/x, plot_dimension);
        y_dat = ydata;

    plot, = ax.plot(x_dat, y_dat, col);
    plot.set_label("(" + str(x) + "x) + (" + str(y) + "y)=" + str(z));

# графики ограничений x,y > 0
plot, = ax.plot(xdata, np.linspace(0, 0, plot_dimension));
plot.set_label("x=0");
plot, = ax.plot(np.linspace(0,0,plot_dimension), ydata);
plot.set_label("y=0");

ax.legend();
plt.show();  