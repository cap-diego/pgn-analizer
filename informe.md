<style type="text/css">

table {
  width: calc(100% - 20px);
  margin: 30px 10px;
  font-family: monospace;
}

code {
  text-align: left;
}

</style>
<div style="text-align: justify">

# Trabajo práctico Teoría de Lenguajes

## Integrantes
- Tasat, Dylan - 29/17 - dylantasat11@gmail.com 
- Springhart, Gonzalo Leandro - 308/17 - glspringhart@gmail.com 
- Buceta, Diego - 001/17 - diegobuceta35@gmail.com

## **Introducción**

Para este trabajo creamos un programa que permita reconocer archivos PGN, vamos a explicar la gramática utilizada para reconocer tales archivos y explicar las distintas decisiones de implementación que tomamos a lo largo del desarrollo.

### **Formato PGN**

Estos archivos representan partidas de ajedrez mediante una sintaxis bastante flexible, pueden describir cualquier tipo de partida, permitiendo comentarios sobre las mismas y abreviaturas para las jugadas más comunes.

Los archivos de este formato están compuestos por una cantidad de partidas, las cuales están compuestas por metadatos opcionales y las jugadas.

### **Objetivo del trabajo**

Para verificar que los archivos siguen el formato correcto creamos una gramática que verifique que el archivo sea una cadena válida del lenguaje, luego agregaremos a sus producciones una serie de atributos que nos permitan conocer los datos necesarios, estos son:
- Mostrar la cantidad de jugadas de captura mencionadas a lo largo de cada partida.
  - Incluyendo las de los comentarios.
- Mostrar las jugadas de captura mencionadas a lo largo de cada partida.
- Validar que la numeración de las jugadas sea correcta para todas las partidas.
  - Tienen que comenzar por 1.
  - Tienen que avanzar de forma ascendente.
  - Si una jugada del blanco va antecedida de número y punto, la siguiente, del negro, no deberá tener número ni puntos o bien podrá tener el mismo número que la última del blanco seguido de tres puntos.

Luego utilizaremos la herramienta PLY y YACC que es una combinación de extensiones para Python que nos permiten crear los lexer y parsers que idenfican la gramática.
Haciendo uso de esto, implementaremos nuestra gramática para generar un parser y evaluar los distintos ejemplos de archivos provistos por la cátedra más algunos que encontramos nosotros durante el proceso de investigación.

## **Gramática**
Comencemos describiendo la gramática sin los atributos, esta será una gramática libre de contexto que valide que una cadena pertenezca al lenguaje de los archivos PGN.
Tenemos las siguientes producciones:

### **Terminales**

Los siguientes símbolos son terminales en nuestra gramática:

- `corchete_abre`
- `corchete_cierra`
- `llave_abre`
- `llave_cierra`
- `parentesis_abre`
- `parentesis_cierra`
- `palabra`
- `espacio`
- `comilla`
- `renglon`
- `gano_blanco`
- `gano_negro`
- `empate`
- `numero_jugada_blanco`
- `numero_jugada_negro`
- `jaque`
- `jaque_mate`
- `token_movimiento`

### **No Terminales**

Los siguientes símbolos son no terminales en nuestra gramática:

  - `S`
  - `METADATA`
  - `JUGADAS`
  - `ITEM_METADATA`
  - `JUGADA`
  - `MOVIMIENTO_FINAL`
  - `COMENTARIO`
  - `MOVIMIENTO`
  - `J2`
  - `COM`
  - `MOVIMIENTO_OPCIONAL`
  - `COMENTARIO_REAL`

El símbolo distinguido es `S`

### **Producciones sin reglas**

