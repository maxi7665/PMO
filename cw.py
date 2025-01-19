import numpy as np;
import graphviz as gv;
import subprocess;

# метод северо-западного угла
def north_west(paths, stocks, needs):

    moves=np.zeros(paths.shape);
    s = stocks.copy();
    n = needs.copy();

    excluded_rows = set();
    excluded_columns = set();

    while 1:

        rows = set(range(paths.shape[0])) - excluded_rows;
        columns = set(range(paths.shape[1])) - excluded_columns;

        if (len(rows) == 0 or len(columns) == 0): break;

        for i in rows:
            for j in columns:

                move = min(s[i], n[j]);

                moves[i][j] = move;
    
                if (move == s[i]):
                    excluded_rows.add(i);
                    n[j] = n[j] - move;
                else:
                    excluded_columns.add(j);
                    s[i] = s[i] - move;
    
                break;
        
            break;

    return moves;

# расчет потенциалов
# получить потенциалы
def get_potentials(paths, moves):

    u = dict(); # потенциалы поставщика
    v = dict(); # потенциалы потребителя

    # кол-во u и v
    u_num = paths.shape[0];
    v_num = paths.shape[1];

    # для первого производителя (вершины) 
    # берем потенциал = 100
    u[0] = 100;

    # расчет потенциалов перебором
    while (u.__len__() != u_num 
           or v.__len__() != v_num):        
        
        for prod in range(paths.shape[0]):
            for cons in range(paths.shape[1]):

                path = paths[prod][cons];
                move = moves[prod][cons];

                if (move != 0):
                    if prod in u and not(cons in v):
                        v[cons] = float(u[prod] + path);
                    elif cons in v and not(prod in u):
                        u[prod] = float(v[cons] - path);
    
    u = dict(sorted(u.items()));
    v = dict(sorted(v.items()));    
    
    return [u,v];

def find_edges_scores(paths, moves, potentials):

    [u,v] = potentials;

    edges_scores = {};

    # для ребер у которых нет стрелок считаем характеристику
    for prod in range(paths.shape[0]):
        for cons in range(paths.shape[1]):

            path = paths[prod][cons];
            move = moves[prod][cons];

            if (move > 0): continue;

            diff = u[prod] - v[cons];
            if diff < 0: diff = -1 * diff;
            score = path - diff;

            edges_scores[(prod, cons)] = float(score);

    min_score = (min(edges_scores.values()) 
        if len(edges_scores.values()) > 0
        else 0);
    min_edge = (-1, -1);

    for key, value in edges_scores.items():
        if value == min_score:
            min_edge = key;
            break;

    return [edges_scores, min_edge, min_score];

# поиск пути в графе
def find_path(
    moves, 
    source,  
    dest = -1,
    source_is_cons = False, 
    dest_is_cons = False,
    path = [],
    visited = set()):

    if (dest == -1): dest = source;

    localpath = path.copy();
    localpath.append(source);

    if (source_is_cons):
        for i in range(moves.shape[0]):
            if (moves[i][source] > 0
                and (i, source) not in visited):     
                prod = i;     

                # конец рекурсии - нашли конечную
                if (prod == dest 
                    and dest_is_cons == False):
                    localpath.append(prod);
                    return localpath;

                localvisited = visited.copy();
                localvisited.add((prod, source));            

                retpath = find_path(
                    moves, 
                    prod, 
                    dest, 
                    False, 
                    dest_is_cons, 
                    localpath,
                    localvisited);

                if (len(retpath)):
                    return retpath;
        
    else:
        for j in range(moves.shape[1]):
            if (moves[source][j] > 0
                and (source, j) not in visited):     
                cons = j;     

                # конец рекурсии - нашли конечную
                if (cons == dest 
                    and dest_is_cons == True):
                    localpath.append(cons);
                    return localpath;

                localvisited = visited.copy();
                localvisited.add((source, j));

                retpath = find_path(
                    moves, 
                    cons, 
                    dest, 
                    True, 
                    dest_is_cons, 
                    localpath,
                    localvisited);

                if (len(retpath)):
                    return retpath;            

    # пустой список - через эту вершину цикл найти не удалось
    return [];



