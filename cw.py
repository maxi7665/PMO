import numpy as np;
import networkx as nx;
import matplotlib.pyplot as plt;
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
    
        # print(moves);

    return moves;

# расчет потенциалов
# получить потенциалы
def get_potentials(paths, moves):

    u = dict(); # потенциалы поставщика
    v = dict(); # потенциалы потребителя

    # кол-во u и v
    u_num = paths.shape[0];
    v_num = paths.shape[1];

    # [prod, cons] = moves[0];
    # path = paths[prod][cons];

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
        






# отрисовка графа
def draw_graph(
    paths, # пути от поставщиков к потребителям
    stocks = [], # запасы
    needs = [], # потребности
    moves = [], # движения ресурсов
    potentials = [{},{}] # расчитанные потенциалы
    ):

    # G = nx.Graph();
    dot = gv.Digraph(engine="circo");


    nodes = set();
    edges = [];
    labels = dict();

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

    print(dot.source);
    file = dot.render('doctest-output/round-table.gv').replace('\\', '/');
    subprocess.run(["cmd", f"/c start {file}"]);
    
    
    # G.add_edges_from(edges);

    # pos = nx.spring_layout(G)

    # nx.draw(G, pos, with_labels=True);
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=labels);

    # plt.show();
    #plt.show();

    # G = nx.petersen_graph()
    # subax1 = plt.subplot(121)
    # nx.draw(G, with_labels=True, font_weight='bold')
    # subax2 = plt.subplot(122)
    # nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')




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

moves = north_west(paths, stocks, needs);

print(moves);

[u, v] = get_potentials(paths, moves);

print("Потенциалы поставщиков");
print(u);

print("Потенциалы потребителей");
print(v);

# exit();

draw_graph(paths, stocks, needs, moves, [u, v]);