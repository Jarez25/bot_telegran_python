from conn.woocommerce_config import wcapi


def crear_categoria(nombre_categoria):
    data = {
        "name": nombre_categoria
    }
    response = wcapi.post("products/categories", data).json()

    # Si se creó correctamente, devuelve el ID y nombre
    if response.get("id"):
        return {
            "id": response.get("id"),
            "name": response.get("name")
        }
    return None
