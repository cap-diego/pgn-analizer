import ply.yacc as yacc
import sys

# Importar mapa de tokens del lexer.
from tokenizer import tokens
import tokenizer

# Definicion de atributos 
movimiento_tiene_captura = False
cantidad_capturas = 0 # Cantidad de capturas totales
capturas_por_partida = [] # Cada elemento representa la cantidad de capturas de una partida
capturas_texto_por_partida = [] # Cada elementeo representa las capturas realizadas en la partida en forma de texto
captura_texto = "" # Captura en forma de texto todas las capturas de una partida
ultima_jugada = 0 # Contador para verificar que las partidas estén numeradas correctamente
ganadores = [] # Arreglo con los resultados de cada partida

def p_start(p):
    '''S    :   METADATA JUGADAS S'''
    p[0] = {'cantidad_capturas': p[2]['cantidad_capturas']}
    p[0]['captura_texto'] = p[2]['captura_texto']

    global cantidad_capturas  
    global captura_texto
    global capturas_por_partida
    global capturas_texto_por_partida

    cantidad_capturas += p[0]['cantidad_capturas']
    captura_texto += p[0]['captura_texto'].replace("  ", "")
    capturas_por_partida.append(p[0]['cantidad_capturas'])
    capturas_texto_por_partida.append("[" + p[0]['captura_texto'].replace("  ", "") + "]")


def p_start_2(p):
    '''S    :   METADATA JUGADAS'''
    p[0] = {'cantidad_capturas': p[2]['cantidad_capturas']}
    p[0]['captura_texto'] = p[2]['captura_texto']

    global cantidad_capturas
    global captura_texto
    global capturas_por_partida
    global capturas_texto_por_partida

    cantidad_capturas += p[0]['cantidad_capturas']
    captura_texto += p[0]['captura_texto']
    capturas_por_partida.append(p[0]['cantidad_capturas'])
    capturas_texto_por_partida.append("[" + p[0]['captura_texto'].replace("  ", "") + "]")

def p_start_jugadas(p):
    '''S    :   JUGADAS'''
    p[0] = {'cantidad_capturas': p[1]['cantidad_capturas']}
    p[0]['captura_texto'] = p[1]['captura_texto']
    
    global cantidad_capturas  
    global captura_texto
    global capturas_por_partida
    global capturas_texto_por_partida

    cantidad_capturas += p[0]['cantidad_capturas']
    captura_texto += p[0]['captura_texto'] 
    capturas_por_partida.append(p[0]['cantidad_capturas'])
    capturas_texto_por_partida.append("[" + p[0]['captura_texto'].replace("  ", "") + "]")

def p_start_jugadas_s(p):
    '''S    :   JUGADAS S'''
    p[0] = {'cantidad_capturas': p[1]['cantidad_capturas']}
    p[0]['captura_texto'] = p[1]['captura_texto']
    
    global cantidad_capturas  
    global captura_texto
    global capturas_por_partida
    global capturas_texto_por_partida

    cantidad_capturas += p[0]['cantidad_capturas']
    captura_texto += p[0]['captura_texto']
    capturas_por_partida.append(p[0]['cantidad_capturas'])
    capturas_texto_por_partida.append("[" + p[0]['captura_texto'].replace("  ", "") + "]")
    
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
    p[0]['captura_texto'] = p[1]['captura_texto'] + " " + p[2]['captura_texto']
    

def p_jugadas2(p):
    '''JUGADAS  :    MOVIMIENTO_FINAL renglon
                |    MOVIMIENTO_FINAL'''
    p[0] = {'cantidad_capturas': 0}
    p[0]['captura_texto'] = ""

def p_movimiento_final(p):
    '''MOVIMIENTO_FINAL :   gano_blanco
                        |   gano_negro
                        |   empate'''
    # Llegamos al final de la partida, reseteamos los indices de la jugada
    global ultima_jugada
    ultima_jugada = 0
    
    # Guardamos al ganaror
    global ganadores
    ganador = "blanco" if p[1] == "1-0" else "negro" if p[1] == "0-1" else "empate"
    ganadores.append(ganador)
    
