import numpy as np

class TuringMachineBinaryAdder:
    def __init__(self):
        self.tape = np.array([' '] * 100)
        self.head_position = 0
        self.current_state = 'right'
        self.plus_index_original = -1 # Guardar el índice original de '+'

        self.transition_function = {
            ('right', '0'):     {'write': None, 'move': 'R', 'new_state': 'right'},
            ('right', '1'):     {'write': None, 'move': 'R', 'new_state': 'right'},
            ('right', '+'):     {'write': None, 'move': 'R', 'new_state': 'right'},
            ('right', ' '):     {'write': None, 'move': 'L', 'new_state': 'read'},

            ('read', '0'):      {'write': 'c',  'move': 'L', 'new_state': 'have0'},
            ('read', '1'):      {'write': 'c',  'move': 'L', 'new_state': 'have1'},
            ('read', '+'):      {'write': ' ',  'move': 'L', 'new_state': 'rewrite'},

            ('have0', '0'):     {'write': None, 'move': 'L', 'new_state': 'have0'},
            ('have0', '1'):     {'write': None, 'move': 'L', 'new_state': 'have0'},
            ('have0', '+'):     {'write': None, 'move': 'L', 'new_state': 'add0'},

            ('have1', '0'):     {'write': None, 'move': 'L', 'new_state': 'have1'},
            ('have1', '1'):     {'write': None, 'move': 'L', 'new_state': 'have1'},
            ('have1', '+'):     {'write': None, 'move': 'L', 'new_state': 'add1'},

            ('add0', '0'):      {'write': 'O',  'move': 'R', 'new_state': 'back0'},
            ('add0', ' '):      {'write': 'O',  'move': 'R', 'new_state': 'back0'},
            ('add0', '1'):      {'write': 'I',  'move': 'R', 'new_state': 'back0'},
            ('add0', 'O'):      {'write': None, 'move': 'L', 'new_state': 'add0'},
            ('add0', 'I'):      {'write': None, 'move': 'L', 'new_state': 'add0'},

            ('add1', '0'):      {'write': 'I',  'move': 'R', 'new_state': 'back1'},
            ('add1', ' '):      {'write': 'I',  'move': 'R', 'new_state': 'back1'},
            ('add1', '1'):      {'write': 'O',  'move': 'L', 'new_state': 'carry'},
            ('add1', 'O'):      {'write': None, 'move': 'L', 'new_state': 'add1'},
            ('add1', 'I'):      {'write': None, 'move': 'L', 'new_state': 'add1'},

            ('carry', '0'):     {'write': '1',  'move': 'R', 'new_state': 'back1'},
            ('carry', ' '):     {'write': '1',  'move': 'R', 'new_state': 'back1'},
            ('carry', '1'):     {'write': '0',  'move': 'L', 'new_state': 'carry'},

            ('back0', '0'):    {'write': None, 'move': 'R', 'new_state': 'back0'},
            ('back0', '1'):    {'write': None, 'move': 'R', 'new_state': 'back0'},
            ('back0', 'O'):    {'write': None, 'move': 'R', 'new_state': 'back0'},
            ('back0', 'I'):    {'write': None, 'move': 'R', 'new_state': 'back0'},
            ('back0', '+'):    {'write': None, 'move': 'R', 'new_state': 'back0'},
            ('back0', 'c'):    {'write': '0',  'move': 'L', 'new_state': 'read'},

            ('back1', '0'):    {'write': None, 'move': 'R', 'new_state': 'back1'},
            ('back1', '1'):    {'write': None, 'move': 'R', 'new_state': 'back1'},
            ('back1', 'O'):    {'write': None, 'move': 'R', 'new_state': 'back1'},
            ('back1', 'I'):    {'write': None, 'move': 'R', 'new_state': 'back1'},
            ('back1', '+'):    {'write': None, 'move': 'R', 'new_state': 'back1'},
            ('back1', 'c'):    {'write': '1',  'move': 'L', 'new_state': 'read'},

            ('rewrite', 'O'):   {'write': '0',  'move': 'L', 'new_state': 'rewrite'},
            ('rewrite', 'I'):   {'write': '1',  'move': 'L', 'new_state': 'rewrite'},
            ('rewrite', '0'):   {'write': None, 'move': 'L', 'new_state': 'rewrite'},
            ('rewrite', '1'):   {'write': None, 'move': 'L', 'new_state': 'rewrite'},
            ('rewrite', ' '):   {'write': None, 'move': 'R', 'new_state': 'done'},

            ('done', None):    {'write': None, 'move': None, 'new_state': 'done'}
        }

    def load_input(self, binary_sum_expression):
        input_array = list(binary_sum_expression)
        start_pos = (len(self.tape) - len(input_array)) // 2
        self.tape[start_pos:start_pos + len(input_array)] = input_array
        self.head_position = start_pos
        self.current_state = 'right'

        # Guardar la posición del '+' durante la carga de entrada
        for i in range(len(input_array)):
            if input_array[i] == '+':
                self.plus_index_original = start_pos + i
                break


    def run(self):
            state = self.current_state
            step_count = 0 # Contador de pasos para limitar la ejecución si hay bucle infinito

            while state != 'done' and step_count < 100: # Límite de 100 pasos como seguridad
                step_count += 1
                symbol = self.tape[self.head_position]
                instruction = self.transition_function.get((state, symbol))

                if instruction:
                    write_symbol = instruction.get('write')
                    move_direction = instruction.get('move')
                    next_state = instruction.get('new_state')

                    print(f"Paso {step_count}: Estado: {state}, Leído: '{symbol}', Escribir: '{write_symbol}', Movimiento: {move_direction}, Nuevo Estado: {next_state}") # Imprimir información del paso
                    print("Cinta:", "".join(self.tape).replace(" ", ".")) # Imprimir estado de la cinta (espacios como '.')
                    print("Posición del Cabezal:", self.head_position)

                    if write_symbol:
                        self.tape[self.head_position] = write_symbol
                    if move_direction == 'R':
                        self.head_position += 1
                    elif move_direction == 'L':
                        self.head_position -= 1
                    state = next_state
                else:
                    print(f"No transition found for state '{state}' and symbol '{symbol}'. Halting.")
                    break
                if self.head_position < 0:
                    print("Error: Head moved off the left end of the tape.")
                    break
                if self.head_position >= len(self.tape):
                    print("Error: Head moved off the right end of the tape. Consider expanding the tape.")
                    break
            self.current_state = state
            if step_count >= 100:
                print("Advertencia: La máquina de Turing podría estar en un bucle infinito o tardar demasiado.")

    def get_result(self):
        if self.plus_index_original != -1:
            result_array = self.tape[:self.plus_index_original] # Tomar hasta el índice original del '+'
            result_str = "".join(result_array).replace(" ", "")
            return result_str
        return "Resultado no encontrado o error en la ejecución"


# Ejemplo de uso
tm_adder = TuringMachineBinaryAdder()



# Prueba 3: 110+10
input_expression = "10+1"
tm_adder.load_input(input_expression)
tm_adder.run()
result = tm_adder.get_result()
print(f"Suma de {input_expression} = {result}") # Expected: 1000