```
               S → METADATA JUGADAS S
                 | METADATA JUGADAS
                 | JUGADAS S
                 | JUGADAS 

        METADATA → ITEM_METADATA METADATA
                 | ITEM_METADATA 

   ITEM_METADATA → corchete_abre palabra espacio comilla COMENTARIO_REAL comilla corchete_cierra renglon 

 COMENTARIO_REAL →  palabra espacio COMENTARIO_REAL
                 |  palabra

         JUGADAS → JUGADA JUGADAS
                 | MOVIMIENTO_FINAL renglon
                 | MOVIMIENTO_FINAL 

MOVIMIENTO_FINAL → gano_blanco
                 | gano_negro
                 | empate 

          JUGADA → numero_jugada_blanco MOVIMIENTO J2
                 | numero_jugada_blanco MOVIMIENTO 

              J2 → COMENTARIO numero_jugada_negro MOVIMIENTO COMENTARIO
                 | COMENTARIO numero_jugada_negro MOVIMIENTO
                 | numero_jugada_negro MOVIMIENTO COMENTARIO
                 | numero_jugada_negro MOVIMIENTO
                 | MOVIMIENTO COMENTARIO
                 | COMENTARIO
                 | MOVIMIENTO

      MOVIMIENTO → token_movimiento ESPECIAL
                 | token_movimiento

        ESPECIAL →  jaque_mate
                 |  jaque

      COMENTARIO → llave_abre  COM llave_cierra
                 | parentecis_abre COM parentecis_cierra
                 | llave_abre llave_cierra
                 | parentecis_abre parentecis_cierra

             COM → MOVIMIENTO_OPCIONAL COM
                 | COMENTARIO COM
                 | palabra COM
                 | espacio COM
                 | MOVIMIENTO_OPCIONAL
                 | COMENTARIO
                 | palabra
                 | espacio
```

## **Tabla de atributos**

| Atributo                              | Heredado / Sintetizado | Tipo      |
| ------------------------------------- | ---------------------- | --------- |
| S.cantidad_capturas                   | S                      | Array INT |
| JUGADAS.cantidad_capturas             | S                      | INT       |
| JUGADA.cantidad_capturas              | S                      | INT       |
| J2.cantidad_capturas                  | S                      | INT       |
| COMENTARIO.cantidad_capturas          | S                      | INT       |
| COM.cantidad_capturas                 | S                      | INT       |
| MOVIMIENTO_OPCIONAL.cantidad_capturas | S                      | INT       |
| JUGADAS.captura_texto                 | S                      | STRING    |
| JUGADA.captura_texto                  | S                      | STRING    |
| J2.captura_texto                      | S                      | STRING    |
| MOVIMIENTO.captura_texto              | S                      | STRING    |
| COMENTARIO.captura_texto              | S                      | STRING    |
| COM.captura_texto                     | S                      | STRING    |
| MOVIMIENTO_OPCIONAL.captura_texto     | S                      | STRING    |
| JUGADAS.numero_jugada                 | H                      | INT       |
| JUGADA.numero_jugada                  | H                      | INT       |
| J2.tiene_num                          | S                      | BOOLEAN   |
| J2.numero_jugada_negro                | S                      | INT       |
| MOVIMIENTO.tiene_captura              | S                      | BOOLEAN   |

### **Producciones con reglas**

