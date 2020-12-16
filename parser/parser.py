import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from tokenizer import tokens

# Definicion de atributos 
movimiento_tiene_captura = False
cantidad_capturas = 0

def p_start(p):
    '''S    :   METADATA JUGADAS S'''
    p[0] = {'cantidad_capturas': p[2]['cantidad_capturas']}
    global cantidad_capturas  
    cantidad_capturas += p[0]['cantidad_capturas']

def p_start_2(p):
    '''S    :   METADATA JUGADAS'''
    p[0] = {'cantidad_capturas': p[2]['cantidad_capturas']}
    global cantidad_capturas  
    cantidad_capturas += p[0]['cantidad_capturas']

def p_start_jugadas(p):
    '''S : JUGADAS'''
    p[0] = {'cantidad_capturas': p[1]['cantidad_capturas']}
    global cantidad_capturas  
    cantidad_capturas += p[0]['cantidad_capturas']

def p_start_jugadas_s(p):
    '''S : JUGADAS S'''
    p[0] = {'cantidad_capturas': p[1]['cantidad_capturas'] + p[2]['cantidad_capturas']}
    global cantidad_capturas  
    cantidad_capturas += p[0]['cantidad_capturas']

def p_metadata(p):
    '''METADATA : ITEM_METADATA METADATA
                | ITEM_METADATA'''
    pass

def p_item_metadata(p):
    'ITEM_METADATA  :   corchete_abre palabra espacio comilla COMENTARIO_REAL comilla corchete_cierra renglon'
    pass

def p_jugadas(p):
    '''JUGADAS  : JUGADA JUGADAS'''
    p[0] = {'cantidad_capturas': p[1]['cantidad_capturas'] + p[2]['cantidad_capturas']}
    

def p_jugadas2(p):
    '''JUGADAS  :    MOVIMIENTO_FINAL renglon
                |    MOVIMIENTO_FINAL'''
    p[0] = {'cantidad_capturas': 0}

def p_movimiento_final(p):
    '''MOVIMIENTO_FINAL :   gano_blanco
                        |   gano_negro
                        |   empate'''
    
def p_jugada(p):
    '''JUGADA   :   numero_jugada_blanco MOVIMIENTO J2'''
    p[0] = {'cantidad_capturas': p[2]['tiene_captura'] + p[3]['cantidad_capturas']}

def p_jugada_(p): 
    '''JUGADA   : numero_jugada_blanco MOVIMIENTO'''
    p[0] = {'tiene_captura': p[2]['tiene_captura']}

def p_J2(p):
    '''J2       :   COMENTARIO numero_jugada_negro MOVIMIENTO COMENTARIO'''
    p[0] = {p[1]['cantidad_capturas'] + p[3]['tiene_captura'] + p[4]['cantidad_capturas']}
    
def p_J22(p):
    '''J2   :   COMENTARIO numero_jugada_negro MOVIMIENTO '''
    p[0] = {'cantidad_capturas': p[1]['cantidad_capturas'] + p[3]['tiene_captura']}

def p_J23(p):
    '''J2   :   numero_jugada_negro MOVIMIENTO COMENTARIO '''
    p[0] = {'cantidad_capturas': p[2]['tiene_captura'] + p[3]['cantidad_capturas']}

def p_J24(p):
    '''J2   :   numero_jugada_negro MOVIMIENTO'''
    p[0] = {'cantidad_capturas': p[2]['tiene_captura']} 

def p_J2_comentario(p):
    '''J2 : COMENTARIO'''
    p[0] = {'cantidad_capturas': p[1]['cantidad_capturas']}

def p_J2_movimiento(p):
    '''J2 : MOVIMIENTO'''
    p[0] = {'cantidad_capturas': p[1]['tiene_captura']}

def p_J2_movimiento_comentario(p):
    '''J2 : MOVIMIENTO COMENTARIO'''
    p[0] = {'cantidad_capturas': p[1]['tiene_captura'] + p[2]['cantidad_capturas']}
    
def p_movimiento(p):
    '''MOVIMIENTO   :   token_movimiento ESPECIAL'''
    p[0] = {'tiene_captura' : 1 if "x" in str(p[1]).lower() else 0}


def p_movimiento_enroque_1_especial(p):
    '''MOVIMIENTO   :   enroque_1 ESPECIAL'''
    p[0] = {'tiene_captura': 0}

def p_movimiento_enroque_2_especial(p):
    '''MOVIMIENTO   :   enroque_2 ESPECIAL'''
    p[0] = {'tiene_captura': 0}

def p_movimiento_enroque_1(p):
    '''MOVIMIENTO   :   enroque_1'''
    p[0] = {'tiene_captura': 0}
    
def p_movimiento_enroque_2(p):
    '''MOVIMIENTO   :   enroque_2'''
    p[0] = {'tiene_captura': 0}


def p_movimiento_token_movimiento(p):
    '''MOVIMIENTO   : token_movimiento'''
    p[0] = {'tiene_captura' : 1 if "x" in str(p[1]).lower() else 0}

def p_especial(p):
    '''ESPECIAL :   jaque_mate
                |   jaque'''

def p_comentario(p):
    '''COMENTARIO   :   llave_abre COM llave_cierra'''
    p[0] = {'cantidad_capturas': p[2]['cantidad_capturas']}

def p_comentario_parentesis_abre_solo(p):
    '''COMENTARIO  : parentecis_abre parentecis_cierra'''    
    p[0] = {'cantidad_capturas': 0}
    
def p_comentario_parentesis_abre(p):
    '''COMENTARIO  : parentecis_abre COM parentecis_cierra'''
    p[0] = {'cantidad_capturas': p[2]['cantidad_capturas']}
    
def p_comentario_llave_abre_solo(p):
    '''COMENTARIO   :    llave_abre llave_cierra'''
    p[0] = {'cantidad_capturas': 0}

def p_com(p):
    '''COM  :   palabra
            |   espacio'''
            
    p[0] = {'cantidad_capturas': 0}

def p_com2(p):
    '''COM  :   palabra COM 
            |   espacio COM'''
    p[0] = {'cantidad_capturas': p[2]['cantidad_capturas']}

def p_com3(p):
    '''COM  :   MOVIMIENTO_OPCIONAL COM
            |   MOVIMIENTO_OPCIONAL'''
    
    val = 0 if len(p) <= 2 else p[2]['cantidad_capturas']
    p[0] = {'cantidad_capturas' : p[1]['cantidad_capturas'] + val} 

def p_com4(p):
    '''COM  :   COMENTARIO COM
            |   COMENTARIO '''
    val = p[2]['cantidad_capturas'] if len(p) > 2 else 0
    p[0] = {'cantidad_capturas': p[1]['cantidad_capturas'] + val}

def p_comentario_real(p):
    '''COMENTARIO_REAL      :   palabra espacio COMENTARIO_REAL
                            |   palabra '''

def p_movimiento_opcional(p):
    '''MOVIMIENTO_OPCIONAL  :   token_movimiento'''
    p[0] = {'cantidad_capturas': 1 if "x" in str(p[1]).lower() else 0}

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
        print("Cantidad de capturas {}".format(cantidad_capturas))
    
    f.close()