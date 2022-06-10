from random import randint
import unittest
from BuddySystem import *


class BuddyAllocationTests(unittest.TestCase):

    def test_bad_sized_reserves(self):
        """
        Prueba que no se pueda reservar valores incorrectos de memoria.
        """

        a : BuddyAllocator = BuddyAllocator(512)
        self.assertFalse(a.reserve_name("a", 0))
        self.assertFalse(a.reserve_name("a", -1))

        for b in a.roots:
            self.assertFalse(a.reserve_name("a", 2**b.blockSize + 1))
    

    def test_initial_blocks(self):
        """
        Prueba la creacion inicial de bloques libres en la memoria.

        Deberia crear uno solo si el tamano es una potencia de dos.
        
        Deberia crear mas de uno si el tamano no es potencia de dos, 
        descomponiendo la memoria en bloques con tamanos resultado de 
        la descomposicion en potencias de dos.
        """

        a : BuddyAllocator = BuddyAllocator(512)

        self.assertTrue(len(a.roots) == 1 and len(a.freeList[9]) == 1 and \
                len(a.freeList.keys()) == 10)

        b : BuddyAllocator = BuddyAllocator(515)
        self.assertTrue(len(b.roots) == 3 and len(b.freeList[9]) == 1 and \
                len(b.freeList[1]) == 1 and len(b.freeList[0]) == 1  and \
                len(b.freeList.keys()) == 10)


    def test_symbol_table_entry(self):
        """
        Prueba que se cree correctamente la entrada de un nombre en la tabla de simbolos y
        se le asocie un bloque.
        """

        a : BuddyAllocator = BuddyAllocator(16) 
        for i in range(0, 16):
            name : str = str(i)
            a.reserve_name(str(i), 1)
            self.assertTrue(contains(a.symbols, name) and a.symbols[name] != None \
                    and a.symbols[name].name == name)
        
        for i in range(0, 16):
            self.assertFalse(a.reserve_name(str(i), 1))

        for i in range(0, 16):
            name : str = str(i)
            a.free_name(name)
            self.assertFalse(contains(a.symbols, name))

    
    def test_minimal_split_and_merge(self):
        """
        Prueba la division de la memoria en sus bloques mas pequenos (2^0) y
        que el resultado de liberar toda la memoria resulta en el bloque original (2^4)
        """

        a : BuddyAllocator = BuddyAllocator(16) 
        for i in range(0, 16):
            self.assertTrue(a.reserve_name(str(i), 1))
            if (i % 2 == 0):
                # No deberia haber bloques libres en la lista 2^0, ya que los casos impares los consumen o
                # es la primera reserva. Se hace split de un bloque mayor hasta 2^0, se consume uno y el otro
                # pasa a la lista libre de 2^0 
                self.assertTrue(len(a.freeList[0]) == 1)
            else:
                # Se consume el bloque libre que hay en la lista 2^0 en vez de hacer split.
                self.assertTrue(len(a.freeList[0]) == 0)
        
        for i in range(0, 16):
            self.assertTrue(a.free_name(str(i)))
        
        self.assertTrue(not a.roots[0].splitted and not a.roots[0].used)
    

    def test_show(self):
        """
        Simplemente espera que el programa no tire una excepcion cuando se pide
        el estado de la memoria
        """

        a : BuddyAllocator = BuddyAllocator(16)
        a.reserve_name("a", 1)
        a.show_state()


if __name__ == '__main__':
    unittest.main()