```javascript
S1 → METADATA JUGADAS S2
{
  // Generamos array con todos los elementos de S2.cantidad_capturas agregandole JUGADAS.cantidad_capturas al final
  S1.cantidad_capturas = [...S2.cantidad_capturas, JUGADAS.cantidad_capturas]
  S1.captura_texto = JUGADAS.captura_texto ++ " " ++ S2.captura_texto
  JUGADAS.numero_jugada = 0
}
```
```javascript
S → METADATA JUGADAS
{  
  S.cantidad_capturas = [JUGADAS.cantidad_capturas]
  S.captura_texto = JUGADAS.captura_texto
  JUGADAS.numero_jugada = 0
}
```
```javascript
S1 → JUGADAS S2
{
  S1.cantidad_capturas = [JUGADAS.cantidad_capturas, ...S2.cantidad_capturas]
  S1.captura_texto = JUGADAS.captura_texto
  JUGADAS.numero_jugada = 0
}
```
```javascript
S → JUGADAS
{
  S.cantidad_capturas = [JUGADAS.cantidad_capturas]
  S.captura_texto = JUGADAS.captura_texto
  JUGADAS.numero_jugada = 0
}
```
```javascript
METADATA → ITEM_METADATA METADATA
```
```javascript
METADATA → ITEM_METADATA
```
```javascript
ITEM_METADATA → corchete_abre palabra espacio comilla COMENTARIO_REAL comilla corchete_cierra renglon
```
```javascript
COMENTARIO_REAL →  palabra espacio COMENTARIO_REAL
```
```javascript
COMENTARIO_REAL →  palabra
```
```javascript
JUGADAS1 → JUGADA JUGADAS2
{
  JUGADAS1.cantidad_capturas = JUGADA.cantidad_capturas + JUGADAS2.cantidad_capturas
  JUGADAS1.captura_texto = JUGADA.captura_texto + JUGADAS2.captura_texto
  JUGADA.numero_jugada = JUGADAS1.numero_jugada + 1
  JUGADAS2.numero_jugada = JUGADAS1.numero_jugada + 1
}
```
```javascript
JUGADAS → MOVIMIENTO_FINAL renglon
{
  JUGADAS1.cantidad_capturas = 0
  JUGADAS1.captura_texto = ""
}
```
```javascript
JUGADAS → MOVIMIENTO_FINAL
{
  JUGADAS1.cantidad_capturas = 0
  JUGADAS1.captura_texto = ""
}
```
```javascript
MOVIMIENTO_FINAL → gano_blanco
```
```javascript
MOVIMIENTO_FINAL → gano_negro
```
```javascript
MOVIMIENTO_FINAL → empate
```
```javascript
JUGADA → numero_jugada_blanco MOVIMIENTO J2
{
  CONDITION(int(numero_jugada_blanco.val) == JUGADA.numero_jugada)

  CONDITION(J2.tiene_num && JUGADA.numero_jugada == J2.numero_jugada_negro)

  JUGADA.cantidad_capturas = int(MOVIMIENTO.tiene_captura) + J2.cantidad_capturas

  JUGADA.captura_texto = ""
  JUGADA.captura_texto += IF(MOVIMIENTO.tiene_captura || J2.cantidad_capturas > 0, numero_jugada_blanco.val, "")
  JUGADA.captura_texto += IF(MOVIMIENTO.tiene_captura, " " ++ MOVIMIENTO.captura_texto ++ " " , "")
  JUGADA.captura_texto += IF(J2.cantidad_capturas > 0, " " ++ J2.captura_texto ++ " " , "")
}
```
```javascript
JUGADA → numero_jugada_blanco MOVIMIENTO
{
  CONDITION(int(numero_jugada_blanco.val) == JUGADA.numero_jugada)

  JUGADA.cantidad_capturas = int(MOVIMIENTO.tiene_captura)

  JUGADA.captura_texto = ""
  JUGADA.captura_texto += IF(MOVIMIENTO.tiene_captura, numero_jugada_blanco.val, "")
  JUGADA.captura_texto += IF(MOVIMIENTO.tiene_captura, " " ++ MOVIMIENTO.captura_texto ++ " " , "")
}
```
```javascript
J2 → COMENTARIO1 numero_jugada_negro MOVIMIENTO COMENTARIO2
{
  J2.cantidad_capturas = COMENTARIO1.cantidad_capturas + int(MOVIMIENTO.tiene_captura) + COMENTARIO2.cantidad_capturas
  J2.captura_texto = COMENTARIO1.captura_texto + MOVIMIENTO.captura_texto + COMENTARIO2.captura_texto
  J2.tiene_num = true
  J2.numero_jugada_n = int(numero_jugada_negro)
}
```
```javascript
J2 → COMENTARIO numero_jugada_negro MOVIMIENTO
{
  J2.cantidad_capturas = int(MOVIMIENTO.tiene_captura) + COMENTARIO.cantidad_capturas
  J2.captura_texto = MOVIMIENTO.captura_texto + COMENTARIO.captura_texto
  J2.numero_jugada_negro = int(numero_jugada_negro.val)
  J2.tiene_num = true
}
```
```javascript
J2 → numero_jugada_negro MOVIMIENTO COMENTARIO
{
  J2.cantidad_capturas = int(MOVIMIENTO.tiene_captura) + COMENTARIO.cantidad_capturas
  J2.captura_texto = MOVIMIENTO.captura_texto + COMENTARIO.captura_texto
  J2.tiene_num = true
  J2.numero_jugada_negro = int(numero_jugada_negro.val)
}
```
```javascript
J2 → numero_jugada_negro MOVIMIENTO
{
  J2.cantidad_capturas = int(MOVIMIENTO.tiene_captura)
  J2.captura_texto = MOVIMIENTO.captura_texto
  J2.tiene_num = true
  J2.numero_jugada_negro = int(numero_jugada_negro.val)
}
```
```javascript
J2 → MOVIMIENTO COMENTARIO
{
  J2.cantidad_capturas = int(MOVIMIENTO.tiene_captura) + COMENTARIO.cantidad_capturas
  J2.captura_texto = MOVIMIENTO.captura_texto + COMENTARIO.captura_texto
  J2.tiene_num = false
}
```
```javascript
J2 → COMENTARIO
{
  J2.cantidad_capturas = COMENTARIO.cantidad_capturas
  J2.captura_texto = COMENTARIO.captura_texto
  J2.tiene_num = false
}
```
```javascript
J2 → MOVIMIENTO
{
  J2.cantidad_capturas = int(MOVIMIENTO.tiene_captura)
  J2.captura_texto = MOVIMIENTO.captura_texto
  J2.tiene_num = false
}
```
```javascript
MOVIMIENTO → token_movimiento ESPECIAL
{
  MOVIMIENTO.tiene_captura = IF("x" in token_movimiento.val, true, false)
  MOVIMIENTO.captura_texto = IF("x" in token_movimiento.val, token_movimiento.val, "")
}
```
```javascript
MOVIMIENTO → token_movimiento
{
  MOVIMIENTO.tiene_captura = IF("x" in token_movimiento.val, true, false)
  MOVIMIENTO.captura_texto = IF("x" in token_movimiento.val, token_movimiento.val, "")
}
```
```javascript
ESPECIAL →  jaque_mate
```
```javascript
ESPECIAL → jaque
```
```javascript
COMENTARIO → llave_abre  COM llave_cierra
{
  COMENTARIO.cantidad_capturas = COM.cantidad_capturas
  COMENTARIO.captura_texto = COM.captura_texto
}
```
```javascript
COMENTARIO → parentecis_abre COM parentecis_cierra
{
  COMENTARIO.cantidad_capturas = COM.cantidad_capturas
  COMENTARIO.captura_texto = COM.captura_texto
}
```
```javascript
COMENTARIO → llave_abre llave_cierra
{
  COMENTARIO.cantidad_capturas = 0
  COMENTARIO.captura_texto = ""
}
```
```javascript
COMENTARIO → parentecis_abre parentecis_cierra
{
  COMENTARIO.cantidad_capturas = 0
  COMENTARIO.captura_texto = ""
}
```
```javascript
COM1 → MOVIMIENTO_OPCIONAL COM2
{
  COM1.cantidad_capturas = int(MOVIMIENTO_OPCIONAL.tiene_captura) + COM2.cantidad_capturas
  COM1.captura_texto = MOVIMIENTO_OPCIONAL.captura_texto ++ COM2.captura_texto
}
```
```javascript
COM1 → COMENTARIO COM2
{
  COM1.cantidad_capturas = COMENTARIO.cantidad_capturas + COM2.cantidad_capturas
  COM1.captura_texto = COMENTARIO.captura_texto ++ COM2.captura_texto
}
```
```javascript
COM1 → palabra COM2
{
  COM1.cantidad_capturas = COM2.cantidad_capturas
  COM1.captura_texto = COM2.captura_texto
}
```
```javascript
COM1 → espacio COM2
{
  COM1.cantidad_capturas = COM2.cantidad_capturas
  COM1.captura_texto = COM2.captura_texto
}
```
```javascript
COM → MOVIMIENTO_OPCIONAL
{
  COM.cantidad_capturas = MOVIMIENTO_OPCIONAL.cantidad_capturas
  COM.captura_texto = MOVIMIENTO_OPCIONAL.captura_texto
}
```
```javascript
COM → COMENTARIO
{
  COM.cantidad_capturas = COMENTARIO.cantidad_capturas
  COM.captura_texto = COMENTARIO.captura_texto
}
```
```javascript
COM → palabra
{
  COM.cantidad_capturas = 0
  COM.captura_texto = ""
}
```
```javascript
COM → espacio
{
  COM.cantidad_capturas = 0
  COM.captura_texto = ""
}
```
```javascript
MOVIMIENTO_OPCIONAL  →   token_movimiento
{
  MOVIMIENTO_OPCIONAL.tiene_captura = IF("x" in token_movimiento.val, true, false)
  MOVIMIENTO_OPCIONAL.captura_texto = IF("x" in token_movimiento.val, token_movimiento.val, "")
}
```

