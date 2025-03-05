transition_function = {
    # 1. Mover a la derecha hasta encontrar un espacio en blanco
    ('right', '0'):  {'write': None, 'move': 'R', 'new_state': 'right'},
    ('right', '1'):  {'write': None, 'move': 'R', 'new_state': 'right'},
    ('right', '*'):  {'write': None, 'move': 'R', 'new_state': 'right'},
    ('right', ' '):  {'write': None, 'move': 'L', 'new_state': 'read'},

    # 2. Leer el dígito del multiplicador (derecha) y marcarlo
    ('read', '0'):   {'write': 'c',  'move': 'L', 'new_state': 'have0'},
    ('read', '1'):   {'write': 'c',  'move': 'L', 'new_state': 'have1'},
    ('read', '*'):   {'write': ' ',  'move': 'L', 'new_state': 'rewrite'},

    # 3. Retroceder hasta encontrar el separador '*' que delimita multiplicando y multiplicador
    ('have0', '0'):  {'write': None, 'move': 'L', 'new_state': 'have0'},
    ('have0', '1'):  {'write': None, 'move': 'L', 'new_state': 'have0'},
    ('have0', '*'):  {'write': None, 'move': 'L', 'new_state': 'mul0'},

    ('have1', '0'):  {'write': None, 'move': 'L', 'new_state': 'have1'},
    ('have1', '1'):  {'write': None, 'move': 'L', 'new_state': 'have1'},
    ('have1', '*'):  {'write': None, 'move': 'L', 'new_state': 'mul1'},

    # 4. Procesar la “suma” (o acumulación) de acuerdo al dígito leído del multiplicador
    #    (La notación 'O' e 'I' se usan como símbolos temporales para el 0 y el 1, respectivamente)
    ('mul0', '0'):   {'write': 'O',  'move': 'R', 'new_state': 'back0'},
    ('mul0', ' '):   {'write': 'O',  'move': 'R', 'new_state': 'back0'},
    ('mul0', '1'):   {'write': 'I',  'move': 'R', 'new_state': 'back0'},
    ('mul0', 'O'):   {'write': None, 'move': 'L', 'new_state': 'mul0'},
    ('mul0', 'I'):   {'write': None, 'move': 'L', 'new_state': 'mul0'},

    ('mul1', '0'):   {'write': 'I',  'move': 'R', 'new_state': 'back1'},
    ('mul1', ' '):   {'write': 'I',  'move': 'R', 'new_state': 'back1'},
    ('mul1', '1'):   {'write': 'O',  'move': 'L', 'new_state': 'carry'},
    ('mul1', 'O'):   {'write': None, 'move': 'L', 'new_state': 'mul1'},
    ('mul1', 'I'):   {'write': None, 'move': 'L', 'new_state': 'mul1'},

    # 5. Propagar el acarreo (similar a la suma)
    ('carry', '0'):  {'write': '1',  'move': 'R', 'new_state': 'back1'},
    ('carry', ' '):  {'write': '1',  'move': 'R', 'new_state': 'back1'},
    ('carry', '1'):  {'write': '0',  'move': 'L', 'new_state': 'carry'},

    # 6. Volver a la zona de lectura para procesar el siguiente dígito del multiplicador
    ('back0', '0'):  {'write': None, 'move': 'R', 'new_state': 'back0'},
    ('back0', '1'):  {'write': None, 'move': 'R', 'new_state': 'back0'},
    ('back0', 'O'):  {'write': None, 'move': 'R', 'new_state': 'back0'},
    ('back0', 'I'):  {'write': None, 'move': 'R', 'new_state': 'back0'},
    ('back0', '*'):  {'write': None, 'move': 'R', 'new_state': 'back0'},
    ('back0', 'c'):  {'write': '0',  'move': 'L', 'new_state': 'read'},

    ('back1', '0'):  {'write': None, 'move': 'R', 'new_state': 'back1'},
    ('back1', '1'):  {'write': None, 'move': 'R', 'new_state': 'back1'},
    ('back1', 'O'):  {'write': None, 'move': 'R', 'new_state': 'back1'},
    ('back1', 'I'):  {'write': None, 'move': 'R', 'new_state': 'back1'},
    ('back1', '*'):  {'write': None, 'move': 'R', 'new_state': 'back1'},
    ('back1', 'c'):  {'write': '1',  'move': 'L', 'new_state': 'read'},

    # 7. Una vez terminada la suma acumulativa (o al llegar al separador) se reescribe la cinta
    ('rewrite', 'O'): {'write': '0',  'move': 'L', 'new_state': 'rewrite'},
    ('rewrite', 'I'): {'write': '1',  'move': 'L', 'new_state': 'rewrite'},
    ('rewrite', '0'): {'write': None, 'move': 'L', 'new_state': 'rewrite'},
    ('rewrite', '1'): {'write': None, 'move': 'L', 'new_state': 'rewrite'},
    ('rewrite', ' '): {'write': None, 'move': 'R', 'new_state': 'done'},

    # 8. Estado final
    ('done', None):   {'write': None, 'move': None, 'new_state': 'done'}
}