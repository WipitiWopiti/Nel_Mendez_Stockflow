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

    for pedido in pedidos:
        # PUNTO CRITICO
        if stock[pedido[1]] >= pedido[2]:
            stock[pedido[1]] -= pedido[2]
            print(f"Pedido {pedido[0]} procesado")
        else:
            print(f"""No hay suficientes unidades de {pedido[1]} para el pedido {pedido[0]}
    Unidades restantes: {stock[pedido[1]]}\n""")


if __name__ == "__main__":

    for caja in range(NUM_CAJAS - 1):
        hilo_caja = threading.Thread(target=procesar_pedido, args=(STOCK_INICIAL, PEDIDOS))
        hilo_caja.start()