## **Desarrollo**

### **Lexer en Python**
TODO

### **Parser en Python**
TODO

### **Ejecuciones de prueba**
TODO

## **Conclusión**
TODO

<!-- 
| hola | aur  | fssf |
| ---- | ---- | ---- |
| chau | fssf | 12   |
-->

<!-- 
S   ->  METADATA JUGADAS S
S   ->  METADATA JUGADAS
S   ->  JUGADAS S
S   ->  JUGADAS

METADATA    ->  ITEM_METADATA METADATA
METADATA    ->  ITEM_METADATA

ITEM_METADATA   ->  corchete_abre palabra espacio comilla COMENTARIO_REAL comilla corchete_cierra renglon

COMENTARIO_REAL ->  palabra espacio COMENTARIO_REAL
COMENTARIO_REAL ->  palabra

JUGADAS ->  JUGADA JUGADAS
JUGADAS ->  MOVIMIENTO_FINAL renglon
JUGADAS ->  MOVIMIENTO_FINAL

MOVIMIENTO_FINAL    ->  gano_blanco
MOVIMIENTO_FINAL    ->  gano_negro
MOVIMIENTO_FINAL    ->  empate

JUGADA  ->  numero_jugada_blanco MOVIMIENTO J2
JUGADA  ->  numero_jugada_blanco MOVIMIENTO

J2  ->  COMENTARIO numero_jugada_negro MOVIMIENTO COMENTARIO
J2  ->  numero_jugada_negro MOVIMIENTO COMENTARIO
J2  ->  numero_jugada_negro MOVIMIENTO
J2  ->  MOVIMIENTO COMENTARIO
J2  ->  COMENTARIO
J2  ->  MOVIMIENTO

MOVIMIENTO  ->  token_movimiento ESPECIAL
MOVIMIENTO  ->  token_movimiento

ESPECIAL    ->  jaque_mate
ESPECIAL    ->  jaque

COMENTARIO  ->  llave_abre  COM llave_cierra
COMENTARIO  ->  parentecis_abre COM parentecis_cierra
COMENTARIO  ->  llave_abre llave_cierra
COMENTARIO  ->  parentecis_abre parentecis_cierra

COM ->  MOVIMIENTO_OPCIONAL COM
COM ->  COMENTARIO COM
COM ->  palabra COM
COM ->  espacio COM
COM ->  MOVIMIENTO_OPCIONAL
COM ->  COMENTARIO
COM ->  palabra
COM ->  espacio
-->

</div>