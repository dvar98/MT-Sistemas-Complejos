transition_function = {
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