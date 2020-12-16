import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from tokenizer import tokens

def p_start(p):
    '''S    :   METADATA JUGADAS S
            |   METADATA JUGADAS
            |   JUGADAS S
            |   JUGADAS'''

    # p[0] = "Parseado S"
    

def p_metadata(p):
    '''METADATA : ITEM_METADATA METADATA
                | ITEM_METADATA'''
    pass

# def p_metadata_error(p):
#     '''METADATA : ITEM_METADATA error METADATA'''
#     print("ERROR EN METADATA: ", p)

def p_item_metadata(p):
    'ITEM_METADATA  :   corchete_abre palabra espacio comilla COMENTARIO_REAL comilla corchete_cierra renglon'
    pass

def p_jugadas(p):
    '''JUGADAS  : JUGADA JUGADAS
                | MOVIMIENTO_FINAL renglon
                | MOVIMIENTO_FINAL '''
    

def p_movimiento_final(p):
    '''MOVIMIENTO_FINAL :   gano_blanco
                        |   gano_negro
                        |   empate'''
    

# def p_jugada(p):
#     '''JUGADA   :   numero_jugada_blanco espacio COMENTARIO espacio MOVIMIENTO COMENTARIO NUMERO_JUGADA_OPCIONAL espacio MOVIMIENTO espacio COMENTARIO espacio
#                 |   numero_jugada_blanco espacio COMENTARIO espacio MOVIMIENTO espacio COMENTARIO NUMERO_JUGADA_OPCIONAL espacio MOVIMIENTO espacio
#                 |   numero_jugada_blanco espacio COMENTARIO espacio MOVIMIENTO espacio NUMERO_JUGADA_OPCIONAL espacio MOVIMIENTO espacio COMENTARIO espacio
#                 |   numero_jugada_blanco espacio COMENTARIO espacio MOVIMIENTO espacio NUMERO_JUGADA_OPCIONAL espacio MOVIMIENTO espacio
#                 |   numero_jugada_blanco espacio MOVIMIENTO espacio COMENTARIO espacio NUMERO_JUGADA_OPCIONAL espacio MOVIMIENTO espacio COMENTARIO espacio
#                 |   numero_jugada_blanco espacio MOVIMIENTO espacio COMENTARIO espacio NUMERO_JUGADA_OPCIONAL espacio MOVIMIENTO espacio
#                 |   numero_jugada_blanco espacio MOVIMIENTO espacio NUMERO_JUGADA_OPCIONAL espacio MOVIMIENTO COMENTARIO espacio
#                 |   numero_jugada_blanco espacio MOVIMIENTO espacio NUMERO_JUGADA_OPCIONAL espacio MOVIMIENTO espacio
#                 |   numero_jugada_blanco espacio COMENTARIO espacio MOVIMIENTO espacio COMENTARIO espacio MOVIMIENTO COMENTARIO espacio
#                 |   numero_jugada_blanco espacio COMENTARIO espacio MOVIMIENTO espacio COMENTARIO espacio MOVIMIENTO espacio
#                 |   numero_jugada_blanco espacio COMENTARIO espacio MOVIMIENTO espacio MOVIMIENTO espacio COMENTARIO espacio
#                 |   numero_jugada_blanco espacio COMENTARIO espacio MOVIMIENTO espacio MOVIMIENTO espacio
#                 |   numero_jugada_blanco espacio MOVIMIENTO espacio COMENTARIO espacio MOVIMIENTO espacio COMENTARIO espacio
#                 |   numero_jugada_blanco espacio MOVIMIENTO espacio COMENTARIO espacio MOVIMIENTO espacio
#                 |   numero_jugada_blanco espacio MOVIMIENTO espacio MOVIMIENTO espacio COMENTARIO espacio
#                 |   numero_jugada_blanco espacio MOVIMIENTO espacio MOVIMIENTO espacio
#                 |   numero_jugada_blanco espacio MOVIMIENTO espacio COMENTARIO espacio
#                 |   numero_jugada_blanco espacio MOVIMIENTO espacio'''
#     pass

# def p_jugada(p):
#     '''JUGADA   :   numero_jugada_blanco espacio MOVIMIENTO espacio COMENTARIO espacio numero_jugada_negro espacio MOVIMIENTO espacio COMENTARIO espacio
#                 |   numero_jugada_blanco espacio MOVIMIENTO espacio numero_jugada_negro espacio MOVIMIENTO espacio COMENTARIO espacio
#                 |   numero_jugada_blanco espacio MOVIMIENTO espacio COMENTARIO espacio numero_jugada_negro espacio MOVIMIENTO espacio
#                 |   numero_jugada_blanco espacio MOVIMIENTO espacio numero_jugada_negro espacio MOVIMIENTO espacio
#                 |   numero_jugada_blanco espacio MOVIMIENTO espacio MOVIMIENTO espacio
#                 |   numero_jugada_blanco espacio MOVIMIENTO espacio COMENTARIO espacio
#                 |   numero_jugada_blanco espacio MOVIMIENTO espacio'''

def p_jugada(p):
    '''JUGADA   :   numero_jugada_blanco MOVIMIENTO J2
                |   numero_jugada_blanco MOVIMIENTO'''

