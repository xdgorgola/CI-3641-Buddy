import sys
from typing import List
from BuddySystem import *

"""
Constantes comandos validos.
"""
TOKEN_RESERVAR = "RESERVAR"
TOKEN_LIBERAR = "LIBERAR"
TOKEN_MOSTAR = "MOSTRAR"
TOKEN_SALIR = "SALIR"


def cmd_usage():
    print("Uso incorrecto. Faltan parametros.")
    print("Uso:\n\tBuddySimulator.py [TAMANO]\n\t-TAMANO : Cantidad de bloques que contiene la memoria.")


def simulator_usage():
    print("Uso:\n\tRESERVAR [NOMBRE] [TAMANO]")
    print("\tReserva TAMANO memoria para NOMBRE")
    print("\t-NOMBRE : Nombre al que se le reservara espacio.")
    print("\t-TAMANO : Tamano a reservar para NOMBRE.")
    print("\n\tLIBERAR [NOMBRE]\n\tLibera la memoria asociada a NOMBRE")
    print("\t-NOMBRE : Nombre a liberar su espacio")
    print("\n\tMOSTRAR\n\tMuestra el estado del buddy system")
    print("\n\tSALIR\n\tMata\\sale del programa.")


if (len(sys.argv) != 2):
    cmd_usage()
    quit()

if (not sys.argv[1].isnumeric()):
    print("La cantidad de bloques de la memoria debe ser un numero!")
    cmd_usage()
    quit()

if (int(sys.argv[1]) <= 0):
    print("Por favor, introduzca un numero positivo/distinto a 0!")
    quit()


a : BuddyAllocator = BuddyAllocator(int(sys.argv[1]))
run : bool = True


while (run):
    tokens : List[str] = input("Introduce un comando>").split()
    if (len(tokens) == 0):
        print("Comando no valido.")
        continue

    comando : str = tokens[0].upper()
    
    if (comando == TOKEN_RESERVAR):
        if (len(tokens) != 3):
            simulator_usage()
            continue
        if (not tokens[2].isnumeric()):
            print("El tamano a reservar debe ser un numero.")
            continue

        tamano : int = int(tokens[2])
        if (tamano <= 0):
            print("El tamano a reservar debe ser mayor a 0")
            continue

        a.reserve_name(tokens[1], int(tokens[2]))
    elif (comando == TOKEN_LIBERAR):
        
        if (len(tokens) != 2):
            simulator_usage()
            continue

        a.free_name(tokens[1])
    elif (comando == TOKEN_MOSTAR):
        a.show_state()
    elif (comando == TOKEN_SALIR):
        run = False
    else:
        simulator_usage()

print("Has matado mi programa :(!")