# переместить ребро
def move_edge(paths, moves, min_edge):

    # новая матрица перемещений
    m = moves.copy();

    (min_edge_prod, min_edge_cons) = min_edge;

    # поиск замкнутого цикла для добавляемого ребра
    cycle = find_path(
        moves, 
        min_edge_cons, 
        min_edge_prod, 
        True);

    print("Найденный цикл, начиная с поставщика:");
    print(cycle);

    min_value = float("inf");
    new_min_edge = (-1,-1);

    # определяем минимальное противоположное ребро
    for i in range(len(cycle) - 1):
        # интересуют только стрелки из потребителей, 
        # по направлению противоположные
        if (i % 2 == 0):
            (cons, prod) = (cycle[i], cycle[i+1]);

            if moves[prod][cons] < min_value:
                new_min_edge = (prod, cons);
                min_value = moves[prod][cons];

    if (new_min_edge == (-1,-1)): raise Exception("Can't found min move");

    print(f"Минимальная противоположная поставка {min_value} для ребра {new_min_edge}");    

    # определяем новое распределение поставок
    for i in range(len(cycle) - 1):
        
        # вычитаем из противоположных ребер
        # добавляем к попутным
        if (i % 2 == 0):
            (cons, prod) = (cycle[i], cycle[i+1]);
            m[prod][cons] = m[prod][cons] - min_value;
        else:
            (prod, cons) = (cycle[i], cycle[i+1]);
            m[prod][cons] = m[prod][cons] + min_value;


    # новое ребро - перемещение
    m[min_edge_prod][min_edge_cons] = min_value;

    return m;   
        

# решение транспортной задачи
def solve(paths, stocks, needs):

    stage = 1;

    # начальное допустимое опорное решение 
    # методом северо-западного угла
    moves = north_west(
        paths, 
        stocks, 
        needs);

    # начальный граф
    draw_graph(
        paths, 
        stocks, 
        needs, 
        moves,  
        name = f"Начальный_граф");

    while (1):

        # поиск потенциалов узлов
        [u, v] = get_potentials(paths, moves);

        print("Потенциалы поставщиков");
        print(u);

        print("Потенциалы потребителей");
        print(v);

        # поиск оценок ребер без перемещений
        [edges_scores, 
        min_edge, 
        min_score] = find_edges_scores(paths, moves, [u, v]);

        print("Оценки ребер без перемещений");
        print(edges_scores);

        # если среди ребер без перемещений
        # есть отрицательные характеристики, 
        # надо сдвинуть план
        if (min_score < 0):
            print(f"Найдена отрицательная хар-ка {min_score} у ребра {min_edge}");
            moves = move_edge(paths, moves, min_edge);


        # отрисовка графа на текущем шаге
        draw_graph(
            paths, 
            stocks, 
            needs, 
            moves, 
            [u, v], 
            f"Шаг_{stage}");

        # не нашлось отрицательных характеристик
        # план оптимален, выход
        if (min_score >= 0):
            break;

        stage = stage + 1;

    # найдено оптимальное решение, 
    # считаем минимизированное значение
    sum = 0;

    for i in range(paths.shape[0]):
        for j in range(paths.shape[1]):
            if (moves[i][j]):
                sum += moves[i][j] * paths[i][j];

    print(f"Найдено оптимальное решение z={sum}");


# отрисовка графа
def draw_graph(
    paths, # пути от поставщиков к потребителям
    stocks = [], # запасы
    needs = [], # потребности
    moves = [], # движения ресурсов
    potentials = [{},{}], # расчитанные потенциалы
    name = "graph"
    ):

    dot = gv.Digraph(engine="circo");

    nodes = set();

    [u,v] = potentials;

    for i in range(paths.shape[0]):
        for j in range(paths.shape[1]):

            from_node = f"A{i+1}";
            to_node = f"B{j+1}";

            if from_node not in nodes:

                node = f"{from_node}|{stocks[i]}";
                if i in u: node = f"{node}|{u[i]}";

                dot.node(from_node, node);
                nodes.add(from_node);
            
            if to_node not in nodes:

                node = f"{to_node}|{-needs[j]}";
                if j in v: node = f"{node}|{v[j]}";

                dot.node(to_node, node, shape="rect");
                nodes.add(to_node);

            dot.edge(
                from_node, 
                to_node, 
                label=f"{int(paths[i][j])}",
                dir="none");
            
    for i in range(moves.shape[0]):
        for j in range(moves.shape[1]):

            if (moves[i][j] != 0):

                from_node = f"A{i+1}";
                to_node = f"B{j+1}";

                dot.edge(
                    from_node, 
                    to_node, 
                    label=f"{int(moves[i][j])}",
                    color="green",
                    fontcolor="red");

    # dot.graph_attr['ratio'] = "compress";
    dot.graph_attr['size'] = "1920,1080";

    # print(dot.source);
    file = dot.render(f'output/{name}').replace('\\', '/');
    subprocess.run(["cmd", f"/c start {file}"]);

stocks = [80, 170, 150]; # запасы
needs = [70, 60, 180, 90]; # потребности

paths = np.array(
    #B1  B2  B3  B4
    [
    [11,  5,  4,  2], #A1
    [ 1,  4,  5,  9], #A2
    [ 9,  8,  7, 10], #A3
    ], 
    dtype = float);

# опорный план отрузок от поставщиков к потребителям
shipments = np.array(
    # B1   B2   B3   B4
    [
    [  0,   0,   0,  80], #A1
    [ 70,  60,  40,   0], #A2
    [  0,   0, 140,  10], #A3
    ], 
    dtype = float);

solve(paths, stocks, needs);