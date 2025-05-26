from conn.woocommerce_config import wcapi


def obtener_pedidos_por_estado(estado):
    response = wcapi.get("orders", params={"status": estado})
    if response.status_code != 200:
        print(f"Error API WooCommerce: {response.status_code}")
        return []
    data = response.json()
    # Debug para ver qué devuelve exactamente la API
    print(f"Respuesta API: {data}")
    return data if isinstance(data, list) else []