def p_jugada(p):
    '''JUGADA   :   numero_jugada_blanco MOVIMIENTO J2'''
    numero_jugada = int(p[1].split(".")[0])

    global ultima_jugada
    if numero_jugada != ultima_jugada + 1:
        raise LexerError("Número de Jugada invalido: llegó {} y se esperaba {}".format(numero_jugada, ultima_jugada + 1))
    
    ultima_jugada += 1

    if(p[3]['tiene_num']):
        numero_jugada_aparte = int(p[3]['numero_aparte'].split("...")[0])

        if numero_jugada_aparte != numero_jugada:
            raise LexerError("ERROR - Número de jugada del jugador negro no coincide con la del blanco, llegó {} y se esperaba {}".format(numero_jugada_aparte, numero_jugada))

    p[0] = {'cantidad_capturas': p[2]['tiene_captura'] + p[3]['cantidad_capturas']}
    p[0]['captura_texto'] = ""
    
    if p[2]['tiene_captura']:
        p[0]['captura_texto'] += p[1] + " " + p[2]['captura_texto'] + " "
    if p[3]['cantidad_capturas'] > 0:
        p[0]['captura_texto'] += ("" if p[2]['tiene_captura'] else p[1] + " ") + p[3]['captura_texto'] + " "
    
    p[0]['captura_texto'] += "," if p[2]['tiene_captura'] or p[3]['cantidad_capturas'] > 0 else ""

def p_jugada_2(p): 
    '''JUGADA   :   numero_jugada_blanco MOVIMIENTO'''
    numero_jugada = int(p[1].split(".")[0])

    global ultima_jugada
    if numero_jugada != ultima_jugada + 1:
        raise LexerError("ERROR - Número de Jugada invalido, llegó {} y se esperaba {}".format(numero_jugada, ultima_jugada + 1))
    
    ultima_jugada += 1
    
    p[0] = {'cantidad_capturas': p[2]['tiene_captura']}
    p[0]['captura_texto'] = ""
    if p[0]['cantidad_capturas'] > 0:
        p[0]['captura_texto'] = p[1] + p[2]['captura_texto'] + ","

def p_J2(p):
    '''J2   :   COMENTARIO numero_jugada_negro MOVIMIENTO COMENTARIO'''
    
    p[0] = {'cantidad_capturas': p[1]['cantidad_capturas'] + p[3]['tiene_captura'] + p[4]['cantidad_capturas']}
    p[0]['captura_texto'] = p[1]['captura_texto'] + " " + p[3]['captura_texto'] + " " + p[4]['captura_texto']
    p[0]['numero_aparte'] = p[2]
    p[0]['tiene_num'] = True
    
def p_J22(p):
    '''J2   :   COMENTARIO numero_jugada_negro MOVIMIENTO '''
    
    p[0] = {'cantidad_capturas': p[1]['cantidad_capturas'] + p[3]['tiene_captura']}
    p[0]['captura_texto'] = p[1]['captura_texto'] + " " + p[3]['captura_texto'] + " "
    p[0]['numero_aparte'] = p[2]
    p[0]['tiene_num'] = True

def p_J23(p):
    '''J2   :   numero_jugada_negro MOVIMIENTO COMENTARIO '''

    p[0] = {'cantidad_capturas': p[2]['tiene_captura'] + p[3]['cantidad_capturas']}
    p[0]['captura_texto'] = p[2]['captura_texto'] + " " + p[3]['captura_texto']
    p[0]['numero_aparte'] = p[1]
    p[0]['tiene_num'] = True

def p_J24(p):
    '''J2   :   numero_jugada_negro MOVIMIENTO'''

    p[0] = {'cantidad_capturas': p[2]['tiene_captura']} 
    p[0]['captura_texto'] = p[2]['captura_texto']
    p[0]['numero_aparte'] = p[1]
    p[0]['tiene_num'] = True

def p_J2_comentario(p):
    '''J2   :   COMENTARIO'''
    p[0] = {'cantidad_capturas': p[1]['cantidad_capturas']}
    p[0]['captura_texto'] = p[1]['captura_texto']
    p[0]['tiene_num'] = False

def p_J2_movimiento(p):
    '''J2   :   MOVIMIENTO'''
    p[0] = {'cantidad_capturas': p[1]['tiene_captura']}
    p[0]['captura_texto'] = p[1]['captura_texto']
    p[0]['tiene_num'] = False

def p_J2_movimiento_comentario(p):
    '''J2   :   MOVIMIENTO COMENTARIO'''
    p[0] = {'cantidad_capturas': p[1]['tiene_captura'] + p[2]['cantidad_capturas']}
    p[0]['captura_texto'] = p[1]['captura_texto'] + " " + p[2]['captura_texto']
    p[0]['tiene_num'] = False
    
def p_movimiento(p):
    '''MOVIMIENTO   :   token_movimiento ESPECIAL'''
    p[0] = {'tiene_captura' : 1 if "x" in str(p[1]).lower() else 0}
    p[0]['captura_texto'] = p[1] if "x" in str(p[1]).lower() else ""


