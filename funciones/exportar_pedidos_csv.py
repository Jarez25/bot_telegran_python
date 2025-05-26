import csv
from conn.woocommerce_config import wcapi


def exportar_pedidos_csv(nombre_archivo="pedidos.csv"):
    pagina = 1
    pedidos = []

    while True:
        respuesta = wcapi.get(
            "orders", params={"per_page": 100, "page": pagina})
        lote = respuesta.json()

        if not isinstance(lote, list) or not lote:
            break

        pedidos.extend(lote)
        pagina += 1

    if not pedidos:
        raise Exception("No se encontraron pedidos.")

    with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as archivo_csv:
        campos = [
            'Pedido ID', 'Fecha', 'Cliente', 'Teléfono', 'Correo',
            'Producto(s)', 'Total del Pedido', 'Método de pago', 'Estado'
        ]
        writer = csv.DictWriter(archivo_csv, fieldnames=campos)
        writer.writeheader()

        for pedido in pedidos:
            billing = pedido.get('billing', {})
            cliente = f"{billing.get('first_name', '').strip()} {billing.get('last_name', '').strip()}".strip(
            )
            telefono = billing.get('phone', '')
            correo = billing.get('email', '')
            total = pedido.get('total', '')
            metodo_pago = pedido.get('payment_method_title', '')
            estado = pedido.get('status', '').capitalize()
            fecha = pedido.get('date_created', '')

            productos = [item.get('name', '')
                         for item in pedido.get('line_items', [])]

            writer.writerow({
                'Pedido ID': pedido.get('id'),
                'Fecha': fecha,
                'Cliente': cliente,
                'Teléfono': telefono,
                'Correo': correo,
                'Producto(s)': ' | '.join(productos),
                'Total del Pedido': total,
                'Método de pago': metodo_pago,
                'Estado': estado
            })

    return nombre_archivo
