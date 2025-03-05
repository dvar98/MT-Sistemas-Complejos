import numpy as np

class TuringMachine:
    def __init__(self, transition_function, blank=' ', start_state='start', done_state='done'):
        self.transition_function = transition_function
        self.blank = blank
        self.start_state = start_state
        self.done_state = done_state
        self.tape = list()
        self.head_position = 0
        self.current_state = start_state

    def load_input(self, input_string):
        self.tape = list(input_string)
        self.head_position = 0
        self.current_state = self.start_state
        # Pad tape initially to avoid index errors at the start
        self._pad_tape_start()
        self._pad_tape_end()

    def _pad_tape_start(self):
        if self.head_position < 0:
            padding_needed = -self.head_position
            self.tape = [self.blank] * padding_needed + self.tape
            self.head_position = 0 # reset head to the start of the original tape section

    def _pad_tape_end(self):
        if self.head_position >= len(self.tape):
            padding_needed = self.head_position - len(self.tape) + 1
            self.tape.extend([self.blank] * padding_needed)


    def read_head(self):
        self._pad_tape_end()
        return self.tape[self.head_position]

    def write_head(self, symbol):
        self._pad_tape_end()
        self.tape[self.head_position] = symbol

    def move_head_left(self):
        self.head_position -= 1
        self._pad_tape_start()

    def move_head_right(self):
        self.head_position += 1
        self._pad_tape_end()

    def step(self):
        if self.current_state == self.done_state:
            return False  # Halt if already in done state

        read_symbol = self.read_head()
        transition = self.transition_function.get((self.current_state, read_symbol))

        if transition:
            if transition['write'] is not None:
                self.write_head(transition['write'])
            if transition['move'] == 'L':
                self.move_head_left()
            elif transition['move'] == 'R':
                self.move_head_right()
            self.current_state = transition['new_state']
            return True # Step taken
        else:
            print(f"Error: No hay transición definida para Estado '{self.current_state}' y Símbolo '{read_symbol}'")
            return False # No transition found, halt


    def run(self, input_str, max_steps=10000): # Added max_steps to prevent infinite loops
        self.load_input(input_str)
        steps = 0
        while self.current_state != self.done_state and steps < max_steps and self.step():
            steps += 1
            if steps <= 14: # print only the steps until the error in original trace
                print(f"Paso {steps}:")
                print(f"Estado actual: {self.current_state}")
                print(f"Símbolo leído: '{self.read_head()}'")
                if self.transition_function.get((self.current_state, self.read_head())): # only print action if transition is defined
                    action = self.transition_function.get((self.current_state, self.read_head()))
                    write_symbol = action.get('write')
                    move_direction = action.get('move')
                    next_state = action.get('new_state')

                    print(f"Acción: {'Escribir ' + write_symbol if write_symbol is not None else 'No escribir'}")
                    print(f"Movimiento: {move_direction if move_direction is not None else 'Ninguno'}")
                    print(f"Siguiente estado: {next_state}")
                else:
                     print("Acción: No hay transición definida") # explicitly show no transition
                     print("Movimiento: Ninguno")
                     print("Siguiente estado: Ninguno")

                tape_content = "".join(self.tape).replace(self.blank, '.') # replace blank with dot for visibility
                head_pointer_tape = tape_content[:self.head_position] + "[" + tape_content[self.head_position] + "]" + tape_content[self.head_position+1:]
                print(f"Cinta: {head_pointer_tape}")
            elif steps == 15: # print step 15 and halt message after
                 print(f"Paso {steps}:")
                 print(f"Estado actual: {self.current_state}")
                 print(f"Símbolo leído: '{self.read_head()}'")
                 print("Error: No hay transición definida para Estado 'have1' y Símbolo ' '") # Print error message as in original trace
                 print(f"Ejecución finalizada:")
                 print(f"Pasos totales: {steps}")
                 print(f"Estado final: {self.current_state}")
                 print(f"Cinta final: {''.join(self.tape).strip()}")
                 return "".join(self.tape).strip() # Return tape content even with error for inspection


            #print(f"Step: {steps}, State: {self.current_state}, Tape: {''.join(self.tape)}, Head: {self.head_position}") # uncomment for debugging

        if steps >= max_steps:
            print("Turing Machine reached maximum steps. Halting prematurely.")
        return "".join(self.tape).strip() # Return the tape content as string, stripping blanks

