import requests
from funciones.actualizar_producto import actualizar_producto


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
