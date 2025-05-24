from conn.woocommerce_config import wcapi


def contar_productos():
    # Consulta solo 1 producto para obtener el total vía header
    response = wcapi.get("products", params={"per_page": 1})
    total = response.headers.get("X-WP-Total", "No disponible")
    return total
