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
            self.assertFalse(a.free_name(name))

    
    def test_minimal_split_and_merge(self):
        """
        Prueba la division de la memoria en sus bloques mas pequenos (2^0) y
        que el resultado de liberar toda la memoria resulta en el bloque original (2^4)
        """

        a : BuddyAllocator = BuddyAllocator(16) 
        for i in range(0, 16):
            self.assertTrue(a.reserve_name(str(i), 1))
        
        for i in range(0, 16):
            self.assertTrue(a.free_name(str(i)))
        
        self.assertTrue(not a.roots[0].splitted and not a.roots[0].used)
    

    def test_internal_split_and_merge(self):
        """
        Prueba la division de memoria usando lo restante de los bloques para hacer mas bloques.
        Los libera y espera que se vuelva al bloque original.
        """

        a : BuddyAllocator = BuddyAllocator(16)
        self.assertTrue(a.reserve_name("a", 10))
        self.assertTrue(a.reserve_name("b", 4))
        self.assertTrue(a.reserve_name("c", 2))
        self.assertTrue(a.free_name("a"))
        self.assertTrue(a.reserve_name("a", 8))
        self.assertTrue(a.reserve_name("d", 2))

        self.assertTrue(a.free_name("a"))
        self.assertTrue(a.free_name("b"))
        self.assertTrue(a.free_name("c"))
        self.assertTrue(a.free_name("d"))

        self.assertTrue(not a.roots[0].splitted and not a.roots[0].used and not a.roots[0].splitted)  

        # Prueba rapida de buscar menor potencia y dividirla.
        a : BuddyAllocator = BuddyAllocator(20)
        self.assertTrue(a.reserve_name("a", 7))
        self.assertTrue(a.free_name("a"))      


    def test_full_blocks(self):
        """
        Prueba que no se pueda reservar bloques de memoria cuando todo esta full.
        """

        a : BuddyAllocator = BuddyAllocator(1)
        self.assertTrue(a.reserve_name("a", 1))
        self.assertFalse(a.reserve_name("b", 100))

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