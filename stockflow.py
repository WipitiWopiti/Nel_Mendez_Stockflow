import threading
from datos import (
    STOCK_INICIAL,
    PEDIDOS,
    REPOSICIONES,
    NUM_CAJAS,
    NUM_REVISORES,
    NUM_TERMINALES,
)



def procesar_pedido(stock:dict, pedidos:tuple):
    
    global reposicion_requerida

    with semaforo:
        print("[SEMAFORO] Terminal ocupado")
        for pedido in pedidos:
            with condition:
                while reposicion_requerida is True:
                    condition.wait()

                # PUNTO CRITICO
                with lock:
                    if stock[pedido[1]] >= pedido[2]:
                        stock[pedido[1]] -= pedido[2]
                        print(f"Pedido {pedido[0]} procesado")
                    else:
                        reposicion_requerida = True
                        
        print("[SEMAFORO] Terminal Liberado")

def reposiciones_almacen(stock, reposiciones):

    with condition:
        while reposicion_requerida is True:
            for producto, cantidad in stock.items():
                for reposicion in reposiciones:
                    if producto == reposicion[1]:
                        cantidad += reposicion[2]
                        stock.update({producto:cantidad})
        condition.notify()



if __name__ == "__main__":

    lock = threading.Lock()
    semaforo = threading.Semaphore(NUM_TERMINALES)
    condition = threading.Condition()

    reposicion_requerida = False
    
    lista_hilos_pedidos = [threading.Thread(target=procesar_pedido, args=(STOCK_INICIAL, PEDIDOS)) for _ in range(NUM_CAJAS - 1)]
    lista_hilos_reposiciones = [threading.Thread(target=reposiciones_almacen, args=(STOCK_INICIAL, REPOSICIONES)) for _ in range(1)]

    for hilo in lista_hilos_pedidos:
        hilo.start()
        
    for hilo in lista_hilos_reposiciones:
        hilo.start()

    for hilo in lista_hilos_pedidos:
        hilo.join()
    
    for hilo in lista_hilos_reposiciones:
        hilo.join()