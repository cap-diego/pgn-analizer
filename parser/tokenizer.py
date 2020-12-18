# ------------------------------------------------------------
# calclex.py
#
# tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------
import ply.lex as lex
import re
import sys

leer_renglones = True   # Indica al lexer si tiene que tokenizar los \n
en_metadata = False     # Indica al lexer si está en la sección metadata
en_comentario = 0       # Indica al lexer si está en un comentrario

# Lista de tokens
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
'jaque',
'jaque_mate',
'palabra',
'numero_jugada_negro',
'numero_jugada_blanco',
'espacio',
'token_movimiento',
'renglon'
)

# Reglas para tokens simples 
t_jaque  = r'\+'
t_jaque_mate  = r'\#'

# Reglas más complejas para ciertos tokens
def t_espacio(t):
    r'[^\S\n\t]'
    global en_metadata
    global en_comentario
    if en_metadata or en_comentario > 0:
        return t

def t_renglon(t):
    r'\n+'
    t.lexer.lineno += len(t.value) # Actualizar el contador de líneas del lexer
    global leer_renglones
    if leer_renglones:
        return t

def t_comilla(t):
    r'\"'
    return t

def t_corchete_abre(t):
    r'\['
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
    #print(en_comentario)
    return t

def t_llave_cierra(t):
    r'\}'
    global en_comentario
    en_comentario -= 1
    #print(en_comentario)
    return t

def t_parentecis_abre(t):
    r'\('
    global en_comentario
    en_comentario += 1
    #print(en_comentario)
    return t

def t_parentecis_cierra(t):
    r'\)'
    global en_comentario
    en_comentario -= 1
    #print(en_comentario)
    return t

def t_palabra(t):
    r'[^(\s|\"|\]|\[|\{|\}|\(|\))]+'
    global leer_renglones
    global en_metadata

    # Matchea con todo lo que no esté separado por espacios
    # Hay que re tokenizar todos los valores que no sean palabras a mano

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

    # Enroques
    elif not en_comentario and re.search(r'O-O-O', t.value):
        t.type = 'enroque_1'

    elif not en_comentario and re.search(r'O-O', t.value):
        t.type = 'enroque_2'

    return t

# Caracteres a ignorar
t_ignore  = '\t'

# Regla para manejar errores
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Creamos el lexer
lexer = lex.lex()

def correr_lexer():
    if(len(sys.argv) != 2):
        print("ERROR - EL PROGRAMA SOLO TOMA UN ARGUMENTO")
        return
    
    f = open(sys.argv[1], "r")
    s = f.read()
    lexer.input(s)
    # Tokenize
    while True:
        tok = lexer.token()
        if not tok: 
            break      # No more input
        print(tok)

if __name__ == '__main__':
    correr_lexer()
