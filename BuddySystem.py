from __future__ import annotations
from math import *
from operator import contains
from typing import Dict, List, Tuple

if (__name__ == "__main__"):
    print("No deberias estar aca! Shuuuu")
    quit()

class BuddyAllocator:
    """
    Clase que implementa un manejador de memoria basado en el buddy system.
    La principal forma de interaccion es mediante los metodos:
        -show_state
        -reserve_name
        _free_name

    Mantiene una tabla de simbolos que asocia un nombre a un bloque asignado y 
    una tabla que asocia un tamano (en forma de exponente de una potencia de dos)
    de bloque a una lista a mantener.
    """

    def __init__(self : BuddyAllocator, size : int) -> None:
        self.symbols : Dict[str, BuddyBlock] = {}
        self.freeList : Dict[int, List[BuddyBlock]] = {}
        self.roots : List[BuddyBlock] = []
        self.initialize_free_list(size)

    

    def initialize_free_list(self : BuddyAllocator, size : int) -> None:
        """
        Inicializa las listas libres para una memoria de tamano size.
        Si el tamano no es potencia de dos, se divide en multiples potencias de dos.

        Argumentos:
            size -- Tamano de la memoria total
        """

        currentSize : int = size
        sizes : List[int] = []

        while (currentSize > 0):
            blockExp, blockSize = self.closest_lower_two_power(currentSize)
            currentSize -= blockSize
            sizes.append(blockExp)

            rootBlock : BuddyBlock = BuddyBlock(None, blockExp)
            self.freeList[blockExp] = [rootBlock]
            self.roots.append(rootBlock)

        biggestValue : int = max(sizes)
        for i in range(0, biggestValue + 1):
            if (contains(self.freeList, i)):
                continue

            self.freeList[i] = []


    def show_inorder(self : BuddyAllocator) -> None:
        """
        Inicia un recorrido in-order en las raices de los arboles formados
        por los bloques iniciales de memoria del buddy system.
        """

        print("-"*30)
        print("Memory in order:\n")
        for b in self.roots:
            self.print_inorder(b)
        print("\n")
        print("-" * 30)


    def print_inorder(self : BuddyAllocator, root : BuddyBlock) -> None:
        """
        Recorre in-order desde un bloque del arbol formado por el buddy system e
        imprime la informacion de los bloques libres y los bloques usados.

        Argumentos:
            root -- Bloque a recorrer in-order
        """

        if (root.lc != None):
            self.print_inorder(root.lc)
            self.print_inorder(root.rc)
        
        if (root.used):
            print("|name %s, name size %i, block size %i|"%(root.name, root.nameSize, 2**root.blockSize), end = " ")
        elif (not root.splitted):
            print("|free, block size %i|"%(2**root.blockSize), end = " ")
            

    def show_state(self : BuddyAllocator) -> None:
        """
        Muestra el estado de la memoria del buddy system en forma de 
        una tabla de nombres asignados, los bloques libres en cada lista y 
        una representacion de la memoria.
        """

        for key in sorted(self.freeList.keys()):
            print("-"*30)
            print("Lista libre de bloques con tamano %i:" %(2**key))
            
            lista : List[BuddyBlock] = self.freeList[key]
            if (len(lista) == 0):
                print("No hay bloques libres en la lista.")
                continue
            
            print("Tiene %i bloques libres" %(len(lista)))
            print("-"*30)

        print("-"*30)
        print("Nombres asignados")
        for (key, item) in self.symbols.items():
            print("Nombre %s asignado a bloque de tamano %i" %(key, 2**item.blockSize)) 
        print("-"*30)
        self.show_inorder()


    
    def look_create_block_in_list(self : BuddyAllocator, name : str, blockSize : int, nameSize : int) -> Tuple[bool, BuddyBlock]:
        """
        Busca el primer bloque libre en una lista de tamano 2^blockSize y se lo asigna a
        un nombre.
        
        Argumentos:
            name -- Nombre a asignar bloque
            blockSize -- Potencia de dos del tamano del bloque a buscar
            nameSize -- Cantidad a reservar para el nombre

        Returns:
            Una tupla (bool, BuddyBlock) cuyo primer elemento es si se encontro exitosamente 
            un bloque en la lista y el segundo elemento es el bloque encontrado (None si no se encontro)
        """

        assert contains(self.freeList, blockSize)
        targetList : List[BuddyBlock] = self.freeList[blockSize]

        targetBlock : BuddyBlock = targetList.pop(0)
        targetBlock.assign_name(name, nameSize)
        
        assert not contains(self.symbols, name), "No se puede asignar mas de un bloque por nombre."
        self.symbols[name] = targetBlock

        return (True, targetBlock)
        

    def look_create_block(self : BuddyAllocator, name : str, size : int) -> Tuple[bool, BuddyBlock]:
        """
        Busca o crea un bloque para un nombre de tamano size.
        
        Argumentos:
            name -- Nombre a buscar bloque
            size -- Cantidad a reservar

        Returns:
            Una tupla (bool, BuddyBlock) cuyo primer elemento es si se encontro exitosamente 
            un bloque en la lista y el segundo elemento es el bloque encontrado (None si no se encontro)
        """

        closestExp : int = self.closest_higher_two_power(size)[0]
        if (not contains(self.freeList, closestExp)):
            print("La cantidad de memoria solicitada es mayor a los bloques mas grandes de la memoria.")
            return (False, None)

        if (len(self.freeList[closestExp]) > 0):
          # Buscamos primero en la lista de su tamano
          found, blockFound = self.look_create_block_in_list(name, closestExp, size)
          if (found):
              return (True, blockFound)

        # Buscamos en las demas listas. NOTA: Sorted lo ordena de menor a mayor.
        for key in sorted(self.freeList.keys()):
            targetList : List[BuddyBlock] = self.freeList[key]
            if (key < closestExp or len(targetList) == 0):
                continue
            
            # Ahora debemos splittear un bloque de lista hasta conseguir el nivel que queremos.
            toSplit : BuddyBlock = targetList.pop(0)
            freeL, freeR = toSplit.split()

            self.freeList[freeR.blockSize].append(freeR)

            while (freeL.blockSize != closestExp):
                freeL, freeR = freeL.split()
                self.freeList[freeR.blockSize].append(freeR)

            assert not contains(self.symbols, name), "No se puede asignar mas de un bloque por nombre."
            freeL.assign_name(name, size)
            self.symbols[name] = freeL
            return (True, freeL)

        return (False, None)


    def reserve_name(self : BuddyAllocator, name : str, size : int) -> Tuple[bool, BuddyBlock]:
        """
        Intenta reservar un bloque de memoria en el buddy system para un nombre.

        Argumentos:
            name -- Nombre al cual se le reservara un bloque
            size -- Cantidad a reservar

        Returns:
            Una tupla (bool, BuddyBlock) cuyo primer elemento es si se encontro exitosamente 
            un bloque en la lista y el segundo elemento es el bloque encontrado (None si no se encontro)
        """

        if (size <= 0):
            print("La memoria a pedir debe ser mayor a 0.")
            return False

        if (contains(self.symbols, name)):
            print("El nombre %s ya contiene espacio reservado en la memoria." %(name))
            return False
        
        found, blockFound = self.look_create_block(name, size)
        if (not found):
            print("No se pudo conseguir un espacio de memoria suficiente para %s." %(name))
            return False

        print("Reservado bloque para %s." %(name))
        return True


    def free_name(self : BuddyAllocator, name : str) -> bool:
        """
        Libera la memoria/bloque asociada a un nombre y combina los bloques en las listas
        de acuerdo a como sea necesario.

        Argumentos:
            name -- Nombre a liberar su memoria

        Returns:
            False si el nombre no existe/no tiene memoria reservada.
            True en otro caso.
        """

        if (not contains(self.symbols, name)):
            print("ERROR: El nombre %s no tiene memoria reservada." %(name))
            return False    
        
        toFree : BuddyBlock = self.symbols.pop(name)
        toFree.free_name()
        self.freeList[toFree.blockSize].append(toFree)

        parent : BuddyBlock = toFree.parent
        while (parent != None and parent.can_be_merged()):
            self.freeList[parent.lc.blockSize].remove(parent.lc)
            self.freeList[parent.rc.blockSize].remove(parent.rc)

            parent.merge_childs()

            self.freeList[parent.blockSize].append(parent)
            parent = parent.parent
        
        print("Se libero el nombre %s de la memoria." %(name))
        return True
                

    def closest_higher_two_power(self : BuddyAllocator, number : int) -> Tuple[int, int]:
        """
        Auxiliar. Devuelve la potencia de dos mas cercana a un numero igual o mayor a este.

        Argumentos:
            number -- Numero a buscar la potencia.

        Returns:
            Una tupla de la forma (int, int) cuyo primer elemento es el exponente y el segundo 
            es 2 elevado al exponente
        """

        closestExp : int = ceil(log2(number))
        return (closestExp, 2**closestExp)


    def closest_lower_two_power(self : BuddyAllocator, number : int) -> Tuple[int, int]:
        """
        Auxiliar. Devuelve la potencia de dos mas cercana a un numero igual o menor a este.

        Argumentos:
            number -- Numero a buscar la potencia.

        Returns:
            Una tupla de la forma (int, int) cuyo primer elemento es el exponente y el segundo 
            es 2 elevado al exponente
        """

        closestExp : int = ceil(log2(number))

        while (2**closestExp > number):
            closestExp -= 1
        
        return (closestExp, 2**closestExp)



