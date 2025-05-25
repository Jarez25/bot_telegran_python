from conn.woocommerce_config import wcapi


def eliminar_categoria(categoria_id):
    try:
        response = wcapi.delete(
            f"products/categories/{categoria_id}", params={"force": True}
        ).json()

        # Si devuelve un ID, se asume que fue eliminada
        if response.get("id"):
            return {
                "deleted": True,
                "id": response.get("id"),
                "name": response.get("name", "Desconocido")
            }
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
