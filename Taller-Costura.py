import logging
import threading
import time

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )


class Canasta(object):
    def __init__(self, start=0):
        self.value = start

    def poner(self):
        self.value = self.value + 1

    def quitar(self, n):
        self.value = self.value - n


def mangas(cond_mangas, canasta_mangas):
    logging.debug('Empieza a fabricar')
    while canasta_mangas.value < 10:
        with cond_mangas:
            canasta_mangas.poner()
            logging.debug('Lleva {}'.format(canasta_mangas.value))
            if canasta_mangas.value >= 2:
                cond_mangas.notifyAll()
                time.sleep(2)


def cuerpo(cond_cuerpo, canasta_cuerpo):
    logging.debug('Empieza a fabricar')
    while canasta_cuerpo.value < 10:
        with cond_cuerpo:
            canasta_cuerpo.poner()
            logging.debug('Lleva {}'.format(canasta_cuerpo.value))
            if canasta_cuerpo.value >= 1:
                cond_cuerpo.notifyAll()
                time.sleep(4)


def ensamble(cond_mangas, cond_cuerpo, canasta_mangas, canasta_cuerpo):
    num_piezas = 0
    while num_piezas < 5:
        with cond_mangas, cond_cuerpo:
            logging.debug('Esperando por mangas')
            cond_mangas.wait()
            logging.debug('Mangas listas')
            logging.debug('Esperando por cuerpo')
            cond_cuerpo.wait()
            logging.debug('Cuerpo listo')
            logging.debug('Material listo para fabricar')
            canasta_mangas.quitar(2)
            canasta_cuerpo.quitar(1)
            logging.debug('Quedan {} mangas'.format(canasta_mangas.value))
            logging.debug('Quedan {} cuerpos'.format(canasta_cuerpo.value))
            num_piezas += 1
            logging.debug('Se hizo 1 pieza. Ahora hay {}'.format(num_piezas))


cond_mangas = threading.Condition()
cond_cuerpo = threading.Condition()
canasta_mangas = Canasta()
canasta_cuerpo = Canasta()
c1 = threading.Thread(name='Mangas', target=mangas, args=(cond_mangas, canasta_mangas,))
c2 = threading.Thread(name='Cuerpo', target=cuerpo, args=(cond_cuerpo, canasta_cuerpo))
e = threading.Thread(name='Ensamble', target=ensamble, args=(cond_mangas, cond_cuerpo, canasta_mangas, canasta_cuerpo,))

e.start()
c1.start()
c2.start()
