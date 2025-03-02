# Notas de Arquitectura de Computadoras

## 23/01/2025

### Speedup
La mejora en el rendimiento se calcula como:
\[ \text{Speedup} = \frac{\text{Performance after improvement}}{\text{Performance before improvement}} \]
\[ = \frac{\text{Execution time before}}{\text{Execution time after}} \]

El tiempo de ejecución después de la mejora se calcula como:
\[ \text{Execution time after improvement} = \frac{\text{Execution time affected by improvement}}{\text{Amount of improvement}} \]

### Modelo de von Neumann
- La arquitectura de von Neumann tiene un único bus para la CPU y la memoria.
- En un ciclo solo se puede transferir una instrucción o un dato.
- **Solución**: usar memorias separadas para datos e instrucciones.

Ciclo de instrucción:
1. Cargar el programa en lenguaje máquina.
2. Inicializar el PC y SF.
3. Fetch instruction.
4. Incrementar PC.
5. Ejecutar instrucción.
6. Repetir el ciclo.

## 24/01/2025

### Conjunto de Instrucciones
- Cada instrucción es directamente ejecutada por el hardware.
- Se representa en binario, ya que el hardware solo entiende bits.

### MIPS
- Lenguaje ensamblador sencillo y fácil de aprender.
- Principio de regularidad.
- Clases de instrucciones:
  - **Aritméticas**: suma, resta, multiplicación, división.
  - **Transferencia de datos**: carga (load) y almacenamiento (store).
  - **Lógicas**: AND, OR.
  - **Saltos condicionales e incondicionales**.

#### Registros
- Memoria integrada en la CPU con poca capacidad (4 bytes).
- En la mayoría de las CPUs modernas, los datos se mueven a registros antes de operar y luego se almacenan en memoria (**arquitectura load/store**).

## 28/01/2025

### Uso de la Memoria en MIPS
- **Segmento de texto**: Código del programa, comienza en 0x400000.
- **Segmento de datos**: Comienza en 0x10010000, contiene:
  - Datos estáticos.
  - Datos dinámicos.
- **Segmento de pila**: Dirección 0x7FFFFFC.

#### Transferencia de Datos en MIPS
- `lw` (load word): Carga una palabra (4 bytes) de memoria a un registro.
- `sw` (store word): Almacena el valor de un registro en memoria.

Ejemplo:
```assembly
lw $r0, C($r1)  # $r0 <- Mem[$r1 + C]
```

#### Variables en MIPS
Ejemplo de declaración:
```assembly
.data
x: .word 17
```

Código MIPS:
```assembly
.text
addi $t0, $zero, 0x20  # $t0 = 32
addi $t1, $zero, 22
add $t2, $t0, $t1
sub $t3, $t1, $t0
mult $t0, $t1
div $t0, $t1

# Copiar el valor de x
t la $s0, x
lw $t4, 0($s0)

# Método 2
lw $t5, x
```

## 29/01/2025

### Ejemplo en MIPS
Escribir un programa en MIPS para el siguiente código en C:
```c
int a = 25;
int b = 17;
int c = a + b;
```
Código en MIPS:
```assembly
.data
a: .word 25
b: .word 17
c: .word -1

.text
la $t0, a
lw $t1, 0($t0)

lw $t2, b
add $t3, $t1, $t2
sw $t3, c
```

### Ejemplo: Cálculo en MIPS
Código en C:
```c
f = (g + h) - (i + j);
```
Código en MIPS:
```assembly
.data
g: .word 10
h: .word 20
i: .word 5
j: .word 15
f: .word 0

.text
.globl main
main:
    # Cargar valores de g, h, i, j desde la memoria
    lw $t0, g  # t0 = g
    lw $t1, h  # t1 = h
    lw $t2, i  # t2 = i
    lw $t3, j  # t3 = j

    # Calcular (g + h)
    add $t4, $t0, $t1

    # Calcular (i + j)
    add $t5, $t2, $t3

    # Calcular (g + h) - (i + j)
    sub $t6, $t4, $t5

    # Almacenar el resultado en f
    sw $t6, f
```
