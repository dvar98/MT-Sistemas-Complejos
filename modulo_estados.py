transition_function = {
    # 1. Recorrer la cinta hacia la derecha hasta encontrar un espacio en blanco.
    ('right', '0'): {'write': None, 'move': 'R', 'new_state': 'right'},
    ('right', '1'): {'write': None, 'move': 'R', 'new_state': 'right'},
    ('right', '%'): {'write': None, 'move': 'R', 'new_state': 'right'},
    ('right', ' '): {'write': None, 'move': 'L', 'new_state': 'read'},

    # 2. Estado "read": leer el dígito del divisor (de derecha a izquierda) y marcarlo con 'c'.
    ('read', '0'): {'write': 'c', 'move': 'L', 'new_state': 'have0'},
    ('read', '1'): {'write': 'c', 'move': 'L', 'new_state': 'have1'},
    # Si se llega al símbolo '%' en vez de un dígito, se entiende que ya no quedan dígitos en el divisor;
    # se procede a reescribir la cinta y finalizar.
    ('read', '%'): {'write': ' ', 'move': 'L', 'new_state': 'rewrite'},

    # 3. Estados "have": retroceder hasta encontrar el separador '%' que divide dividendo y divisor.
    ('have0', '0'): {'write': None, 'move': 'L', 'new_state': 'have0'},
    ('have0', '1'): {'write': None, 'move': 'L', 'new_state': 'have0'},
    ('have0', '%'): {'write': None, 'move': 'L', 'new_state': 'sub0'},

    ('have1', '0'): {'write': None, 'move': 'L', 'new_state': 'have1'},
    ('have1', '1'): {'write': None, 'move': 'L', 'new_state': 'have1'},
    ('have1', '%'): {'write': None, 'move': 'L', 'new_state': 'sub1'},

    # 4. Estados para realizar la sustracción (una “cifra a cifra”) del divisor al dividendo.
    # Estado "sub0": se resta 0 (es decir, el dígito del dividendo se mantiene igual).
    ('sub0', '0'): {'write': '0', 'move': 'R', 'new_state': 'back0'},
    ('sub0', '1'): {'write': '1', 'move': 'R', 'new_state': 'back0'},
    ('sub0', ' '): {'write': '0', 'move': 'R', 'new_state': 'back0'},
    ('sub0', 'O'): {'write': None, 'move': 'L', 'new_state': 'sub0'},
    ('sub0', 'I'): {'write': None, 'move': 'L', 'new_state': 'sub0'},

    # Estado "sub1": se resta 1.
    # Si el dígito del dividendo es 1, 1-1 = 0; si es 0, se produce un "préstamo".
    ('sub1', '1'): {'write': '0', 'move': 'R', 'new_state': 'back0'},
    ('sub1', '0'): {'write': '1', 'move': 'L', 'new_state': 'borrow'},
    ('sub1', ' '): {'write': '1', 'move': 'L', 'new_state': 'borrow'},
    ('sub1', 'O'): {'write': None, 'move': 'L', 'new_state': 'sub1'},
    ('sub1', 'I'): {'write': None, 'move': 'L', 'new_state': 'sub1'},

    # 5. Estado "borrow": manejar el préstamo en la sustracción.
    ('borrow', '0'): {'write': '1', 'move': 'R', 'new_state': 'back1'},
    ('borrow', '1'): {'write': '0', 'move': 'L', 'new_state': 'borrow'},
    ('borrow', ' '): {'write': '1', 'move': 'R', 'new_state': 'back1'},

    # 6. Estados "back": avanzar hacia la derecha hasta encontrar el marcador 'c',
    # para luego borrar el marcador y volver al estado "read" para procesar el siguiente dígito del divisor.
    ('back0', '0'): {'write': None, 'move': 'R', 'new_state': 'back0'},
    ('back0', '1'): {'write': None, 'move': 'R', 'new_state': 'back0'},
    ('back0', 'O'): {'write': None, 'move': 'R', 'new_state': 'back0'},
    ('back0', 'I'): {'write': None, 'move': 'R', 'new_state': 'back0'},
    ('back0', '%'): {'write': None, 'move': 'R', 'new_state': 'back0'},
    ('back0', 'c'): {'write': '0', 'move': 'L', 'new_state': 'read'},

    ('back1', '0'): {'write': None, 'move': 'R', 'new_state': 'back1'},
    ('back1', '1'): {'write': None, 'move': 'R', 'new_state': 'back1'},
    ('back1', 'O'): {'write': None, 'move': 'R', 'new_state': 'back1'},
    ('back1', 'I'): {'write': None, 'move': 'R', 'new_state': 'back1'},
    ('back1', '%'): {'write': None, 'move': 'R', 'new_state': 'back1'},
    ('back1', 'c'): {'write': '1', 'move': 'L', 'new_state': 'read'},

    # 7. Estado "rewrite": se recorre la cinta para transformar los símbolos temporales (si los hubiera)
    # en dígitos definitivos y dejar el resultado final (el módulo, que es el residuo en el dividendo).
    ('rewrite', 'O'): {'write': '0', 'move': 'L', 'new_state': 'rewrite'},
    ('rewrite', 'I'): {'write': '1', 'move': 'L', 'new_state': 'rewrite'},
    ('rewrite', '0'): {'write': None, 'move': 'L', 'new_state': 'rewrite'},
    ('rewrite', '1'): {'write': None, 'move': 'L', 'new_state': 'rewrite'},
    ('rewrite', ' '): {'write': None, 'move': 'R', 'new_state': 'done'},

    # Estado final.
    ('done', None): {'write': None, 'move': None, 'new_state': 'done'}
}