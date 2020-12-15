import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from tokenizer import tokens

def p_start(p):
    'S : METADATA JUGADAS'
    pass

def p_metadata(p):
    '''METADATA : ITEM_METADATA METADATA
                | lambda'''
    pass

def p_item_metadata(p):
    'ITEM_METADATA : corchete_abre palabra comilla palabra comilla corchete_cierra'
    pass

def p_jugadas(p):
    '''JUGADAS  : JUGADA JUGADAS
                | MOVIMIENTO_FINAL'''
    pass

def p_movimiento_final(p):
    '''MOVIMIENTO_FINAL :   gano_blanco
                        |   gano_negro
                        |   empate'''
    pass

def p_jugada(p):
    'JUGADA :   NUMERO_JUGADA punto COMENTARIO MOVIMIENTO COMENTARIO NUMERO_JUGADA_OPCIONAL MOVIMIENTO COMENTARIO'
    pass

def p_numero_jugada(p):
    'NUMERO_JUGADA  :   numero'
    pass

def p_numero_jugada_opcional(p):
    '''NUMERO_JUGADA_OPCIONAL   :   NUMERO_JUGADA punto punto punto COMENTARIO
                                |   lambda'''
    pass

def p_movimiento(p):
    '''MOVIMIENTO   :   PIEZA POS_OPCIONAL X POS ESPECIAL
                    |   enroque_1 ESPECIAL
                    |   enroque_2 ESPECIAL'''
    pass

def p_equis(p):
    '''X    :   equis
            |   lambda'''
    pass

def p_pos_opcional(p):
    '''POS_OPCIONAL :   COLUMNA FILA
                    |   COLUMNA
                    |   FILA
                    |   lambda'''
    pass

def p_pos(p):
    'POS    :   COLUMNA FILA'
    pass

def p_especial(p):
    '''ESPECIAL :   jaque_mate
                |   jaque
                |   lambda'''
    pass

def p_pieza(p):
    '''PIEZA    :   pieza
                |   lambda'''
    pass

def p_columna(p):
    'COLUMNA    :   columna'
    pass

def p_fila(p):
    'FILA   :   fila'
    pass

def p_comentario(p):
    '''COMENTARIO   :   llave_abre COM llave_cierra
                    |   parentecis_abre COM parentecis_cierra
                    |   lambda'''
    pass

def p_com(p):
    '''COM  :   COMENTARIO_REAL MOVIMIENTO_OPCIONAL COMENTARIO COM
            |   lambda'''
    pass

def p_comentario_real(p):
    '''COMENTARIO_REAL      :   palabra COMENTARIO_REAL
                            |   lambda'''
    pass

def p_movimiento_opcional(p):
    '''MOVIMIENTO_OPCIONAL  :   NUMERO_OPCIONAL MOVIMIENTO
                            |   lambda'''
    pass

def p_numero_opcional(p):
    '''NUMERO_OPCIONAL  :   NUMERO_JUGADA PUNTOS_OPCIONALES'''
    pass

def p_puntos_opcionales(p):
    '''PUNTOS_OPCIONALES    :   punto
                            |   punto punto punto
                            |   lambda'''
    pass

def p_lambda(p):
    'lambda :'
    pass

# Error rule for syntax errors
def p_error(p):
    # p[0].valid = False
    print("Syntax error")

# Build the parser
parser = yacc.yacc(debug=True)

if __name__ == '__main__':

    while True:
        try:
            s = input('calc > ')
        except EOFError:
            break
        if not s: continue
        result = parser.parse(s)
        print(result)