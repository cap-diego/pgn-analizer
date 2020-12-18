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

<!-- Comencemos describiendo la gramática sin los atributos, esta será una gramática libre de contexto que valide que una cadena pertenezca al lenguaje de los archivos PGN. -->

En esta sección se describen los detalles relacionados a la gramática que utilizamos para reconocer el formato PGN. Durante el desarrollo del TP esta gramática tuvo algunos cambios importantes debido a que las herramientas que utilizamos estaban orientadas crear parsers LR, uno de ellos es que eliminamos todas las producciones lambda ya que causaban conflictos en las tablas.

Las diferentes partes de nuestra gramática son las siguientes:

### **Símbolos Terminales**

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

### **Símbolos No Terminales**

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

             COM → token_movimiento COM
                 | COMENTARIO COM
                 | palabra COM
                 | espacio COM
                 | token_movimiento
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
COM1 → token_movimiento COM2
{
  COM1.cantidad_capturas = IF("x" in token_movimiento.val, 1, 0)) + COM2.cantidad_capturas
  COM1.captura_texto = IF("x" in token_movimiento.val, token_movimiento.val, "") ++ COM2.captura_texto
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
COM → token_movimiento
{
  COM.cantidad_capturas = IF("x" in token_movimiento.val, 1, 0)
  COM.captura_texto = IF("x" in token_movimiento.val, token_movimiento.val, "")
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

## **Desarrollo**

Como mencionamos anteriormente utilizamos PLY y YACC para construir nuestro programa, estas herramientas requerían que programemos un Lexer y un Parser para poder reconocer nuestro lenguaje. Debido a como funcionan esas herramientas el código que parsea las reglas de los atributos no es una copia 1:1 con las escritas anteriormente, esto se explicará mejor en la sección del Parser.

### **Lexer**

Para que un parser pueda reconocer un texto, se tienen que convertir los characteres del texto en **tokens**, estos tokes son los que el parser leerá y mapeará a las producciones de nuestra gramática.

La forma en la que PLY maneja los tokens es mediante **reglas**, éstas corresponden con funciones de python (o strings) que contendrán una expresión regular que indica como reconocer el token junto con código en caso de necesitarlo.

PLY tiene un orden en el cual los tokens son revisados, esto es importante a la hora de definirlos, el orden es el siguiente:

- Los tokens que sean funciones se revisan primero y en el orden de definición
- Los tokens que sean strings se revisan en orden que que tan larga sea la expresión regular que utilizan

La mayoría de las reglas se pueden entender fácilmente al leer sus expresiones regulares y/ó código pero la regla de palabra es más compleja y la explicaremos a continuación:

#### **palabra**

Este token se utiliza cuando se quiere reconocer una palabra cualquiera, es principalmente usado en la metadada y en los comentarios. La expresión regular que reconoce a una palabra es `[^(\s|\"|\]|\[|\{|\})]+` y reconoce a todos los caracteres que no sean ", [, ], {, } o whitespaces. 

Ésta expresión regular es muy ámplia y reconoce a otras combinaciones de caracteres que nos interesa reconocer como otros tokens, incluso al reacomodar las reglas de PLY. Nuestra solución a éste problema fue recalcular el valor como otro token si la palabra reconocida encajaba con alguna de las expresiones regulares que nos interesa separar de la misma.

A la vez si la palabra se encuentra en un comentario algunos valores no son recalculados ya que no importan en ese contexto. Para revisar si un token palabra está en un comentario se utilizan variables que se modifican en los tokens de las llaves y los paréntesis.

### **Parser**

Una vez tokenizado el archivo a leer el parser toma los tokens e intenta reconocer el lenguaje en base a la gramática que definimos. YACC permite escribir funciones que representen las producciones de la gramática y utilizar código para representar las reglas de la misma. Las funciones contienen un comentario al principio que YACC lee para identificar la gramatica, no es necesario que las funciones tengan el mismo nombre que el no terminal de las producciones que representan. 

Los atributos sintetizados son programados mediante el parametro de entrada de las funciones `p`, ésta variable contiene un arreglo que representa a los elementos de la producción, en los no terminales utilizamos diccionarios de python cuyas claves coinciden con los atributos de la gramática y los guardamos en la posición correspondiente, y para los terminales se utiliza su valor directamente (si p[i] es terminal YACC le asigna el string que lo representa y si es un no terminal el calculo que su valor queda en el programador). 

YACC no soporta utilizar el arreglo `p` para calcular atributos heredados, por lo que tuvimos que resolverlo mediante el uso de variables globales. Esto nos permitió calcularlos correctamente pero no se pudo realizar de una forma que sea exactamente igual a como se escribieron en la gramática.

Una vez calculadas las secuencias de los puntajes y capturas se tienen que invertir, ya que son calculadas en orden inverso.

### **Ejecuciones de prueba**

En ésta sección mostraremos los resultados de ejecutar algunos archivos en nuestro programa.

### **Casos válidos**

#### **Archivo**: entrada_valida.txt

Output:

```
Parseando . . . 
Lectura Finalizada 
Cantidad de capturas por partida:  [14, 0] 
Capturas por partida: 
Partida 1: [ 6.Bxg5, 7. hxg5 Qxg5 , 10.Qxg7 Nxd5., 11. exf6 gxf6 , 12. Nxd5., 17.Bxe4 dxe4 Rxe4 , 18. Bxe4 dxe4 , 19. Nxe4 , ] 
Partida 2: [ ] 
Cantidad de capturas totales:  14 
Ganadores:  ['blanco', 'blanco'] 
```

#### **Archivo**: loco.txt

Output:

```
Parseando . . .  
Lectura Finalizada 
Cantidad de capturas por partida:  [67, 11, 7, 0, 12, 2, 1, 27, 5, 6, 10] 
Capturas por partida:  
Partida 1: [ 2. Bhxb6 ,10. Qxh7 , 13. Qxe2 , 14. Rxc3 , 15.Kxa8? B3xg8Nxf3Rxh2 Qxb2Rxd2 Bxh2 Kxd7 Qxg6 Bcxa3 Rxd5+Kxa1 Pxb8 Kxf3 Pxa4 Pxa6Bxh8 Paxg7Nxg3 Bxd1 Ncxf8 Rxd4 Kxb8 Pcxg8Nxc3 Pxe3 Khxe3 Q6xb1 Qxc3 Qxc1 Bxb7 Kxg6Qxg1Qxc4 Qxe3Kxf6 K7xa6 R7xg6 Rxa2 Qxe6 Nxa6 Rxc4Rgxa4 Qxb8Nxf3Nxb4 Qxc8Qxc3+ Pxg8 Nxe6Pxc4 Rxe4 , 22. Kxb3 , 23. Bxa7 , 28. K1xd6 ,32. Bxe3+ Kxc1 ,38.Nxh8 Pxc4Bxf4Kgxh2, 41.Nxc2, 42. Qxb1 ,] 
Partida 2: [1. Kgxb6# Kxh6 Bxd8 Pxf4 P5xg1Kxa4Nxh5B4xe7, 4. Qxa1 Rxd5 Rxe4,] 
Partida 3: [1. Kxf3 ,7. Bxd2 ,9. Qxb6 ,13. Phxb3 , 18. Kxd8 , 19. Pdxc7 , 22. Bexf7 , ] 
Partida 4: [ ] 
Partida 5: [1. Pxd5 ,3. P5xe7 , 16. Nxc4 Bxe1 , 21. Kxd6 , 22. Qxb7 , 25. Bxf4 ,27. Bxc5 , 30. Rxf3 ,32. Rxh8 , 33. Pxe4 ,35. Paxd1 ,] 
Partida 6: [1. Qxe8,3. Kxe7 ,] 
Partida 7: [1. Rxd3 , ] 
Partida 8: [5. Nxh8 , 6. Bxe7 , 7. Pxh7 ,9. Qxg5 ,11. Rxe5 ,17. Q4xb1 , 20. Rxe2 ,22. Kxb5 Pxa2 ,26. Qxg6 , 31. Rxe8 Re1xa3+Bxg2, 32. Khxc7 ,36. Kxf4 Kxe3 Bxb4K4xa2 Pxa1Nxh5 Kxg1 Nxh5Kfxb3,40. Nxa2 , 43. Kxh7 ,45.Bxe1, 52. P1xd2 , ] 
Partida 9: [3. Kxc7 Pxa2 , 6. Bxa5 , 9. Pxe5 ,11. Kxf4 ,] 
Partida 10: [ 2. Rxg5 , 7. Rxg1 ,9.Qxd8 , 10. Bxb5 , 11. Qxd4 ,17.Bxa5 , ] 
Partida 11: [3. Pxh5 ,9. Rxf6 Rxh4Bxg1 Pxa3 Kxc1Bxg8,13. Pxa1 ,15. Bxa3 ,29. Qxd5 , ] 
Cantidad de capturas totales:  148 
Ganadores:  ['blanco', 'blanco', 'blanco', 'empate', 'empate', 'blanco', 'negro', 'empate', 'blanco', 'negro', 'negro'] 
```

### **Casos no válidos**

#### **Archivo**: error_falta_).txt

Output:

```
Parseando . . .
ERROR - Los paréntesis o corchetes de comentarios no están balanceados
```

#### **Archivo**: numero_jugada_incorrecto.txt

Output:

```
Parseando . . .
Número de Jugada invalido: llegó 7 y se esperaba 3
```

#### **Archivo**: jugada_negro_falla.txt

Output:
```
Parseando . . .
ERROR - Número de jugada del jugador negro no coincide con la del blanco, llegó 17 y se esperaba 2
```

## **Conclusión**
Para llegar a un parser funcional tuvimos que hacer un proceso iterativo incremental bastante amplio entre la implementación y la gramática, las limitaciones de la librería no nos permitieron programar la gramática de una forma tan libre como las definimos en clase y tuvimos que reformularla.

A pesar de esto, en relativamente poco tiempo logramos desarrollar un parser de un lenguaje bastante complejo que calculaba todos los datos pedidos, eso demuestra la gran capacidad de los parsers autogenerados, aunque falta mucho desarrollo sobre las herramientas como PLY para que sean realmente útiles en la práctica.

El proyecto quedó con muchas producciones y por lo tanto muy largo debido a la simplificación que tuvimos que hacer para poder utilizar la libería, esto puede generar confusión especialmente en proyectos de mayor embergadura y nos limita mucho. 

</div>