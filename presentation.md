---
marp: true
theme: default
paginate: true
---

# Algoritmos de Ordenamiento y Recursión: Merge Sort y Pila de Llamadas

---

# Introducción a Merge Sort

- Merge Sort es un algoritmo eficiente basado en la estrategia de 'divide y vencerás'.
- Consideremos un arreglo de ejemplo: [4, 3, 1, 2, 5, 3].
- Opera dividiendo el arreglo a la mitad hasta alcanzar un caso base, luego combinando las partes ordenadas.
- Es ampliamente utilizado por su estabilidad y su complejidad temporal de O(N log N).

---

# El Algoritmo Merge Sort: Pseudocódigo

- La función `MergeSort(A)` inicia el proceso de ordenamiento recursivo.
- El caso base se define cuando el tamaño del arreglo es uno: `if A.size == 1 return A`.
- Si no es el caso base, se divide `A` en dos subarreglos: `A_left` y `A_right`.
- Se realizan llamadas recursivas a `MergeSort(A_left)` y `MergeSort(A_right)` para ordenar cada mitad.

---

# El Algoritmo Merge Sort: Proceso de Fusión (Merge)

- Tras la ordenación recursiva, la función `Merge(A_left, A_right)` combina los subarreglos.
- Compara elementos de ambos subarreglos y los coloca de forma ordenada en un nuevo arreglo.
- Este paso es crucial para ensamblar las soluciones de los subproblemas en una solución final ordenada.
- El proceso continúa ascendiendo en la jerarquía de llamadas hasta que el arreglo completo está ordenado.

---

# Ejemplo Visual de Merge Sort

- Observemos la representación visual del algoritmo Merge Sort con un arreglo de ejemplo.
- El arreglo inicial se divide repetidamente hasta obtener subarreglos de un solo elemento.
- Posteriormente, estos subarreglos se fusionan de forma ordenada en niveles ascendentes.
- Este diagrama ilustra la estrategia de 'divide y vencerás' en acción.

---

# La Pila de Llamadas (Call Stack)

- La pila de llamadas es una estructura de datos LIFO (Last-In, First-Out) crucial en la ejecución de programas.
- Cada vez que se invoca una función, se 'empuja' (push) un nuevo marco de pila con su contexto.
- Al finalizar una función, su marco de pila se 'desapila' (pop), liberando los recursos asociados.
- Es fundamental para gestionar el flujo de ejecución y las variables locales de las funciones.

---

# Fundamentos de la Recursión

- La recursión es una técnica donde una función se llama a sí misma para resolver un problema.
- Es imperativo definir un 'caso base' que detenga la recursión para evitar bucles infinitos.
- Las funciones recursivas a menudo simplifican la lógica para problemas complejos y repetitivos.
- Permiten abordar problemas dividiéndolos en instancias más pequeñas del mismo problema.

---

# Ejemplo de Recursión No de Cola: fun S1(x)

- Analicemos la función `fun S1(x)` que retorna `2 * S1(x)`.
- Esta es una recursión no de cola (non-tail recursion) porque la llamada recursiva no es la última operación.
- Se debe esperar el valor de retorno de `S1(x)` para multiplicarlo por 2.
- Esto implica que los marcos de pila se acumulan hasta que todas las llamadas retornan.

---

# Ejemplo de Recursión de Cola: fun rec(x)

- Consideremos la función `fun rec(x)` que retorna `rec(x*2)` con un caso base `if x > 150 return x`.
- Esta es una recursión de cola (tail recursion) ya que la llamada recursiva es la última acción en la función.
- No se realizan operaciones adicionales después de la llamada recursiva.
- Los compiladores pueden optimizar la recursión de cola, transformándola en un bucle iterativo para ahorrar espacio en la pila.

---

# Seguimiento de la Pila de Llamadas en Recursión

- El diagrama ilustra el seguimiento de la pila para una llamada como `rec(10)`.
- Cada invocación de `rec(x)` (`rec(10)`, `rec(20)`, `rec(40)`, `rec(80)`) apila un nuevo marco.
- Al alcanzar el caso base (`x > 150`, que ocurre con `rec(160)`), la recursión finaliza.
- Los valores se desapilan secuencialmente hasta retornar el resultado final.