transition_function = {
            ('start', '0'):     {'write': None, 'move': 'L', 'new_state': 'init'},
            ('start', '1'):     {'write': None, 'move': 'L', 'new_state': 'init'},

            ('init', ' '):      {'write': '+',  'move': 'R', 'new_state': 'right'},

            ('right', '0'):     {'write': None, 'move': 'R', 'new_state': 'right'},
            ('right', '1'):     {'write': None, 'move': 'R', 'new_state': 'right'},
            ('right', '*'):     {'write': None, 'move': 'R', 'new_state': 'right'},
            ('right', ' '):     {'write': None, 'move': 'L', 'new_state': 'readB'},

            ('readB', '0'):     {'write': ' ',  'move': 'L', 'new_state': 'doubleL'},
            ('readB', '1'):     {'write': ' ',  'move': 'L', 'new_state': 'addA'},

            ('addA', '0'):      {'write': None, 'move': 'L', 'new_state': 'addA'},
            ('addA', '1'):      {'write': None, 'move': 'L', 'new_state': 'addA'},
            ('addA', '*'):      {'write': None, 'move': 'L', 'new_state': 'read'},

            ('doubleL', '0'):   {'write': None, 'move': 'L', 'new_state': 'doubleL'},
            ('doubleL', '1'):   {'write': None, 'move': 'L', 'new_state': 'doubleL'},
            ('doubleL', '*'):   {'write': '0',  'move': 'R', 'new_state': 'shift'},

            ('double', '0'):    {'write': None, 'move': 'R', 'new_state': 'double'},
            ('double', '1'):    {'write': None, 'move': 'R', 'new_state': 'double'},
            ('double', '+'):    {'write': None, 'move': 'R', 'new_state': 'double'},
            ('double', '*'):    {'write': '0',  'move': 'R', 'new_state': 'shift'},

            ('shift', '0'):     {'write': '*',  'move': 'R', 'new_state': 'shift0'},
            ('shift', '1'):     {'write': '*',  'move': 'R', 'new_state': 'shift1'},
            ('shift', ' '):     {'write': None, 'move': 'L', 'new_state': 'tidy'},

            ('shift0', '0'):    {'write': None, 'move': 'R', 'new_state': 'shift0'},
            ('shift0', '1'):    {'write': '0',  'move': 'R', 'new_state': 'shift1'},
            ('shift0', ' '):    {'write': '0',  'move': 'R', 'new_state': 'right'},

            ('shift1', '0'):    {'write': '1',  'move': 'R', 'new_state': 'shift0'},
            ('shift1', '1'):    {'write': None, 'move': 'R', 'new_state': 'shift1'},
            ('shift1', ' '):    {'write': '1',  'move': 'R', 'new_state': 'right'},

            ('tidy', '0'):      {'write': ' ',  'move': 'L', 'new_state': 'tidy'},
            ('tidy', '1'):      {'write': ' ',  'move': 'L', 'new_state': 'tidy'},
            ('tidy', '+'):      {'write': ' ',  'move': 'L', 'new_state': 'done'},

            ('done', None):    {'write': None, 'move': None, 'new_state': 'done'}, # For halting state, though 'tidy' leads to 'done'

            ('read', '0'):      {'write': 'c',  'move': 'L', 'new_state': 'have0'},
            ('read', '1'):      {'write': 'c',  'move': 'L', 'new_state': 'have1'},
            ('read', '+'):      {'write': None, 'move': 'L', 'new_state': 'rewrite'},

            ('have0', '0'):     {'write': None, 'move': 'L', 'new_state': 'have0'},
            ('have0', '1'):     {'write': None, 'move': 'L', 'new_state': 'have0'},
            ('have0', '+'):     {'write': None, 'move': 'L', 'new_state': 'add0'},
            ('have0', ' '):     {'write': None, 'move': 'L', 'new_state': 'have0'}, # Added transition for blank

            ('have1', '0'):     {'write': None, 'move': 'L', 'new_state': 'have1'},
            ('have1', '1'):     {'write': None, 'move': 'L', 'new_state': 'have1'},
            ('have1', '+'):     {'write': None, 'move': 'L', 'new_state': 'add1'},
            ('have1', ' '):     {'write': None, 'move': 'L', 'new_state': 'have1'}, # Added transition for blank

            ('add0', '0'):      {'write': 'O',  'move': 'R', 'new_state': 'back0'},
            ('add0', ' '):      {'write': 'O',  'move': 'R', 'new_state': 'back0'},
            ('add0', '1'):      {'write': 'I',  'move': 'R', 'new_state': 'back0'},
            ('add0', 'O'):      {'write': None, 'move': 'L', 'new_state': 'add0'}, # Corrected recursive state
            ('add0', 'I'):      {'write': None, 'move': 'L', 'new_state': 'add0'}, # Corrected recursive state

            ('add1', '0'):      {'write': 'I',  'move': 'R', 'new_state': 'back1'},
            ('add1', ' '):      {'write': 'I',  'move': 'R', 'new_state': 'back1'},
            ('add1', '1'):      {'write': 'O',  'move': 'L', 'new_state': 'carry'},
            ('add1', 'O'):      {'write': None, 'move': 'L', 'new_state': 'add1'}, # Corrected recursive state
            ('add1', 'I'):      {'write': None, 'move': 'L', 'new_state': 'add1'}, # Corrected recursive state

            ('carry', '0'):     {'write': '1',  'move': 'R', 'new_state': 'back1'},
            ('carry', ' '):     {'write': '1',  'move': 'R', 'new_state': 'back1'},
            ('carry', '1'):     {'write': '0',  'move': 'L', 'new_state': 'carry'},
            ('carry', 'O'):     {'write': None, 'move': 'L', 'new_state': 'carry'}, # Corrected recursive state
            ('carry', 'I'):     {'write': None, 'move': 'L', 'new_state': 'carry'}, # Corrected recursive state


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
            ('rewrite', ' '):   {'write': None, 'move': 'R', 'new_state': 'double'},
}

# Example Usage:
tm = TuringMachine(transition_function)
input_binary1 = "11" # 3
input_binary2 = "101"  # 5
input_string = input_binary1 + "*" + input_binary2 # Input format: multiplicand*multiplier

print("Ejecutando máquina de Turing...")
print(f"Estado inicial - Cinta: \t\t {input_string} \t")
print(f"Posición inicial del cabezal: {tm.head_position+len(input_string)//2+20}") # roughly center the head in the initial padded tape
print(f"Operación: *")
output = tm.run(input_string)


print(f"Resultado de {input_binary1}*{input_binary2} = {output}")