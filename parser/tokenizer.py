# ------------------------------------------------------------
# calclex.py
#
# tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------
import ply.lex as lex

# List of token names.   This is always required
tokens = (
'enroque_1',
'enroque_2',
'gano_blanco',
'gano_negro',
'empate',
'corchete_abre',
'corchete_cierra',
'llave_abre',
'llave_cierra',
'parentecis_abre',
'parentecis_cierra',
'comilla',
'punto',
'jaque',
'jaque_mate',
'pieza',
'columna',
'fila',
'palabra',
'numero',
'equis',
'espacio',
)

# precedence = (
#     ('left', '', '')
# )

# Regular expression rules for simple tokens
t_enroque_1 = r'O-O-O'
t_enroque_2 = r'O-O'
t_gano_blanco  = r'1-0'
t_gano_negro  = r'0-1'
t_empate  = r'1\/2-1\/2'
t_corchete_abre  = r'\['
t_corchete_cierra  = r'\]'
t_llave_abre  = r'\{'
t_llave_cierra  = r'\}'
t_parentecis_abre  = r'\('
t_parentecis_cierra  = r'\)'
t_comilla  = r'\"'
t_punto  = r'\.'
t_jaque  = r'\+'
t_jaque_mate  = r'\#'
t_pieza  = r'[PNBRQK]'
t_columna  = r'[a-h]'
t_fila  = r'[1-8]'
t_palabra = r'[a-zA-Z]+|\?|\-|\,' # r'[a-zA-Z]+'
t_equis = r'x'
t_espacio = r'\s'

# A regular expression rule with some action code
def t_numero(t):
    r'\d+'
    t.value = int(t.value)    
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

if __name__ == '__main__':
    # Test it out
    data = '''
    [PlyCount "45"]
    1. e4 {Notes by Richard Reti} 1... e6 
    '''

    # Give the lexer some input
    lexer.input(data)

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok: 
            break      # No more input
        print(tok)