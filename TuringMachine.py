import numpy as np
import importlib

class TuringMachineBinaryOperator:
    def __init__(self):
        self.tape = np.array([' '] * 50)
        self.head_position = 0
        self.current_state = 'right'
        self.operator_index = -1  # Posición del símbolo de la operación
        self.operation_type = None
        self.transition_function = {}  # Se cargará según la operación

    def load_input(self, expression):
        input_array = list(expression)
        start_pos = (len(self.tape) - len(input_array)) // 2
        self.tape[start_pos:start_pos + len(input_array)] = input_array
        self.head_position = start_pos
        self.current_state = 'right'

        # Detecta el operador (puede ser '+', '-' o '*') y guarda su posición
        for i, symbol in enumerate(input_array):
            if symbol in ['+', '-', '*']:
                self.operator_index = start_pos + i
                self.operation_type = symbol
                break

        # Carga el módulo de transiciones adecuado
        if self.operation_type == '+':
            mod = importlib.import_module("suma_estados")
        elif self.operation_type == '-':
            mod = importlib.import_module("resta_estados")
        elif self.operation_type == '*':
            mod = importlib.import_module("multiplicacion_estados")
        else:
            raise ValueError("Operación no reconocida")
        self.transition_function = mod.transition_function.copy()

    def run(self):
        state = self.current_state
        step_count = 0

        print("\nEjecutando máquina de Turing...")
        print(f"Estado inicial - Cinta: {''.join(self.tape)}")
        print(f"Posición inicial del cabezal: {self.head_position}")
        print(f"Operación: {self.operation_type}\n")

        while state != 'done' and step_count < 10000:
            step_count += 1
            symbol = self.tape[self.head_position]
            instruction = self.transition_function.get((state, symbol))

            if instruction:
                write_symbol = instruction.get('write')
                move_direction = instruction.get('move')
                next_state = instruction.get('new_state')

                print(f"Paso {step_count}:")
                print(f"Estado actual: {state}")
                print(f"Símbolo leído: '{symbol}'")
                print(f"Acción: {'Escribir ' + str(write_symbol) if write_symbol else 'No escribir'}")
                print(f"Movimiento: {move_direction}")
                print(f"Siguiente estado: {next_state}")

                # Mostrar la cinta con el cabezal marcado
                tape_display = list(self.tape)
                tape_display[self.head_position] = f"[{tape_display[self.head_position]}]"
                print(f"Cinta: {''.join(tape_display).replace(' ', '.')}")

                if write_symbol is not None:
                    self.tape[self.head_position] = write_symbol
                if move_direction == 'R':
                    self.head_position += 1
                elif move_direction == 'L':
                    self.head_position -= 1
                state = next_state
            else:
                print(f"\nError: No hay transición definida para Estado '{state}' y Símbolo '{symbol}'")
                break

            if self.head_position < 0:
                print("\nError: El cabezal se movió fuera del límite izquierdo de la cinta.")
                break
            if self.head_position >= len(self.tape):
                print("\nError: El cabezal se movió fuera del límite derecho de la cinta.")
                break

        print("\nEjecución finalizada:")
        print(f"Pasos totales: {step_count}")
        print(f"Estado final: {state}")
        print(f"Cinta final: {''.join(self.tape).replace(' ', '.')}")
        self.current_state = state

    def get_result(self):
        # Se asume que el resultado está a la izquierda del separador.
        # Se recorren todos los símbolos y se consideran como resultado solo los que
        # sean '1' o X (los X se interpretan como '1').
        result_array = []
        for symbol in self.tape:
            if symbol == '1' or symbol == 'X':
                result_array.append('1')
        return "".join(result_array)


# Ejemplo de uso:

tm = TuringMachineBinaryOperator()
# Puedes probar con distintas operaciones:
#input_expression = "1+1"  # Para suma
input_expression = "111-11"  # Para resta

tm.load_input(input_expression)
tm.run()
result = tm.get_result()
print(f"Resultado de {input_expression} = {result}")