def p_J2(p):
    '''J2       :   COMENTARIO numero_jugada_negro MOVIMIENTO COMENTARIO
                |   COMENTARIO numero_jugada_negro MOVIMIENTO 
                |   numero_jugada_negro MOVIMIENTO COMENTARIO 
                |   numero_jugada_negro MOVIMIENTO 
                |   MOVIMIENTO COMENTARIO
                |   MOVIMIENTO
                |   COMENTARIO'''

# def p_JugadaCont2(p):
#     '''J2   :    espacio MOVIMIENTO J3
#             |   numero_jugada_negro espacio MOVIMIENTO J3
#             |   MOVIMIENTO J3'''
#     pass

# def p_JugadaCont3(p):
#     '''J3   :   COMENTARIO espacio
#             |   espacio'''
#     pass

# def p_numero_jugada(p):
#     'NUMERO_JUGADA  :   numero'
#     pass

# def p_numero_jugada_opcional(p):
#     '''NUMERO_JUGADA_OPCIONAL   :   numero_jugada_negro'''
    #  espacio COMENTARIO
    #                             |   numero_jugada_negro'''
    # pass

# def p_movimiento(p):
#     '''MOVIMIENTO   :   PIEZA POS_OPCIONAL equis PIEZA POS ESPECIAL
#                     |   PIEZA POS_OPCIONAL PIEZA POS ESPECIAL
#                     |   PIEZA equis POS ESPECIAL
#                     |   PIEZA POS ESPECIAL
#                     |   PIEZA POS_OPCIONAL equis POS ESPECIAL
#                     |   PIEZA POS_OPCIONAL POS ESPECIAL
#                     |   POS_OPCIONAL equis PIEZA POS ESPECIAL
#                     |   POS_OPCIONAL PIEZA POS ESPECIAL
#                     |   equis POS ESPECIAL
#                     |   POS ESPECIAL
#                     |   enroque_1 ESPECIAL
#                     |   enroque_2 ESPECIAL
#                     |   PIEZA POS_OPCIONAL equis PIEZA POS
#                     |   PIEZA POS_OPCIONAL PIEZA POS
#                     |   PIEZA equis POS
#                     |   PIEZA POS
#                     |   PIEZA POS_OPCIONAL equis POS
#                     |   PIEZA POS_OPCIONAL POS
#                     |   POS_OPCIONAL equis PIEZA POS
#                     |   POS_OPCIONAL PIEZA POS
#                     |   equis POS
#                     |   POS
#                     |   enroque_1
#                     |   enroque_2'''
                    
#     pass

def p_movimiento(p):
    '''MOVIMIENTO   :   token_movimiento ESPECIAL
                    |   enroque_1 ESPECIAL
                    |   enroque_2 ESPECIAL
                    |   token_movimiento
                    |   enroque_1
                    |   enroque_2'''
    pass 

# def p_equis(p):
#     '''X    :   equis'''
#     pass

# def p_pos_opcional(p):
#     '''POS_OPCIONAL :   palabra numero
#                     |   palabra
#                     |   numero'''
#     pass

# def p_pos(p):
#     'POS    :   palabra numero'
#     pass

def p_especial(p):
    '''ESPECIAL :   jaque_mate
                |   jaque'''
    pass

# def p_pieza(p):
#     '''PIEZA    :   pieza'''
#     pass

def p_comentario(p):
    '''COMENTARIO   :   llave_abre COM llave_cierra
                    |   parentecis_abre COM parentecis_cierra
                    |   llave_abre llave_cierra
                    |   parentecis_abre parentecis_cierra'''
    pass

def p_com(p):
    '''COM  :   palabra COM 
            |   MOVIMIENTO_OPCIONAL COM
            |   COMENTARIO COM
            |   espacio COM
            |   palabra
            |   MOVIMIENTO_OPCIONAL 
            |   COMENTARIO
            |   espacio'''
    pass

def p_comentario_real(p):
    '''COMENTARIO_REAL      :   palabra espacio COMENTARIO_REAL
                            |   palabra '''
    pass

    
def p_movimiento_opcional(p):
    '''MOVIMIENTO_OPCIONAL  :   token_movimiento'''
    pass

# def p_numero_opcional(p):
#     '''NUMERO_OPCIONAL  :   NUMERO_JUGADA PUNTOS_OPCIONALES
#                         |   NUMERO_JUGADA'''
#     pass

# def p_puntos_opcionales(p):
#     '''PUNTOS_OPCIONALES    :   punto
#                             |   punto punto punto'''
#     pass

# def p_lambda(p):
#     'lambda :'
#     pass

class LexerError(BaseException): pass

# Error rule for syntax errors
def p_error(p):
    # p[0].valid = False
    if p is None:
        print("EOF!!!")
    else:
        print("TOKEN QUE CAUSO EL ERROR: ", p)
        raise LexerError("Input invalido")

# Build the parser
parser = yacc.yacc(debug=True)

if __name__ == '__main__':

    f = open("testeo.txt", "r")
    s = f.read()
    print("Parseando . . .")
    try:
        result = parser.parse(s)
    except LexerError as err:
        print(err)
    else:
        print("OK")