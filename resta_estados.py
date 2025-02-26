transition_function = {
    # Estado "right": se busca en el operando izquierdo una '1' sin cancelar.
    ('right', '1'): {'write': 'X', 'move': 'R', 'new_state': 'seek_sep'},
    ('right', 'X'): {'write': None, 'move': 'R', 'new_state': 'right'},
    ('right', 'B'): {'write': None, 'move': 'R', 'new_state': 'right'},
    ('right', '-'): {'write': None, 'move': 'R', 'new_state': 'done'},
    ('right', ' '): {'write': None, 'move': 'R', 'new_state': 'done'},

    # Estado "seek_sep": se avanza hasta encontrar el separador '-' para pasar al operando derecho.
    ('seek_sep', '1'): {'write': None, 'move': 'R', 'new_state': 'seek_sep'},
    ('seek_sep', 'B'): {'write': None, 'move': 'R', 'new_state': 'seek_sep'},
    ('seek_sep', 'X'): {'write': None, 'move': 'R', 'new_state': 'seek_sep'},
    ('seek_sep', '-'): {'write': None, 'move': 'R', 'new_state': 'erase'},
    ('seek_sep', ' '): {'write': None, 'move': 'R', 'new_state': 'done'},

    # Estado "erase": en el operando derecho se busca una '1' que cancelar.
    ('erase', '1'): {'write': 'B', 'move': 'L', 'new_state': 'back'},
    ('erase', 'B'): {'write': None, 'move': 'R', 'new_state': 'erase'},
    ('erase', '-'): {'write': None, 'move': 'R', 'new_state': 'erase'},
    ('erase', 'X'): {'write': None, 'move': 'R', 'new_state': 'erase'},
    ('erase', ' '): {'write': None, 'move': 'L', 'new_state': 'done'},

    # Estado "back": retroceder hasta encontrar el marcador 'X' en el operando izquierdo;
    # luego se cambia 'X' por 'B' (cancelado) y se vuelve a empezar.
    ('back', 'X'): {'write': 'B', 'move': 'R', 'new_state': 'right'},
    ('back', '1'): {'write': None, 'move': 'L', 'new_state': 'back'},
    ('back', 'B'): {'write': None, 'move': 'L', 'new_state': 'back'},
    ('back', '-'): {'write': None, 'move': 'L', 'new_state': 'back'},
    ('back', ' '): {'write': None, 'move': 'L', 'new_state': 'back'},

    # Estado final "done": la resta ha terminado.
    ('done', None): {'write': None, 'move': None, 'new_state': 'done'}
}