import requests
from funciones.actualizar_producto import actualizar_producto
from conn.woocommerce_config import wcapi, mensajes_bot


def actualizar_productos():
    response = requests.get("https://fakestoreapi.com/products")
    productos_falsos = response.json()

    for p in productos_falsos:
        producto = {
            "sku": f"FAKE-{p['id']}",
            "name": p['title'],
            "price": str(p['price']),
            "regular_price": str(p['price']),
            "stock_quantity": 10,
            "type": "simple",
            "images": [{"src": p["image"]}]
        }
        actualizar_producto(producto)


if __name__ == "__main__":
    actualizar_productos()

    with open("mensajes_bot.txt", "w", encoding="utf-8") as f:
        for m in mensajes_bot:
            f.write(m + "\n")
