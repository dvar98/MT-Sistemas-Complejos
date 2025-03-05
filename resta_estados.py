transition_function = {
    # Estado "right": recorre la cinta hasta el final
    ('right', '0'): {'write': None, 'move': 'R', 'new_state': 'right'},
    ('right', '1'): {'write': None, 'move': 'R', 'new_state': 'right'},
    ('right', '-'): {'write': None, 'move': 'R', 'new_state': 'right'},
    ('right', ' '): {'write': None, 'move': 'L', 'new_state': 'read'},

    # Estado "read": lee el dígito del sustraendo y lo marca con 'c'
    ('read', '0'): {'write': 'c', 'move': 'L', 'new_state': 'have0'},
    ('read', '1'): {'write': 'c', 'move': 'L', 'new_state': 'have1'},
    ('read', '-'): {'write': ' ', 'move': 'L', 'new_state': 'rewrite'},

    # Estados "have": se mueve a la izquierda hasta encontrar el operador '-'
    ('have0', '0'): {'write': None, 'move': 'L', 'new_state': 'have0'},
    ('have0', '1'): {'write': None, 'move': 'L', 'new_state': 'have0'},
    ('have0', '-'): {'write': None, 'move': 'L', 'new_state': 'sub0'},

    ('have1', '0'): {'write': None, 'move': 'L', 'new_state': 'have1'},
    ('have1', '1'): {'write': None, 'move': 'L', 'new_state': 'have1'},
    ('have1', '-'): {'write': None, 'move': 'L', 'new_state': 'sub1'},

    # Estados "sub": se efectúa la resta sobre el dígito del minuendo
    # En "sub0" se resta 0 (no se genera préstamo)
    ('sub0', '0'): {'write': 'O', 'move': 'R', 'new_state': 'back0'},
    ('sub0', '1'): {'write': 'I', 'move': 'R', 'new_state': 'back0'},
    ('sub0', ' '): {'write': 'O', 'move': 'R', 'new_state': 'back0'},
    ('sub0', 'O'): {'write': None, 'move': 'L', 'new_state': 'sub0'},
    ('sub0', 'I'): {'write': None, 'move': 'L', 'new_state': 'sub0'},

    # En "sub1" se resta 1 (de 1 se obtiene 0 sin préstamo; de 0 se obtiene 1 y se genera préstamo)
    ('sub1', '0'): {'write': 'I', 'move': 'L', 'new_state': 'borrow'},  # 0 - 1: genera préstamo
    ('sub1', '1'): {'write': 'O', 'move': 'R', 'new_state': 'back0'},    # 1 - 1: sin préstamo
    ('sub1', ' '): {'write': 'I', 'move': 'L', 'new_state': 'borrow'},
    ('sub1', 'O'): {'write': None, 'move': 'L', 'new_state': 'sub1'},
    ('sub1', 'I'): {'write': None, 'move': 'L', 'new_state': 'sub1'},

    # Estado "borrow": propaga el préstamo a la siguiente posición del minuendo
    # Si se encuentra un 0 se sigue prestando; si se encuentra un 1 se cancela el préstamo (1-1=0)
    ('borrow', '0'): {'write': 'I', 'move': 'L', 'new_state': 'borrow'},
    ('borrow', '1'): {'write': 'O', 'move': 'R', 'new_state': 'back1'},
    ('borrow', ' '): {'write': 'I', 'move': 'L', 'new_state': 'borrow'},
    ('borrow', 'O'): {'write': None, 'move': 'L', 'new_state': 'borrow'},
    ('borrow', 'I'): {'write': None, 'move': 'L', 'new_state': 'borrow'},

    # Estados "back": se mueve a la derecha hasta encontrar el marcador 'c'
    ('back0', '0'): {'write': None, 'move': 'R', 'new_state': 'back0'},
    ('back0', '1'): {'write': None, 'move': 'R', 'new_state': 'back0'},
    ('back0', 'O'): {'write': None, 'move': 'R', 'new_state': 'back0'},
    ('back0', 'I'): {'write': None, 'move': 'R', 'new_state': 'back0'},
    ('back0', '-'): {'write': None, 'move': 'R', 'new_state': 'back0'},
    ('back0', 'c'): {'write': '0', 'move': 'L', 'new_state': 'read'},

    ('back1', '0'): {'write': None, 'move': 'R', 'new_state': 'back1'},
    ('back1', '1'): {'write': None, 'move': 'R', 'new_state': 'back1'},
    ('back1', 'O'): {'write': None, 'move': 'R', 'new_state': 'back1'},
    ('back1', 'I'): {'write': None, 'move': 'R', 'new_state': 'back1'},
    ('back1', '-'): {'write': None, 'move': 'R', 'new_state': 'back1'},
    ('back1', 'c'): {'write': '1', 'move': 'L', 'new_state': 'read'},

    # Estado "rewrite": se recorre la cinta y se transforman los símbolos temporales ('O' e 'I')
    # en los dígitos finales (0 y 1)
    ('rewrite', 'O'): {'write': '0', 'move': 'L', 'new_state': 'rewrite'},
    ('rewrite', 'I'): {'write': '1', 'move': 'L', 'new_state': 'rewrite'},
    ('rewrite', '0'): {'write': None, 'move': 'L', 'new_state': 'rewrite'},
    ('rewrite', '1'): {'write': None, 'move': 'L', 'new_state': 'rewrite'},
    ('rewrite', ' '): {'write': None, 'move': 'R', 'new_state': 'done'},

    # Estado "done": estado de detención de la máquina
    ('done', None): {'write': None, 'move': None, 'new_state': 'done'}
}