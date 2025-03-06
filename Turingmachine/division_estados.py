transition_function = {
    # 1. Mover el cabezal a la derecha hasta llegar al final de la entrada.
    ('right', '0'): {'write': None, 'move': 'R', 'new_state': 'right'},
    ('right', '1'): {'write': None, 'move': 'R', 'new_state': 'right'},
    ('right', '/'): {'write': None, 'move': 'R', 'new_state': 'right'},
    ('right', ' '): {'write': None, 'move': 'L', 'new_state': 'check'},
    
    # 2. Retroceder hasta encontrar el separador '/'.
    ('check', '0'): {'write': None, 'move': 'L', 'new_state': 'check'},
    ('check', '1'): {'write': None, 'move': 'L', 'new_state': 'check'},
    ('check', '/'): {'write': None, 'move': 'L', 'new_state': 'prepare'},
    
    # 3. Preparar la sustracción: marcar el dígito del dividendo.
    ('prepare', '0'): {'write': 'c', 'move': 'L', 'new_state': 'd_have0'},
    ('prepare', '1'): {'write': 'c', 'move': 'L', 'new_state': 'd_have1'},
    ('prepare', ' '): {'write': None, 'move': 'R', 'new_state': 'finish_division'},
    
    # 4. Retroceder en el dividendo hasta encontrar el separador '/'.
    ('d_have0', '0'): {'write': None, 'move': 'L', 'new_state': 'd_have0'},
    ('d_have0', '1'): {'write': None, 'move': 'L', 'new_state': 'd_have0'},
    ('d_have0', '/'): {'write': None, 'move': 'L', 'new_state': 'div_sub0'},
    ('d_have0', ' '): {'write': None, 'move': 'R', 'new_state': 'finish_division'},  # TRANSICIÓN AGREGADA
    
    ('d_have1', '0'): {'write': None, 'move': 'L', 'new_state': 'd_have1'},
    ('d_have1', '1'): {'write': None, 'move': 'L', 'new_state': 'd_have1'},
    ('d_have1', '/'): {'write': None, 'move': 'L', 'new_state': 'div_sub1'},
    ('d_have1', ' '): {'write': None, 'move': 'R', 'new_state': 'finish_division'},  # TRANSICIÓN AGREGADA
    
    # 5. Realizar la sustracción parcial del divisor.
    # Se utilizan símbolos temporales: 'O' para representar 0 e 'I' para representar 1.
    ('div_sub0', '0'): {'write': 'O', 'move': 'R', 'new_state': 'd_back0'},
    ('div_sub0', ' '): {'write': 'O', 'move': 'R', 'new_state': 'd_back0'},
    ('div_sub0', '1'): {'write': 'I', 'move': 'R', 'new_state': 'd_back0'},
    ('div_sub0', 'O'): {'write': None, 'move': 'L', 'new_state': 'div_sub0'},
    ('div_sub0', 'I'): {'write': None, 'move': 'L', 'new_state': 'div_sub0'},
    
    ('div_sub1', '0'): {'write': 'I', 'move': 'L', 'new_state': 'd_borrow'},
    ('div_sub1', '1'): {'write': 'O', 'move': 'R', 'new_state': 'd_back0'},
    ('div_sub1', ' '): {'write': 'I', 'move': 'L', 'new_state': 'd_borrow'},
    ('div_sub1', 'O'): {'write': None, 'move': 'L', 'new_state': 'div_sub1'},
    ('div_sub1', 'I'): {'write': None, 'move': 'L', 'new_state': 'div_sub1'},
    
    # 6. Manejar el préstamo si la sustracción lo requiere.
    ('d_borrow', '0'): {'write': '1', 'move': 'R', 'new_state': 'd_back1'},
    ('d_borrow', ' '): {'write': '1', 'move': 'R', 'new_state': 'd_back1'},
    ('d_borrow', '1'): {'write': '0', 'move': 'L', 'new_state': 'd_borrow'},
    
    # 7. Retroceder hasta la marca 'c' para finalizar la sustracción parcial.
    ('d_back0', '0'): {'write': None, 'move': 'R', 'new_state': 'd_back0'},
    ('d_back0', '1'): {'write': None, 'move': 'R', 'new_state': 'd_back0'},
    ('d_back0', 'O'): {'write': None, 'move': 'R', 'new_state': 'd_back0'},
    ('d_back0', 'I'): {'write': None, 'move': 'R', 'new_state': 'd_back0'},
    ('d_back0', 'c'): {'write': '0', 'move': 'L', 'new_state': 'record_quotient'},
    
    ('d_back1', '0'): {'write': None, 'move': 'R', 'new_state': 'd_back1'},
    ('d_back1', '1'): {'write': None, 'move': 'R', 'new_state': 'd_back1'},
    ('d_back1', 'O'): {'write': None, 'move': 'R', 'new_state': 'd_back1'},
    ('d_back1', 'I'): {'write': None, 'move': 'R', 'new_state': 'd_back1'},
    ('d_back1', 'c'): {'write': '1', 'move': 'L', 'new_state': 'record_quotient'},
    
    # 8. Registrar un dígito en el cociente por cada sustracción exitosa.
    # En este ejemplo usamos 'X' para indicar un dígito del cociente.
    ('record_quotient', '0'): {'write': 'X', 'move': 'R', 'new_state': 'reset'},
    ('record_quotient', '1'): {'write': 'X', 'move': 'R', 'new_state': 'reset'},
    ('record_quotient', ' '): {'write': 'X', 'move': 'R', 'new_state': 'reset'},
    ('record_quotient', 'X'): {'write': 'X', 'move': 'R', 'new_state': 'reset'},
    
    # 9. Restablecer los símbolos temporales y posicionar el cabezal para intentar otra sustracción.
    ('reset', 'O'): {'write': '0', 'move': 'R', 'new_state': 'reset'},
    ('reset', 'I'): {'write': '1', 'move': 'R', 'new_state': 'reset'},
    ('reset', '/'): {'write': '/', 'move': 'R', 'new_state': 'right'},
    ('reset', '0'): {'write': None, 'move': 'R', 'new_state': 'reset'},
    ('reset', '1'): {'write': None, 'move': 'R', 'new_state': 'reset'},
    ('reset', ' '): {'write': None, 'move': 'R', 'new_state': 'right'},
    
    # 10. Finalizar la división: reescribir los símbolos temporales para dejar el resultado final.
    ('finish_division', 'O'): {'write': '0', 'move': 'L', 'new_state': 'finish_division'},
    ('finish_division', 'I'): {'write': '1', 'move': 'L', 'new_state': 'finish_division'},
    ('finish_division', '0'): {'write': None, 'move': 'L', 'new_state': 'finish_division'},
    ('finish_division', '1'): {'write': None, 'move': 'L', 'new_state': 'finish_division'},
    ('finish_division', 'c'): {'write': ' ', 'move': 'L', 'new_state': 'finish_division'},  # NUEVA TRANSICIÓN PARA LIMPIAR 'c'
    ('finish_division', ' '): {'write': None, 'move': 'R', 'new_state': 'done'},
    
    # Estado final.
    ('done', None): {'write': None, 'move': None, 'new_state': 'done'}
}