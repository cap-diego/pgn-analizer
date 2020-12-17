<div style="text-align: justify">

# Trabajo práctico Teoría de Lenguajes

## Integrantes
- Tasat, Dylan - 29/17 - dylantasat11@gmail.com 
- Springhart, Gonzalo Leandro - 308/17 - glspringhart@gmail.com 
- Buceta, Diego - 001/17 - diegobuceta35@gmail.com

## Introducción
Para este trabajo vamos a generar una gramática de atributos que decodifique los archivos PGN.

Estos archivos representan partidas de ajedrez mediante una sintaxis bastante flexible, permiten describir situaciones muy complejas, permitiendo comentarios de los distintos jugadores y abreviaturas para las jugadas más comunes.

Generaremos una gramática que verifique que el archivo sea una cadena válida del lenguaje, luego agregaremos a sus producciones una serie de atributos que nos permitan conocer los datos necesarios, estos son:
- Mostrar la cantidad de jugadas de captura mencionadas a lo largo de cada partida.
  - Incluyendo las de los comentarios.
- Mostrar las jugadas de captura mencionadas a lo largo de cada partida.
- Validar que la numeración de las jugadas sea correcta para todas las partidas.
  - Tienen que comenzar por 1.
  - Tienen que avanzar de forma ascendente.
  - Si una jugada del blanco va antecedida de número y punto, la siguiente, del negro, no deberá tener número ni puntos o bien podrá tener el mismo número que la última del blanco seguido de tres puntos.

Luego utilizaremos la herramienta PLY y YACC que es una combinación de extensiones para Python que nos permiten especificar una gramática y te genera un parser automáticamente.
Haciendo uso de esto, implementaremos nuestra gramática para generar un parser y evaluar los distintos ejemplos de archivos provistos por la cátedra más algunos que encontramos nosotros durante el proceso de investigación.

## Gramática
Comencemos describiendo la gramática sin los atributos, esta será una gramática libre de contexto que valide que una cadena pertenezca al lenguaje de los archivos PGN.
Tenemos las siguientes producciones:

```
S → METADATA JUGADAS
METADATA → ITEM_METADATA METADATA | λ
```

### Terminales

### No Terminales

### Producciones

## Atributos
TODO

## Parser en Python
TODO

## Conclusión
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
-->

</div>