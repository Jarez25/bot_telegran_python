import csv
from datetime import datetime
from conn.woocommerce_config import wcapi


def exportar_pedidos_csv(nombre_archivo="pedidos.csv"):
    pedidos = wcapi.get("orders").json()
    pedidos = pedidos if isinstance(
        pedidos, list) else pedidos.get('orders', [])

    if not pedidos:
        raise Exception("No se encontraron pedidos.")

    # Crea el CSV con encabezados comunes
    with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as archivo_csv:
        campos = ['ID', 'Fecha', 'Cliente', 'Total', 'Estado']
        writer = csv.DictWriter(archivo_csv, fieldnames=campos)
        writer.writeheader()

        for pedido in pedidos:
            writer.writerow({
                'ID': pedido['id'],
                'Fecha': pedido['date_created'],
                'Cliente': f"{pedido['billing']['first_name']} {pedido['billing']['last_name']}",
                'Total': pedido['total'],
                'Estado': pedido['status']
            })

    return nombre_archivo
