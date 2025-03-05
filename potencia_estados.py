transition_function = {
    # 1. Mover el cabezal a la derecha hasta llegar al final de la entrada.
    ('right', '0'):     {'write': None, 'move': 'R', 'new_state': 'right'},
    ('right', '1'):     {'write': None, 'move': 'R', 'new_state': 'right'},
    ('right', '^'):     {'write': None, 'move': 'R', 'new_state': 'right'},
    ('right', ' '):     {'write': None, 'move': 'L', 'new_state': 'read'},

    # 2. En el estado "read" se lee el dígito del exponente (desde la parte derecha)
    ('read', '0'):      {'write': 'c',  'move': 'L', 'new_state': 'have0'},
    ('read', '1'):      {'write': 'c',  'move': 'L', 'new_state': 'have1'},
    ('read', '^'):      {'write': ' ',  'move': 'L', 'new_state': 'rewrite'},

    # 3. Retroceder hasta encontrar el operador '^' que separa base y exponente.
    ('have0', '0'):     {'write': None, 'move': 'L', 'new_state': 'have0'},
    ('have0', '1'):     {'write': None, 'move': 'L', 'new_state': 'have0'},
    ('have0', '^'):     {'write': None, 'move': 'L', 'new_state': 'exp0'},

    ('have1', '0'):     {'write': None, 'move': 'L', 'new_state': 'have1'},
    ('have1', '1'):     {'write': None, 'move': 'L', 'new_state': 'have1'},
    ('have1', '^'):     {'write': None, 'move': 'L', 'new_state': 'exp1'},

    # 4. Estados de operación para la potencia:
    # El estado "exp0" se activa cuando el dígito del exponente es 0
    ('exp0', '0'):      {'write': 'O',  'move': 'R', 'new_state': 'exp_back0'},
    ('exp0', ' '):      {'write': 'O',  'move': 'R', 'new_state': 'exp_back0'},
    ('exp0', '1'):      {'write': 'I',  'move': 'R', 'new_state': 'exp_back0'},
    ('exp0', 'O'):      {'write': None, 'move': 'L', 'new_state': 'exp0'},
    ('exp0', 'I'):      {'write': None, 'move': 'L', 'new_state': 'exp0'},

    # El estado "exp1" se activa cuando el dígito del exponente es 1:
    ('exp1', '0'):      {'write': 'I',  'move': 'R', 'new_state': 'exp_back1'},
    ('exp1', ' '):      {'write': 'I',  'move': 'R', 'new_state': 'exp_back1'},
    ('exp1', '1'):      {'write': 'O',  'move': 'L', 'new_state': 'exp_carry'},
    ('exp1', 'O'):      {'write': None, 'move': 'L', 'new_state': 'exp1'},
    ('exp1', 'I'):      {'write': None, 'move': 'L', 'new_state': 'exp1'},

    # 5. Propagación de "acarreo" para el estado "exp1"
    ('exp_carry', '0'): {'write': '1',  'move': 'R', 'new_state': 'exp_back1'},
    ('exp_carry', ' '): {'write': '1',  'move': 'R', 'new_state': 'exp_back1'},
    ('exp_carry', '1'): {'write': '0',  'move': 'L', 'new_state': 'exp_carry'},

    # 6. Retroceder hasta la marca 'c' para completar el ciclo y volver a leer otro dígito del exponente.
    # Se agregan transiciones para el símbolo '^' en ambos estados de retroceso.
    ('exp_back0', '0'): {'write': None, 'move': 'R', 'new_state': 'exp_back0'},
    ('exp_back0', '1'): {'write': None, 'move': 'R', 'new_state': 'exp_back0'},
    ('exp_back0', 'O'): {'write': None, 'move': 'R', 'new_state': 'exp_back0'},
    ('exp_back0', 'I'): {'write': None, 'move': 'R', 'new_state': 'exp_back0'},
    ('exp_back0', '^'): {'write': None, 'move': 'R', 'new_state': 'exp_back0'},
    ('exp_back0', 'c'): {'write': '0',  'move': 'L', 'new_state': 'read'},

    ('exp_back1', '0'): {'write': None, 'move': 'R', 'new_state': 'exp_back1'},
    ('exp_back1', '1'): {'write': None, 'move': 'R', 'new_state': 'exp_back1'},
    ('exp_back1', 'O'): {'write': None, 'move': 'R', 'new_state': 'exp_back1'},
    ('exp_back1', 'I'): {'write': None, 'move': 'R', 'new_state': 'exp_back1'},
    ('exp_back1', '^'): {'write': None, 'move': 'R', 'new_state': 'exp_back1'},
    ('exp_back1', 'c'): {'write': '1',  'move': 'L', 'new_state': 'read'},

    # 7. Reescribir los símbolos temporales ('O' e 'I') a los dígitos definitivos.
    ('rewrite', 'O'):   {'write': '0',  'move': 'L', 'new_state': 'rewrite'},
    ('rewrite', 'I'):   {'write': '1',  'move': 'L', 'new_state': 'rewrite'},
    ('rewrite', '0'):   {'write': None, 'move': 'L', 'new_state': 'rewrite'},
    ('rewrite', '1'):   {'write': None, 'move': 'L', 'new_state': 'rewrite'},
    ('rewrite', ' '):   {'write': None, 'move': 'R', 'new_state': 'done'},

    # Estado final.
    ('done', None):     {'write': None, 'move': None, 'new_state': 'done'}
}