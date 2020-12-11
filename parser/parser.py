import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from tokenizer import tokens

def p_start(p):
    'S : METADATA JUGADAS'
    pass

def p_metadata(p):
    'METADATA : ITEM_METADATA METADATA'
    '         | lambda'
    pass

def p_lambda(p):
    'lambda :'
    pass

def p_item_metadata(p):
    'ITEM_METADATA : corchete_abre palabra comilla palabra comilla corchete_cierra'
    pass

def p_jugadas(p):
    'JUGADAS : pieza columna' # TODO Cambiar
    pass

# Error rule for syntax errors
def p_error(p):
    p[0].valid = False

# Build the parser
parser = yacc.yacc()

if __name__ == '__main__':
    while True:
        try:
            s = input('calc > ')
        except EOFError:
            break
        if not s: continue
        result = parser.parse(s)
        print(result)