class BuddyBlock:
    """
    Clase representativa de un bloque en el buddy system. Contiene como informacion:
        -El bloque del cual proviene (en caso de ser producto de dividir en dos un bloque)
        -El tamano del bloque (representado como el exponente de una potencia de 2)
        -El tamano que reservo el nombre
        -Indicadores de si esta siendo usado o no
        -El nombre que reservo el bloque (si este esta reservado)
        -Los bloques resultantes de ser divido (si este fue dividido)
    """

    def __init__(self : BuddyBlock, parent : BuddyBlock, blockSize : int) -> None:
        self.parent : BuddyBlock = parent
        self.blockSize : int = blockSize
        self.nameSize : int = 0
        self.used : bool = False
        self.splitted : bool = False

        self.name : str = None
        self.lc : BuddyBlock = None
        self.rc : BuddyBlock = None
    

    def assign_name(self : BuddyBlock, name : str, nameSize : int) -> None:
        """
        Asigna/asocia un nombre al bloque.

        Argumentos:
            name -- Nombre al que se le asigna el bloque
            nameSize -- El tamano que reservo el nombre
        """

        #assert not (self.used or self.rc != None or self.lc != None), "No se puede asignar un nombre a un bloque ya usado o con hijos."
        self.name = name
        self.nameSize = nameSize
        self.used = True

    
    def free_name(self : BuddyBlock) -> None:
        """
        Libera el bloque del nombre al que se le asigno.
        """

        assert self.used and self.lc == None and self.rc == None, "No se puede liberar un bloque no usado o con hijos."
        self.name = None
        self.used = False

    
    def split(self : BuddyBlock) -> Tuple[BuddyBlock, BuddyBlock]:
        """
        Divide el bloque en dos.

        Returns:
            Una tupla que contiene los dos bloques resultantes de la division, siendo el primer elemento
            el bloque izquierdo y el segundo el derecho
        """

        assert not self.splitted, "No se puede dividir un bloque ya dividido."
        self.lc, self.rc = BuddyBlock(self, self.blockSize - 1), BuddyBlock(self, self.blockSize - 1)
        self.splitted = True
        return (self.lc, self.rc)
    

    def can_be_merged(self : BuddyBlock) -> bool:
        """
        Calcula si los hijos del bloque pueden ser mergeado de vuelta
        en el bloque padre

        Returns:
            True si se cumple la condicion/False en caso contrario.
        """

        return (self.lc != None and self.rc != None) and not (self.lc.used or self.rc.used) \
            and not (self.lc.splitted or self.rc.splitted) and not self.used and self.splitted
    

    def merge_childs(self : BuddyBlock) -> None:
        """
        Mergea los hijos del bloque en caso de que haya sido dividido.
        """

        assert self.can_be_merged(), "No se puede mergear un bloque padre con hijos en uso o sin hijos."
        del self.lc
        del self.rc
        self.lc, self.rc = None, None
        self.splitted = False