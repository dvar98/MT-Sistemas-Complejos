# potencia_estados.py

transition_function = {
    # 1. Mover a la derecha hasta encontrar un espacio en blanco
    ('right', '0'): {'write': None, 'move': 'R', 'new_state': 'right'},
    ('right', '1'): {'write': None, 'move': 'R', 'new_state': 'right'},
    ('right', '^'): {'write': None, 'move': 'R', 'new_state': 'right'},
    ('right', ' '): {'write': None, 'move': 'L', 'new_state': 'check_exp'},

    # 2. En "check_exp", leer el primer dígito del exponente:
    #    Si es '0' → se procederá a borrar la base para dejar solo "1"
    ('check_exp', '0'): {'write': None, 'move': 'L', 'new_state': 'erase_base'},
    #    Si es '1' → se pasa a revisar si hay segundo dígito (para distinguir exponente 1 o 2)
    ('check_exp', '1'): {'write': None, 'move': 'R', 'new_state': 'check_exp_second'},

    # 3. En "check_exp_second", si se encuentra '0' se interpreta como exponente "10" (2),
    #    de lo contrario (si es blank) el exponente es 1.
    ('check_exp_second', '0'): {'write': None, 'move': 'L', 'new_state': 'do_multiplication'},
    ('check_exp_second', ' '): {'write': None, 'move': 'L', 'new_state': 'erase_exponent'},

    # 4. Caso exponente 0: borrar la base y escribir "1"
    #    Estado "erase_base": se mueve a la izquierda borrando los dígitos de la base y el operador '^'.
    ('erase_base', '0'): {'write': ' ', 'move': 'L', 'new_state': 'erase_base'},
    ('erase_base', '1'): {'write': ' ', 'move': 'L', 'new_state': 'erase_base'},
    ('erase_base', '^'): {'write': ' ', 'move': 'L', 'new_state': 'erase_base'},
    #    Cuando se encuentra un espacio (fuera de la base), se pasa a "write_one"
    ('erase_base', ' '): {'write': None, 'move': 'R', 'new_state': 'write_one'},
    #    En "write_one" se escribe el "1" y se pasa al estado final.
    ('write_one', ' '): {'write': '1', 'move': 'R', 'new_state': 'done'},

    # 5. Caso exponente 1: borrar la parte del exponente y dejar la base intacta
    ('erase_exponent', '^'): {'write': ' ', 'move': 'R', 'new_state': 'erase_exponent'},
    ('erase_exponent', '0'): {'write': ' ', 'move': 'R', 'new_state': 'erase_exponent'},
    ('erase_exponent', '1'): {'write': ' ', 'move': 'R', 'new_state': 'erase_exponent'},
    ('erase_exponent', ' '): {'write': None, 'move': 'R', 'new_state': 'done'},

    # 6. Caso exponente 2: se realizará una multiplicación (base * base).
    #    Estado "do_multiplication": borrar el separador y los dígitos del exponente,
    #    y al llegar a un espacio se inserta '*' para simular "base * base"
    ('do_multiplication', '^'): {'write': ' ', 'move': 'R', 'new_state': 'do_multiplication'},
    ('do_multiplication', '0'): {'write': ' ', 'move': 'R', 'new_state': 'do_multiplication'},
    ('do_multiplication', '1'): {'write': ' ', 'move': 'R', 'new_state': 'do_multiplication'},
    ('do_multiplication', ' '): {'write': '*', 'move': 'L', 'new_state': 'read'},

    # 7. Fase de multiplicación (se reusa la lógica de multiplicacion_estados)
    ('read', '0'):   {'write': 'c',  'move': 'L', 'new_state': 'have0'},
    ('read', '1'):   {'write': 'c',  'move': 'L', 'new_state': 'have1'},
    ('read', '*'):   {'write': ' ',  'move': 'L', 'new_state': 'rewrite'},

    ('have0', '0'):  {'write': None, 'move': 'L', 'new_state': 'have0'},
    ('have0', '1'):  {'write': None, 'move': 'L', 'new_state': 'have0'},
    ('have0', '*'):  {'write': None, 'move': 'L', 'new_state': 'mul0'},

    ('have1', '0'):  {'write': None, 'move': 'L', 'new_state': 'have1'},
    ('have1', '1'):  {'write': None, 'move': 'L', 'new_state': 'have1'},
    ('have1', '*'):  {'write': None, 'move': 'L', 'new_state': 'mul1'},

    ('mul0', '0'):      {'write': 'O',  'move': 'R', 'new_state': 'back0'},
    ('mul0', ' '):      {'write': 'O',  'move': 'R', 'new_state': 'back0'},
    ('mul0', '1'):      {'write': 'I',  'move': 'R', 'new_state': 'back0'},
    ('mul0', 'O'):      {'write': None, 'move': 'L', 'new_state': 'mul0'},
    ('mul0', 'I'):      {'write': None, 'move': 'L', 'new_state': 'mul0'},

    ('mul1', '0'):      {'write': 'I',  'move': 'R', 'new_state': 'back1'},
    ('mul1', ' '):      {'write': 'I',  'move': 'R', 'new_state': 'back1'},
    ('mul1', '1'):      {'write': 'O',  'move': 'L', 'new_state': 'carry'},
    ('mul1', 'O'):      {'write': None, 'move': 'L', 'new_state': 'mul1'},
    ('mul1', 'I'):      {'write': None, 'move': 'L', 'new_state': 'mul1'},

    ('carry', '0'):     {'write': '1',  'move': 'R', 'new_state': 'back1'},
    ('carry', ' '):     {'write': '1',  'move': 'R', 'new_state': 'back1'},
    ('carry', '1'):     {'write': '0',  'move': 'L', 'new_state': 'carry'},

    ('back0', '0'):    {'write': None, 'move': 'R', 'new_state': 'back0'},
    ('back0', '1'):    {'write': None, 'move': 'R', 'new_state': 'back0'},
    ('back0', 'O'):    {'write': None, 'move': 'R', 'new_state': 'back0'},
    ('back0', 'I'):    {'write': None, 'move': 'R', 'new_state': 'back0'},
    ('back0', '*'):    {'write': None, 'move': 'R', 'new_state': 'back0'},
    ('back0', 'c'):    {'write': '0',  'move': 'L', 'new_state': 'read'},

    ('back1', '0'):    {'write': None, 'move': 'R', 'new_state': 'back1'},
    ('back1', '1'):    {'write': None, 'move': 'R', 'new_state': 'back1'},
    ('back1', 'O'):    {'write': None, 'move': 'R', 'new_state': 'back1'},
    ('back1', 'I'):    {'write': None, 'move': 'R', 'new_state': 'back1'},
    ('back1', '*'):    {'write': None, 'move': 'R', 'new_state': 'back1'},
    ('back1', 'c'):    {'write': '1',  'move': 'L', 'new_state': 'read'},

    ('rewrite', 'O'): {'write': '0',  'move': 'L', 'new_state': 'rewrite'},
    ('rewrite', 'I'): {'write': '1',  'move': 'L', 'new_state': 'rewrite'},
    ('rewrite', '0'): {'write': None, 'move': 'L', 'new_state': 'rewrite'},
    ('rewrite', '1'): {'write': None, 'move': 'L', 'new_state': 'rewrite'},
    ('rewrite', ' '): {'write': None, 'move': 'R', 'new_state': 'done'},

    # Estado final
    ('done', None):   {'write': None, 'move': None, 'new_state': 'done'}
}