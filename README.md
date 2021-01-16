# Analizador de [PGN/Portable Game Notation](https://en.wikipedia.org/wiki/Portable_Game_Notation)

## Contenidos

1. [Objetivo](#objetivo)

2. [Constraints del problema](#constraints)

3. [Ejemplos](#ejemplos)

4. [Solución](#solucion)

5. [Dependencias](#dependencias)

6. [Ejemplo de corrida](#ejemplocorrida)

7. [TODO](#todo)

### Objetivo <a name="objetivo"></a>
- Verificar la sintaxis de un PNG
 - Contar jugadas de captura
 - Incluyendo las de los comentarios
 - Devolver la secuencia en formato texto

  ### Contrainsts <a name="constraints"></a>
    - Sintaxis png
      - [descriptor de evento]: puede ser nombre, lugar, fecha, nombres jugadores, resultado, etc.
      - Son cadenas entre comillas.
      - Se puede asumir que son cadenas arbitrarias.
      - Las jugadas deben estar en orden creciente y no pueden faltar intermedias.
      - La última jugada contiene el resultado: 1-0 (ganó blanco), 0-1 (ganó negro), ½-½ (empate).
    - Formato de jugada
      - Pieza inicial:  P, N, B, R, Q, K (default: P)
      - Coordenadas casilla actual (columna fila) (opcional ambos)
      - Las capturas se indican con: x.
      - Coordenadas nueva casilla: a1, a2, …, h8. 
      - Enroques: O-O-O, O-O
      - Si la jugada amenaza al rey (jaque) va seguida de +.
      - Si la jugada es jaque mate va seguida de #.
      - número.: significa que la siguiente jugada es del otro jugador
      - número … : si esto precede a la jugada entonces nùmero debe coincidir con el inmediato anterior.
      - Significa que la siguiente jugada es del mismo turno, como que reanuda la descripción de la misma jugada (generalmente después de un comentario)
    - Formato de comentarios
      - Con {} ó ().
      - Pueden estar anidados.
      - Deben estar balanceados.
      - Pueden contener jugadas.

  ### Ejemplos <a name="ejemplos"></a>
  #### Ejemplo jugadas válidas
  - Ndf6: Caballo en columna d mueve a f6
  - exf4: peón en columna e captura pieza en f4.
  - 1. e4 e5 2. Nf3 { Nf3 se considera mala } 2… Nc6 ½-½.

  #### Ejemplo jugadas no válidas
  - 1. e4 e4 3. e5 e5 4. e4 0-1: No es válido porque falta movimiento 2
  - 1. e4 e5 { Nf3 1-0: No es válido porque la llave no está balanceada.


### Solución: Gramática de atributos <a name="solucion"></a>
 <details><summary>Ver más</summary>
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

</details>

### **Casos no válidos**
<details><summary>Ver más</summary>  

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
</details>


### Dependencias <a name="dependencias"></a>
 - python3
 - ply (versión 3.11)
### Ejemplo corrida <a name="ejemplocorrida"></a>
- Situados en el directorio principal:
  - ```python 
     python parser/parser.py parser/entrada_valida.txt
   ```

 ### Todo: <a name="todo"></a>
  - Agregar al readme las reglas para cada producción
  - Corrección bugs
  - [1. e4 e5 2. Nc3 3. Nc6 1-0]: Es admitida cuando no debería serlo
  - Errores en algunas lista de jugadas retornadas. entrada_valida.txt retorna: [... 12. Nxd5., 17. **Bxe4** dxe4 Rxe4 , 18. Bxe4 dxe4 , 19. Nxe4 ...] y Bxe4 es una jugada correspondiente a la #18 y no #17.
      - Posible error: bug en la expresión regular que detecta jugadas
