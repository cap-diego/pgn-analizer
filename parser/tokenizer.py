# ------------------------------------------------------------
# calclex.py
#
# tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------
import ply.lex as lex
import re

leer_renglones = True
en_metadata = False
en_comentario = 0

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
#'punto',
'jaque',
'jaque_mate',
#'pieza',
#'columna',
#'fila',
'palabra',
#'numero',
'numero_jugada_negro',
'numero_jugada_blanco',
#'equis',
'espacio',
'token_movimiento',
'renglon'
)

# precedence = (
#     ('left', '', '')
# )

# Regular expression rules for simple tokens
# t_enroque_1 = r'O-O-O'
# t_enroque_2 = r'O-O'
# t_gano_blanco  = r'1-0'
# t_gano_negro  = r'0-1'
# t_empate  = r'1\/2-1\/2'
# t_corchete_abre  = r'\['
# t_corchete_cierra  = r'\]'
# t_llave_abre  = r'\{'
# t_llave_cierra  = r'\}'
# t_parentecis_abre  = r'\('
# t_parentecis_cierra  = r'\)'
# t_comilla  = r'\"'
# t_punto  = r'\.'
t_jaque  = r'\+'
t_jaque_mate  = r'\#'
# t_pieza  = r'[PNBRQK]'
# t_columna  = r'[a-h]'
# t_fila  = r'[1-8]'
# t_palabra = r'[a-zA-Z]+|\?|\-|\,' # r'[a-zA-Z]+'
# t_equis = r'x'
# t_espacio = r'\s'
# t_renglon = r'\n'


def t_espacio(t):
    r'[^\S\n\t]'
    # import pdb;pdb.set_trace()
    global en_metadata
    global en_comentario

    if en_metadata or en_comentario > 0:
        return t

# Define a rule so we can track line numbers
def t_renglon(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    # import pdb; pdb.set_trace()
    global leer_renglones
    if leer_renglones:
        return t

def t_comilla(t):
    r'\"'
    # import pdb; pdb.set_trace()
    # global en_metadata
    # en_metadata = not en_metadata
    return t

def t_corchete_abre(t):
    r'\['
    # import pdb; pdb.set_trace()
    global leer_renglones
    leer_renglones = True

    global en_metadata
    en_metadata = not en_metadata
    return t

def t_corchete_cierra(t):
    r'\]'
    global en_metadata
    en_metadata = not en_metadata
    return t

def t_llave_abre(t):
    r'\{'
    global en_comentario
    en_comentario += 1
    return t

def t_llave_cierra(t):
    r'\}'
    global en_comentario
    en_comentario -= 1
    return t

def t_parentecis_abre(t):
    r'\('
    global en_comentario
    en_comentario += 1
    return t

def t_parentecis_cierra(t):
    r'\)'
    global en_comentario
    en_comentario -= 1
    return t

def t_palabra(t):
    r'[^(\s|\"|\]|\[|\{|\})]+'
    global leer_renglones
    global en_metadata
    # Matchea con todo lo que no esté separado por espacios
    # Hay que re tokenizar todos los valores a mano

    # import pdb; pdb.set_trace()

    if en_metadata:
        return t
    
    # Numero de jugada del jugador negro
    if not en_comentario and re.search(r'\d+\.\.\.', t.value) and len(t.value.split("...")) == 2 and t.value.split("...")[1] == '' and t.value.split("...")[0].isdigit():
        t.type = 'numero_jugada_negro'
        # import pdb; pdb.set_trace()
        leer_renglones = False
        
    # Numero de jugada del jugador blanco
    elif not en_comentario and re.search(r'\d+\.', t.value) and len(t.value.split(".")) == 2 and t.value.split(".")[1] == '' and t.value.split(".")[0].isdigit():
        t.type = 'numero_jugada_blanco'
        # import pdb; pdb.set_trace()
        leer_renglones = False

    # Movimientos 
    elif re.search(r'[PNBRQK]?[a-h]?[1-8]?x?[PNBRQK]?[a-h][1-8]', t.value):
        t.type ='token_movimiento'
    
    # Movimientos Finales
    elif not en_comentario and re.search(r'1-0', t.value):
        # import pdb; pdb.set_trace()
        t.type = 'gano_blanco'
        leer_renglones = True
    
    elif not en_comentario and re.search(r'0-1', t.value):
        t.type = 'gano_negro'
        leer_renglones = True
    
    elif not en_comentario and re.search(r'1\/2-1\/2', t.value):
        t.type = 'empate'
        leer_renglones = True

    elif not en_comentario and re.search(r'O-O-O', t.value):
        t.type = 'enroque_1'

    elif not en_comentario and re.search(r'O-O', t.value):
        t.type = 'enroque_2'

    return t

# A regular expression rule with some action code
# def t_numero(t):
#     r'\d+'
#     t.value = int(t.value)
#     return t

# def t_palabra(t):
#     r'[a-zA-Z]+|\?|\-|\,'
#     t.type = 'columna' if t.value in 'abcdefgh' else 'fila' if t.value in '12345678' else 'palabra'
#     return t

# A string containing ignored characters (spaces and tabs)
t_ignore  = '\t'

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
    # lexer.input(data)

    f = open("testeo.txt", "r")
    s = f.read()
    lexer.input(s)
    # Tokenize
    while True:
        tok = lexer.token()
        if not tok: 
            break      # No more input
        print(tok)