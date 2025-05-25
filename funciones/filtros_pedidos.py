from conn.woocommerce_config import wcapi


def obtener_pedidos_por_estado(estado):
    response = wcapi.get("orders", params={"status": estado})
    if response.status_code != 200:
        return []
    data = response.json()
    pedidos = data if isinstance(data, list) else data.get('orders', [])
    return pedidos
