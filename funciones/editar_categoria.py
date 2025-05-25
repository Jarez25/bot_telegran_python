from conn.woocommerce_config import wcapi


def editar_categoria(categoria_id, nuevo_nombre):
    data = {
        "name": nuevo_nombre
    }
    response = wcapi.put(f"products/categories/{categoria_id}", data).json()
    if response.get("id"):
        return {
            "id": response.get("id"),
            "name": response.get("name")
        }
    return None
