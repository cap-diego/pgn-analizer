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
    '''JUGADA   :   numero_jugada_blanco COMENTARIO MOVIMIENTO COMENTARIO NUMERO_JUGADA_OPCIONAL MOVIMIENTO COMENTARIO
                |   numero_jugada_blanco COMENTARIO MOVIMIENTO COMENTARIO NUMERO_JUGADA_OPCIONAL MOVIMIENTO
                |   numero_jugada_blanco COMENTARIO MOVIMIENTO NUMERO_JUGADA_OPCIONAL MOVIMIENTO COMENTARIO
                |   numero_jugada_blanco COMENTARIO MOVIMIENTO NUMERO_JUGADA_OPCIONAL MOVIMIENTO 
                |   numero_jugada_blanco MOVIMIENTO COMENTARIO NUMERO_JUGADA_OPCIONAL MOVIMIENTO COMENTARIO
                |   numero_jugada_blanco MOVIMIENTO COMENTARIO NUMERO_JUGADA_OPCIONAL MOVIMIENTO
                |   numero_jugada_blanco MOVIMIENTO NUMERO_JUGADA_OPCIONAL MOVIMIENTO COMENTARIO
                |   numero_jugada_blanco MOVIMIENTO NUMERO_JUGADA_OPCIONAL MOVIMIENTO
                |   numero_jugada_blanco COMENTARIO MOVIMIENTO COMENTARIO MOVIMIENTO COMENTARIO
                |   numero_jugada_blanco COMENTARIO MOVIMIENTO COMENTARIO MOVIMIENTO
                |   numero_jugada_blanco COMENTARIO MOVIMIENTO MOVIMIENTO COMENTARIO
                |   numero_jugada_blanco COMENTARIO MOVIMIENTO MOVIMIENTO 
                |   numero_jugada_blanco MOVIMIENTO COMENTARIO MOVIMIENTO COMENTARIO
                |   numero_jugada_blanco MOVIMIENTO COMENTARIO MOVIMIENTO
                |   numero_jugada_blanco MOVIMIENTO MOVIMIENTO COMENTARIO
                |   numero_jugada_blanco MOVIMIENTO MOVIMIENTO'''
    pass

# def p_numero_jugada(p):
#     'NUMERO_JUGADA  :   numero'
#     pass

def p_numero_jugada_opcional(p):
    '''NUMERO_JUGADA_OPCIONAL   :   numero_jugada_negro COMENTARIO
                                |   numero_jugada_negro'''
    pass

def p_movimiento(p):
    '''MOVIMIENTO   :   PIEZA POS_OPCIONAL equis PIEZA POS ESPECIAL
                    |   PIEZA POS_OPCIONAL PIEZA POS ESPECIAL
                    |   PIEZA equis POS ESPECIAL
                    |   PIEZA POS ESPECIAL
                    |   PIEZA POS_OPCIONAL equis POS ESPECIAL
                    |   PIEZA POS_OPCIONAL POS ESPECIAL
                    |   POS_OPCIONAL equis PIEZA POS ESPECIAL
                    |   POS_OPCIONAL PIEZA POS ESPECIAL
                    |   equis POS ESPECIAL
                    |   POS ESPECIAL
                    |   enroque_1 ESPECIAL
                    |   enroque_2 ESPECIAL
                    |   PIEZA POS_OPCIONAL equis PIEZA POS
                    |   PIEZA POS_OPCIONAL PIEZA POS
                    |   PIEZA equis POS
                    |   PIEZA POS
                    |   PIEZA POS_OPCIONAL equis POS
                    |   PIEZA POS_OPCIONAL POS
                    |   POS_OPCIONAL equis PIEZA POS
                    |   POS_OPCIONAL PIEZA POS
                    |   equis POS
                    |   POS
                    |   enroque_1
                    |   enroque_2'''
                    
    pass

# def p_equis(p):
#     '''X    :   equis'''
#     pass

def p_pos_opcional(p):
    '''POS_OPCIONAL :   palabra numero
                    |   palabra
                    |   numero'''
    pass

def p_pos(p):
    'POS    :   palabra numero'
    pass

def p_especial(p):
    '''ESPECIAL :   jaque_mate
                |   jaque'''
    pass

def p_pieza(p):
    '''PIEZA    :   pieza'''
    pass

def p_comentario(p):
    '''COMENTARIO   :   llave_abre COM llave_cierra
                    |   parentecis_abre COM parentecis_cierra
                    |   llave_abre llave_cierra
                    |   parentecis_abre parentecis_cierra'''
    pass

def p_com(p):
    '''COM  :   COMENTARIO_REAL COM 
            |   MOVIMIENTO_OPCIONAL COM
            |   COMENTARIO COM
            |   COMENTARIO_REAL
            |   MOVIMIENTO_OPCIONAL 
            |   COMENTARIO'''
    pass

def p_comentario_real(p):
    '''COMENTARIO_REAL      :   palabra espacio COMENTARIO_REAL
                            |   palabra'''
    pass

def p_movimiento_opcional(p):
    '''MOVIMIENTO_OPCIONAL  :   NUMERO_OPCIONAL token_movimiento
                            |   token_movimiento'''
    pass

def p_numero_opcional(p):
    '''NUMERO_OPCIONAL  :   NUMERO_JUGADA PUNTOS_OPCIONALES
                        |   NUMERO_JUGADA'''
    pass

def p_puntos_opcionales(p):
    '''PUNTOS_OPCIONALES    :   punto
                            |   punto punto punto'''
    pass

def p_lambda(p):
    'lambda :'
    pass

# Error rule for syntax errors
def p_error(p):
    # p[0].valid = False
    if p is None:
        print("EOF!!!")
    else:
        print("TOKEN QUE CAUSO EL ERROR: ", p)

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