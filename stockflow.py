import threading
from datos import (
    STOCK_INICIAL,
    PEDIDOS,
    REPOSICIONES,
    NUM_CAJAS,
    NUM_REVISORES,
    NUM_TERMINALES,
)
import time

def procesar_pedido(stock:dict, pedidos:tuple, solicitudes:list, reposiciones:list):

    with semaforo:
        print("[SEMAFORO] Terminal ocupado")
        for pedido in pedidos:
            with condition:
                print("Condicion pedido entrada")
                while stock[pedido[1]] < pedido[2]:
                    print(f"Esperando en pedido {pedido}")

                    if pedido not in solicitudes:
                        solicitudes.append(pedido)
                        condition.notify()

                    condition.wait()

                stock[pedido[1]] -= pedido[2]
                print(f"Pedido {pedido[0]} procesado")
                
                        
        print("[SEMAFORO] Terminal Liberado")

def reposiciones_almacen(stock:dict, reposiciones:list, solicitudes:list):

    with condition:
        print("Condition almacen entrada")
        while not solicitudes:
            condition.wait()

        solicitud = solicitudes.pop(0)

        for producto, cantidad in stock.items():
            for reposicion in reposiciones:
                if producto == reposicion[1] and producto == solicitud[1]:
                    cantidad += reposicion[2]
                    stock.update({producto:cantidad})
                    print("reposicion reposicionada")

        condition.notify_all()
        print("Notificacion hecha")



if __name__ == "__main__":

    lock = threading.Lock()
    semaforo = threading.Semaphore(NUM_TERMINALES)
    condition = threading.Condition()

    solicitudes_reposicion = []
    
    lista_hilos_pedidos = [threading.Thread(target=procesar_pedido, args=(STOCK_INICIAL, PEDIDOS, solicitudes_reposicion, REPOSICIONES)) for _ in range(NUM_CAJAS - 1)]
    lista_hilos_reposiciones = [threading.Thread(target=reposiciones_almacen, args=(STOCK_INICIAL, REPOSICIONES, solicitudes_reposicion)) for _ in range(1)]

    for hilo in lista_hilos_pedidos:
        hilo.start()
        
    for hilo in lista_hilos_reposiciones:
        hilo.start()

    for hilo in lista_hilos_pedidos:
        hilo.join()
    
    for hilo in lista_hilos_reposiciones:
        hilo.join()