def p_movimiento_enroque(p):
    '''MOVIMIENTO   :   enroque_1 ESPECIAL
                    |   enroque_1 
                    |   enroque_2 ESPECIAL
                    |   enroque_2 '''
    p[0] = {'tiene_captura': 0}
    p[0]['captura_texto'] = ""

def p_movimiento_token_movimiento(p):
    '''MOVIMIENTO   : token_movimiento'''
    p[0] = {'tiene_captura' : 1 if "x" in str(p[1]).lower() else 0}
    p[0]['captura_texto'] = p[1] if "x" in str(p[1]).lower() else ""

def p_especial(p):
    '''ESPECIAL :   jaque_mate
                |   jaque'''

def p_comentario(p):
    '''COMENTARIO   :   llave_abre COM llave_cierra'''
    p[0] = {'cantidad_capturas': p[2]['cantidad_capturas']}
    p[0]['captura_texto'] = p[2]['captura_texto']

def p_comentario_parentesis_abre_solo(p):
    '''COMENTARIO  : parentecis_abre parentecis_cierra'''    
    p[0] = {'cantidad_capturas': 0}
    p[0]['captura_texto'] = ""

def p_comentario_parentesis_abre(p):
    '''COMENTARIO  : parentecis_abre COM parentecis_cierra'''
    p[0] = {'cantidad_capturas': p[2]['cantidad_capturas']}
    p[0]['captura_texto'] = p[2]['captura_texto']

def p_comentario_llave_abre_solo(p):
    '''COMENTARIO   :    llave_abre llave_cierra'''
    p[0] = {'cantidad_capturas': 0}
    p[0]['captura_texto'] = ""

def p_com(p):
    '''COM  :   palabra
            |   espacio'''
            
    p[0] = {'cantidad_capturas': 0}
    p[0]['captura_texto'] = ""

def p_com2(p):
    '''COM  :   palabra COM 
            |   espacio COM'''
    p[0] = {'cantidad_capturas': p[2]['cantidad_capturas']}
    p[0]['captura_texto'] = p[2]['captura_texto']

def p_com3(p):
    '''COM  :   token_movimiento COM
            |   token_movimiento'''
    
    val = 0 if len(p) <= 2 else p[2]['cantidad_capturas']
    p[0] = {'cantidad_capturas' : (1 if "x" in str(p[1]).lower() else 0) + val}

    val2 = "" if len(p) <= 2 else  p[2]['captura_texto']
    p[0]['captura_texto'] = (p[1] if "x" in str(p[1]).lower() else "") + " " + val2

def p_com4(p):
    '''COM  :   COMENTARIO COM
            |   COMENTARIO '''
    val = p[2]['cantidad_capturas'] if len(p) > 2 else 0
    p[0] = {'cantidad_capturas': p[1]['cantidad_capturas'] + val}
    
    val2 = "" if len(p) <= 2 else  p[2]['captura_texto']
    p[0]['captura_texto'] = p[1]['captura_texto'] + " " + val2

def p_comentario_real(p):
    '''COMENTARIO_REAL      :   palabra espacio COMENTARIO_REAL
                            |   palabra'''

# Clase para mostrar errores
class LexerError(BaseException): pass

# Error rule for syntax errors
def p_error(p):
    # p[0].valid = False
    if p is None:
        #print(tokenizer.en_comentario)
        if tokenizer.en_comentario != 0:
            raise LexerError("ERROR - Los paréntesis o corchetes de comentarios no están balanceados")
        else:
            raise LexerError("ERROR - Llegó a EOF sin terminar de procesar")
    else:
        #print("Error, token {} no esperado".format(p.value))
        raise LexerError("ERROR - token {} no esperado en línea {}".format(p.type, p.lineno))

# Build the parser
parser = yacc.yacc(debug=True)

# Codigo para leer los archivos de input
def programa_principal():
    if(len(sys.argv) != 2):
        print("ERROR - EL PROGRAMA SOLO TOMA UN ARGUMENTO")
        return
    
    f = open(sys.argv[1], "r")

    s = f.read()
    print("Parseando . . .")
    try:
        result = parser.parse(s)
    except LexerError as err:
        print(err)
    else:
        print("Lectura Finalizada")
        
        # Invierto los arreglos con los datos ya que se forman al revés
        capturas_por_partida.reverse()
        capturas_texto_por_partida.reverse()
        
        print("Cantidad de capturas por partida: ", capturas_por_partida)
        
        print("Capturas por partida: ")
        for i in range(len(capturas_texto_por_partida)):
            print("Partida {}: {}".format(i+1, capturas_texto_por_partida[i]))
        
        print("Cantidad de capturas totales: ", sum(capturas_por_partida))
        print("Ganadores: ", ganadores)
    
    f.close()

if __name__ == '__main__':
    programa_principal()
