# CI-3641-Buddy
## Información
Implementación de un simulador de buddy system para CI-3641 hecho en Python 3.10.5.

## Uso del programa
### Ejecución del simulador
Para ejecutar el simulador, ejecuta con python 3 el archivo **BuddySimulator.py**. Este toma como argumento la cantidad de 
bloques de memoria que manejará el simulador.

### Comandos

- **RESERVAR \[NOMBRE\] \[CANTIDAD\]**
  - **NOMBRE:** Nombre al cual se le asigna memoria.
  - **CANTIDAD:** Cantidad de espacio a reservar
 
- **LIBERAR \[NOMBRE\]**
  - **NOMBRE:** Nombre a liberar de la memoria.
 
- **MOSTRAR:** Muestra  el estado de la memoria, las listas de bloques libres e información sobre los nombres asignados y sus bloques.

- **SALIR:** Se cierra el simulador.

## Unit Testing
### Requisitos de las pruebas
- Librería **unittest** para el unit testing.
- Librería **coverage** para el code coverage.

### Ejecución de las pruebas
Para ejecutar unicamente las pruebas, ejecute sobre el archivo **allocation_tests.py** el siguiente comando:

		py -m unittest allocation_tests.py
    
Para ejecutar el code coverage, priemro ejecute sobre el archivo **allocation_tests.py** los siguientes comandos:

		coverage run -m unittest allocation_tests.py
		coverage report

## De interés
- [Code Coverage](https://coverage.readthedocs.io/en/6.4.1/#:~:text=Coverage.py%20is%20a%20tool,gauge%20the%20effectiveness%20of%20tests. "Code Coverage")
- [unittest](https://docs.python.org/3/library/unittest.html "unittest")
