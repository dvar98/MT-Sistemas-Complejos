import numpy as np
import importlib

class TuringMachineBinaryOperator:
    def __init__(self):
        self.tape = np.array([' '] * 100)
        self.head_position = 0
        self.current_state = 'right'
        self.operator_index = -1
        self.operation_type = None
        self.transition_function = {}
        self.plus_index_original = -1

    def load_input(self, expression):
        self.tape.fill(' ')  # Clear the tape before loading new input
        input_array = list(expression)
        start_pos = (len(self.tape) - len(input_array)) // 2
        self.tape[start_pos:start_pos + len(input_array)] = input_array
        self.head_position = start_pos
        self.current_state = 'right'
        
        for i, symbol in enumerate(input_array):
            if symbol in ['+', '-', '*', '/', '^', '%', '√']:
                self.operator_index = start_pos + i
                self.operation_type = symbol
                self.plus_index_original = self.operator_index
                break
        
        if self.operation_type == '+':
            mod = importlib.import_module("suma_estados")
        elif self.operation_type == '-':
            mod = importlib.import_module("resta_estados")
        elif self.operation_type == '*':
            mod = importlib.import_module("multiplicacion_estados")
        elif self.operation_type == '/':
            mod = importlib.import_module("division_estados")
        else:
            mod = None
        
        if mod:
            self.transition_function = mod.transition_function.copy()

    def calculate_result(self, num1, num2, op):
        if op == '%':
            return num1 % num2
        elif op == '^':
            return num1 ** num2
        elif op == '√':
            return int(num1 ** 0.5)
        return None
    
    def execute(self):
            if self.operation_type in ['+', '-', '*', '/']:
                while self.current_state != 'done':  # Procesar con estados solo en estas operaciones
                    symbol = self.tape[self.head_position]  # Leer el símbolo actual
                    transition = self.transition_function.get((self.current_state, symbol))  # Obtener transición
        
                    if transition is None:  # Si no hay transición definida, detener la máquina
                        break
        
                    # Escribir en la cinta si es necesario
                    if transition['write'] is not None:
                        self.tape[self.head_position] = transition['write']
        
                    # Mover el cabezal
                    if transition['move'] == 'R':
                        self.head_position += 1
                    elif transition['move'] == 'L':
                        self.head_position -= 1
        
                    # Cambiar al nuevo estado
                    self.current_state = transition['new_state']
            
            else:
                # Si es %, ^ o √, calcular directamente
                expression = ''.join(self.tape).strip()
                num1, num2 = None, None
                if self.operation_type == '√':
                    num1 = int(expression.split(self.operation_type)[0], 2)
                else:
                    num1, num2 = map(lambda x: int(x, 2), expression.split(self.operation_type))
        
                result = self.calculate_result(num1, num2, self.operation_type)
                result_bin = bin(result)[2:]
        
                self.tape.fill(' ')
                self.tape[:len(result_bin)] = list(result_bin)
        
    def get_result(self):
        if self.operation_type in ['+', '-', '*', '/']:
            if self.plus_index_original != -1:
                result_array = self.tape[:self.plus_index_original]
                result_str = "".join(result_array).replace(" ", "")
                return result_str
            return "Resultado no encontrado o error en la ejecución"
        else:
            return "".join(self.tape).strip()  # Para %, ^ y √, devuelve el resultado completo

# Ejemplo de uso
tm = TuringMachineBinaryOperator()

# Leer cintas de entrada desde la consola
while True:
    cinta = input("Ingrese la cinta (o 'salir' para terminar): ")
    if cinta.lower() == 'salir':
        break
    tm.load_input(cinta)
    tm.execute()
    print(f"Resultado de {cinta} = {tm.get_result()}")