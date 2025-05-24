from conn.woocommerce_config import wcapi


def obtener_producto_por_sku(sku):
    response = wcapi.get("products", params={"sku": sku}).json()
    if isinstance(response, list) and response:
        return response[0]
    return None
