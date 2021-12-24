"""sir_plott.py"""

import plotly.graph_objects as go
import numpy as np


# tree node : ( list of edges to its children , level , label_name  )
# tree key node is sorted by level-traversal
# tree = sample4 = {1: ([(1, 2)], 0, 'READ (x)', 'square'),
#                   2: ([(2, 3), (2, 6)], 0, 'IF', 'square'),
#                   3: ([(3, 4), (3, 5)], 1, 'LESSTHAN (<)', 'circle'),
#                   4: ([], 2, 'NUMBER (0)', 'circle'),
#                   5: ([], 2, 'IDENTIFIER (x)', 'circle'),
#                   6: ([(6, 7), (6, 8)], 1, 'ASSIGN (fact)', 'square'),
#                   7: ([], 2, 'number (1)', 'circle'),
#                   8: ([(8, 9), (8, 17), (8, 20)], 1, 'REPEAT', 'square'),
#                   9: ([(9, 10), (9, 13)], 2, 'ASSIGN (fact)', 'square'),
#                   10: ([(10, 11), (10, 12)], 3, 'MULT (*)', 'circle'),
#                   11: ([], 4, 'IDENTIFIER (fact)', 'circle'),
#                   12: ([], 4, 'IDENTIFIER (x)', 'circle'),
#                   13: ([(13, 14)], 2, 'ASSIGN (x)', 'square'),
#                   14: ([(14, 15), (14, 16)], 3, 'MINUS (-)', 'circle'),
#                   15: ([], 4, 'IDENTIFIER (x)', 'circle'),
#                   16: ([], 4, 'NUMBER (1)', 'circle'),
#                   17: ([(17, 18), (17, 19)], 2, 'EQUAL (=)', 'circle'),
#                   18: ([], 3, 'IDENTIFIER (x)', 'circle'),
#                   19: ([], 3, 'NUMBER (0)', 'circle'),
#                   20: ([(20, 21)], 1, 'WRITE', 'square'),
#                   21: ([], 2, 'IDENTIFIER (fact)', 'circle')}

#sq_cr_switch = list([True]*10+[False]*3)


def data_framer(tree: dict, x_sep: float) -> (list, list, list, list, list):
    """

    """

    def input_tree_dict(tree: dict) -> (list, list, list, list):
        edges = []
        #edges +=[ v[0] for  k,v in tree.items()]

        for _, v in tree.items():
            edges += v[0]
        labels = [v[2] for _, v in tree.items()]
        levels = [val[1] for _, val in tree.items()]
        sq_cr_switch = [str(val[-1]).lower() for _, val in tree.items()]

        return edges, labels, levels, sq_cr_switch

    edges, labels, levels, sq_cr_switch = input_tree_dict(tree)

    "hyperpramerters"
    #x_sep = 2
    # appeared to have no impact
    # center_x = 1 # ex
    ymax = 0

    # y values for each node
    Y = [ymax-val for val in levels]
    # number of children in ervey level
    child_count = dict()
    ch = []
    for _, val in tree.items():
        child_count[val[1]] = child_count.get(val[1], 0) + 1
        ch.append(child_count[val[1]])

    X = [ch[i]*2 - val*x_sep for i, val in enumerate(levels)]

    edges_pos_x = []
    edges_pos_y = []
    for edge in edges:
        edges_pos_x += [X[edge[0]-1], X[edge[1]-1], None]
        edges_pos_y += [Y[edge[0]-1], Y[edge[1]-1], None]

    return X, Y, edges_pos_x, edges_pos_y, labels, sq_cr_switch


def make_annotations(X, Y, text, labels, font_size=10, font_color='rgb(250,250,250)'):
    L = len(X)
    if len(text) != L:
        raise ValueError('The lists pos and text must have the same len')
    annotations = []
    for k in range(L):
        annotations.append(
            dict(
                # or replace labels with a different list for the text within the circle
                text=labels[k],
                x=X[k], y=Y[k]+.24,
                xref='x1', yref='y1',
                font=dict(color=font_color, size=font_size),
                showarrow=False)
        )
    return annotations


def MR_Fantastic_tree_plotter_without_root_or_linux(tree: dict, x_sep: str = 2, square_color: str = 'cyan ', circle_color='rgb(199,21,133)') -> None:
    "function el primo"

    def plot(labels: list, colors: list) -> None:

        fig = go.Figure()
        """'inferno'
        viridis
        magma
        thermal
        Emrld
        magenta
        plotly3
        """
        'LightSkyBlue'
        fig.add_trace(go.Scatter(x=edges_pos_x,
                                 y=edges_pos_y,
                                 mode='lines',
                                 line=dict(color='rgb(210,210,210)', width=4),
                                 hoverinfo='none'
                                 ))
        fig.add_trace(go.Scatter(x=X,
                                 y=Y,
                                 mode='markers',
                                 name='noice graph baby',
                                 marker=dict(
                                     symbol=sq_cr_switch,
                                     size=40,
                                     color=colors,
                                     # colorscale='plotly3', # one of plotly colorscales
                                     #line=dict(color='green', width=1),
                                 ),
                                 text=labels,
                                 hoverinfo='text',
                                 opacity=0.9
                                 ))
        axis = dict(showline=False,  # hide axis line, grid, ticklabels and  title
                    zeroline=False,
                    showgrid=False,
                    showticklabels=False,
                    )
        # v_label=list(str(len(labels)))*len(labels)
        fig.update_layout(title='Parse Tree',
                          annotations=make_annotations(
                              X, Y, labels, labels, font_color='rgb(0,0,0)'),
                          font_size=15,
                          showlegend=False,
                          xaxis=axis,
                          yaxis=axis,
                          # marker_symbol='square',
                          # marker_symbol='cross',
                          margin=dict(l=40, r=40, b=85, t=100),
                          hovermode='closest',
                          plot_bgcolor='rgb(248,248,248)'
                          )
        fig.update_traces(marker_size=40)
        fig.show()

    X, Y, edges_pos_x, edges_pos_y, labels, sq_cr_switch = data_framer(
        tree, x_sep)
    colors = []
    for i, val in enumerate(sq_cr_switch):
        if val == 'square':
            colors.append(square_color)
        else:
            colors.append(circle_color)

    plot(labels, colors)


# def __main__():
#     pass


# if __name__ == '__main__':
#     MR_Fantastic_tree_plotter_without_root_or_linux(tree, 2)
