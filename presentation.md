---
marp: true
theme: default
paginate: true
---

# Algoritmos de Ordenamiento y Recursi�n: Merge Sort y Pila de Llamadas

---

# Introducci�n a Merge Sort

- Merge Sort es un algoritmo eficiente basado en la estrategia de 'divide y vencer�s'.
- Consideremos un arreglo de ejemplo: [4, 3, 1, 2, 5, 3].
- Opera dividiendo el arreglo a la mitad hasta alcanzar un caso base, luego combinando las partes ordenadas.
- Es ampliamente utilizado por su estabilidad y su complejidad temporal de O(N log N).

---

# El Algoritmo Merge Sort: Pseudoc�digo

- La funci�n `MergeSort(A)` inicia el proceso de ordenamiento recursivo.
- El caso base se define cuando el tama�o del arreglo es uno: `if A.size == 1 return A`.
- Si no es el caso base, se divide `A` en dos subarreglos: `A_left` y `A_right`.
- Se realizan llamadas recursivas a `MergeSort(A_left)` y `MergeSort(A_right)` para ordenar cada mitad.

---

# El Algoritmo Merge Sort: Proceso de Fusi�n (Merge)

- Tras la ordenaci�n recursiva, la funci�n `Merge(A_left, A_right)` combina los subarreglos.
- Compara elementos de ambos subarreglos y los coloca de forma ordenada en un nuevo arreglo.
- Este paso es crucial para ensamblar las soluciones de los subproblemas en una soluci�n final ordenada.
- El proceso contin�a ascendiendo en la jerarqu�a de llamadas hasta que el arreglo completo est� ordenado.

---

# Ejemplo Visual de Merge Sort

- Observemos la representaci�n visual del algoritmo Merge Sort con un arreglo de ejemplo.
- El arreglo inicial se divide repetidamente hasta obtener subarreglos de un solo elemento.
- Posteriormente, estos subarreglos se fusionan de forma ordenada en niveles ascendentes.
- Este diagrama ilustra la estrategia de 'divide y vencer�s' en acci�n.

---

# La Pila de Llamadas (Call Stack)

- La pila de llamadas es una estructura de datos LIFO (Last-In, First-Out) crucial en la ejecuci�n de programas.
- Cada vez que se invoca una funci�n, se 'empuja' (push) un nuevo marco de pila con su contexto.
- Al finalizar una funci�n, su marco de pila se 'desapila' (pop), liberando los recursos asociados.
- Es fundamental para gestionar el flujo de ejecuci�n y las variables locales de las funciones.

---

# Fundamentos de la Recursi�n

- La recursi�n es una t�cnica donde una funci�n se llama a s� misma para resolver un problema.
- Es imperativo definir un 'caso base' que detenga la recursi�n para evitar bucles infinitos.
- Las funciones recursivas a menudo simplifican la l�gica para problemas complejos y repetitivos.
- Permiten abordar problemas dividi�ndolos en instancias m�s peque�as del mismo problema.

---

# Ejemplo de Recursi�n No de Cola: fun S1(x)

- Analicemos la funci�n `fun S1(x)` que retorna `2 * S1(x)`.
- Esta es una recursi�n no de cola (non-tail recursion) porque la llamada recursiva no es la �ltima operaci�n.
- Se debe esperar el valor de retorno de `S1(x)` para multiplicarlo por 2.
- Esto implica que los marcos de pila se acumulan hasta que todas las llamadas retornan.

---

# Ejemplo de Recursi�n de Cola: fun rec(x)

- Consideremos la funci�n `fun rec(x)` que retorna `rec(x*2)` con un caso base `if x > 150 return x`.
- Esta es una recursi�n de cola (tail recursion) ya que la llamada recursiva es la �ltima acci�n en la funci�n.
- No se realizan operaciones adicionales despu�s de la llamada recursiva.
- Los compiladores pueden optimizar la recursi�n de cola, transform�ndola en un bucle iterativo para ahorrar espacio en la pila.

---

# Seguimiento de la Pila de Llamadas en Recursi�n

- El diagrama ilustra el seguimiento de la pila para una llamada como `rec(10)`.
- Cada invocaci�n de `rec(x)` (`rec(10)`, `rec(20)`, `rec(40)`, `rec(80)`) apila un nuevo marco.
- Al alcanzar el caso base (`x > 150`, que ocurre con `rec(160)`), la recursi�n finaliza.
- Los valores se desapilan secuencialmente hasta retornar el resultado final.
