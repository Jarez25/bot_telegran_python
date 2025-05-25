from conn.woocommerce_config import wcapi


def listar_categorias():
    response = wcapi.get("products/categories").json()
    if isinstance(response, dict) and "code" in response:
        return None
    return response
