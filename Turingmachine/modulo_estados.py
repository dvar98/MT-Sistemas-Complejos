transition_function = {
    #
    # 1) Estado 'right': avanza hacia la derecha hasta toparse con un espacio.
    #    Luego retrocede una posición y pasa a 'check'.
    #
    ('right', '0'): {'write': None, 'move': 'R', 'new_state': 'right'},
    ('right', '1'): {'write': None, 'move': 'R', 'new_state': 'right'},
    ('right', '%'): {'write': None, 'move': 'R', 'new_state': 'right'},
    ('right', ' '): {'write': None, 'move': 'L', 'new_state': 'check'},

    #
    # 2) Estado 'check': retrocede hasta encontrar '%'.
    #    Entonces mueve la cabeza una posición a la derecha y pasa a 'prepare'.
    #
    ('check', '0'): {'write': None, 'move': 'L', 'new_state': 'check'},
    ('check', '1'): {'write': None, 'move': 'L', 'new_state': 'check'},
    ('check', '%'): {'write': None, 'move': 'R', 'new_state': 'prepare'},

    #
    # 3) Estado 'prepare': busca un dígito del DIVIDENDO.
    #    - Si encuentra '0', lo marca como 'c' y pasa a 'd_have0'.
    #    - Si encuentra '1', lo marca como 'c' y pasa a 'd_have1'.
    #    - Si es ' ' => significa que no hay más dígitos que procesar => 'finish_modulo'.
    #
    ('prepare', '0'): {'write': 'c', 'move': 'R', 'new_state': 'd_have0'},
    ('prepare', '1'): {'write': 'c', 'move': 'R', 'new_state': 'd_have1'},
    ('prepare', ' '): {'write': None, 'move': 'R', 'new_state': 'finish_modulo'},

    #
    # 4) Estados 'd_have0' y 'd_have1':
    #    Tras marcar un bit del dividendo con 'c', se avanza a la derecha en busca del '%'
    #    para luego arrancar la resta parcial.
    #    Si se encuentra un espacio antes de '%', lo tratamos como si el divisor estuviera
    #    "acabado" => igual pasamos a la sustracción.
    #
    ('d_have0', '0'): {'write': None, 'move': 'R', 'new_state': 'd_have0'},
    ('d_have0', '1'): {'write': None, 'move': 'R', 'new_state': 'd_have0'},
    ('d_have0', '%'): {'write': None, 'move': 'R', 'new_state': 'mod_sub0'},
    ('d_have0', ' '): {'write': None, 'move': 'R', 'new_state': 'mod_sub0'},

    ('d_have1', '0'): {'write': None, 'move': 'R', 'new_state': 'd_have1'},
    ('d_have1', '1'): {'write': None, 'move': 'R', 'new_state': 'd_have1'},
    ('d_have1', '%'): {'write': None, 'move': 'R', 'new_state': 'mod_sub1'},
    ('d_have1', ' '): {'write': None, 'move': 'R', 'new_state': 'mod_sub1'},

    #
    # 5) 'mod_sub0' y 'mod_sub1': "Resta parcial" de un bit del DIVIDENDO contra el DIVISOR.
    #    Se utilizan símbolos temporales 'O' y 'I'.
    #
    #    Caso 'c=0' => 'mod_sub0':
    #    - 0 - 0 => 0 => escribimos 'O', moverse a la derecha para seguir.
    #    - 0 - 1 => 1 => escribimos 'I', moverse a la derecha => borrow posterior.
    #    - 0 - ' ' => interpretamos ' ' como 0 => escribimos 'O'.
    #    - Si leemos 'O' o 'I' repetidos, retrocedemos para no confundir con bits sin procesar.
    #    - Cuando encontremos '%', significa fin del divisor => volvemos a la marca 'c'.
    #
    ('mod_sub0', '0'): {'write': 'O', 'move': 'R', 'new_state': 'mod_sub0'},
    ('mod_sub0', '1'): {'write': 'I', 'move': 'R', 'new_state': 'mod_sub0'},
    ('mod_sub0', ' '): {'write': 'O', 'move': 'R', 'new_state': 'mod_sub0'},
    ('mod_sub0', 'O'): {'write': None, 'move': 'L', 'new_state': 'mod_sub0'},
    ('mod_sub0', 'I'): {'write': None, 'move': 'L', 'new_state': 'mod_sub0'},
    ('mod_sub0', '%'): {'write': '%', 'move': 'L', 'new_state': 'back_to_c0'},

    #    Caso 'c=1' => 'mod_sub1':
    #    - 1 - 0 => 1 => escribimos 'I', moverse a la izquierda => 'd_borrow' si hace falta.
    #    - 1 - 1 => 0 => escribimos 'O', moverse a la derecha => 'mod_sub_done1'.
    #    - 1 - ' ' => treat ' ' como 0 => 1 => 'I', moverse a la izquierda => 'd_borrow'.
    #
    ('mod_sub1', '0'): {'write': 'I', 'move': 'L', 'new_state': 'd_borrow'},
    ('mod_sub1', '1'): {'write': 'O', 'move': 'R', 'new_state': 'mod_sub_done1'},
    ('mod_sub1', ' '): {'write': 'I', 'move': 'L', 'new_state': 'd_borrow'},
    ('mod_sub1', 'O'): {'write': None, 'move': 'L', 'new_state': 'mod_sub1'},
    ('mod_sub1', 'I'): {'write': None, 'move': 'L', 'new_state': 'mod_sub1'},
    ('mod_sub1', '%'): {'write': '%', 'move': 'L', 'new_state': 'back_to_c1'},

    #
    # 6) 'd_borrow': maneja el "préstamo" que surge cuando 1 - 0 => 1 y
    #    se requiere reducir algún bit a la izquierda.
    #
    ('d_borrow', '0'): {'write': '1', 'move': 'R', 'new_state': 'mod_sub_done1'},
    ('d_borrow', '1'): {'write': '0', 'move': 'L', 'new_state': 'd_borrow'},
    ('d_borrow', ' '): {'write': '1', 'move': 'R', 'new_state': 'mod_sub_done1'},
    ('d_borrow', 'O'): {'write': None, 'move': 'L', 'new_state': 'd_borrow'},
    ('d_borrow', 'I'): {'write': None, 'move': 'L', 'new_state': 'd_borrow'},
    ('d_borrow', '%'): {'write': '%', 'move': 'L', 'new_state': 'd_borrow'},

    #
    # 7) 'mod_sub_done1': indica que procesamos "1 - 1" (o "1 - 0" con el préstamo hecho).
    #    Si quisiéramos seguir restando más bits del divisor, avanzaríamos a la derecha.
    #    Pero para simplificar, en cuanto vemos cualquier símbolo, retrocedemos para volver
    #    a la marca 'c' => 'back_to_c1'.
    #
    ('mod_sub_done1', '0'): {'write': None, 'move': 'L', 'new_state': 'back_to_c1'},
    ('mod_sub_done1', '1'): {'write': None, 'move': 'L', 'new_state': 'back_to_c1'},
    ('mod_sub_done1', 'O'): {'write': None, 'move': 'L', 'new_state': 'back_to_c1'},
    ('mod_sub_done1', 'I'): {'write': None, 'move': 'L', 'new_state': 'back_to_c1'},
    ('mod_sub_done1', ' '): {'write': None, 'move': 'L', 'new_state': 'back_to_c1'},
    ('mod_sub_done1', '%'): {'write': '%', 'move': 'L', 'new_state': 'back_to_c1'},

    #
    # 8) 'back_to_c0' y 'back_to_c1': retroceder hasta encontrar la marca 'c'
    #    y sustituirla por '0' o '1', respectivamente.
    #
    ('back_to_c0', '0'): {'write': None, 'move': 'L', 'new_state': 'back_to_c0'},
    ('back_to_c0', '1'): {'write': None, 'move': 'L', 'new_state': 'back_to_c0'},
    ('back_to_c0', 'O'): {'write': None, 'move': 'L', 'new_state': 'back_to_c0'},
    ('back_to_c0', 'I'): {'write': None, 'move': 'L', 'new_state': 'back_to_c0'},
    ('back_to_c0', ' '): {'write': None, 'move': 'L', 'new_state': 'back_to_c0'},
    ('back_to_c0', '%'): {'write': '%', 'move': 'L', 'new_state': 'back_to_c0'},
    ('back_to_c0', 'c'): {'write': '0', 'move': 'R', 'new_state': 'reset'},

    ('back_to_c1', '0'): {'write': None, 'move': 'L', 'new_state': 'back_to_c1'},
    ('back_to_c1', '1'): {'write': None, 'move': 'L', 'new_state': 'back_to_c1'},
    ('back_to_c1', 'O'): {'write': None, 'move': 'L', 'new_state': 'back_to_c1'},
    ('back_to_c1', 'I'): {'write': None, 'move': 'L', 'new_state': 'back_to_c1'},
    ('back_to_c1', ' '): {'write': None, 'move': 'L', 'new_state': 'back_to_c1'},
    ('back_to_c1', '%'): {'write': '%', 'move': 'L', 'new_state': 'back_to_c1'},
    ('back_to_c1', 'c'): {'write': '1', 'move': 'R', 'new_state': 'reset'},

    #
    # 9) 'reset': convertir temporalmente O->0 e I->1, avanzar hasta reencontrar
    #    el separador '%' o un espacio, y saltar a 'right' para seguir con otro bit
    #    del dividendo.
    #
    ('reset', 'O'): {'write': '0', 'move': 'R', 'new_state': 'reset'},
    ('reset', 'I'): {'write': '1', 'move': 'R', 'new_state': 'reset'},
    ('reset', '0'): {'write': None, 'move': 'R', 'new_state': 'reset'},
    ('reset', '1'): {'write': None, 'move': 'R', 'new_state': 'reset'},
    ('reset', '%'): {'write': '%', 'move': 'R', 'new_state': 'right'},
    ('reset', ' '): {'write': None, 'move': 'R', 'new_state': 'right'},

    #
    # 10) 'finish_modulo': ya no hay más bits del dividendo que procesar.
    #     Retroceder para reescribir O->0, I->1, borrar cualquier 'c', etc.
    #     Al toparse con un espacio suelto, pasar a 'done'.
    #
    ('finish_modulo', 'O'): {'write': '0', 'move': 'L', 'new_state': 'finish_modulo'},
    ('finish_modulo', 'I'): {'write': '1', 'move': 'L', 'new_state': 'finish_modulo'},
    ('finish_modulo', 'c'): {'write': ' ', 'move': 'L', 'new_state': 'finish_modulo'},
    ('finish_modulo', '0'): {'write': None, 'move': 'L', 'new_state': 'finish_modulo'},
    ('finish_modulo', '1'): {'write': None, 'move': 'L', 'new_state': 'finish_modulo'},
    ('finish_modulo', '%'): {'write': '%', 'move': 'L', 'new_state': 'finish_modulo'},
    ('finish_modulo', ' '): {'write': None, 'move': 'R', 'new_state': 'done'},

    #
    # 11) Estado final
    #
    ('done', None): {'write': None, 'move': None, 'new_state': 'done'},
}