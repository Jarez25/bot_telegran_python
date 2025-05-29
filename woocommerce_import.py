import requests
from funciones.actualizar_producto import actualizar_producto
from conn.woocommerce_config import wcapi, mensajes_bot

# Cache para evitar duplicar búsqueda/creación de categorías
categorias_creadas = {}


def obtener_id_categoria(nombre_categoria):
    if nombre_categoria in categorias_creadas:
        return categorias_creadas[nombre_categoria]

    try:
        response = wcapi.get("products/categories",
                             params={"search": nombre_categoria})
        data = response.json()

        if isinstance(data, list) and len(data) > 0 and "id" in data[0]:
            categoria_id = data[0]["id"]
        else:
            # Si no existe, crearla
            nueva = wcapi.post("products/categories", {
                "name": nombre_categoria,
                "slug": nombre_categoria.lower().replace(" ", "-")
            }).json()
            categoria_id = nueva.get("id")

        categorias_creadas[nombre_categoria] = categoria_id
        return categoria_id

    except Exception as e:
        print(
            f"❌ Error obteniendo o creando la categoría '{nombre_categoria}': {e}")
        return None


def actualizar_productos():
    response = requests.get(
        "https://divia.serverupagency.com/api/items/compuflash")
    data = response.json()
    productos = data.get("productos", [])

    for p in productos:
        categoria_nombre = p.get("categoria", "Sin categoría")
        categoria_id = obtener_id_categoria(categoria_nombre)

        # Si falló al obtener la categoría, omitir el producto
        if not categoria_id:
            print(
                f"⚠️ Producto '{p['nombre']}' omitido por fallo en categoría.")
            continue

        producto = {
            "sku": p["sku"],
            "name": p["nombre"],
            "price": str(p["precio"]),
            "regular_price": str(p["precio"]),
            "stock_quantity": p["stock"],
            "type": "simple",
            "images": [{"src": p["image"]}],
            "categories": [{"id": categoria_id}]
        }

        actualizar_producto(producto)


if __name__ == "__main__":
    actualizar_productos()

    with open("mensajes_bot.txt", "w", encoding="utf-8") as f:
        for m in mensajes_bot:
            f.write(m + "\n")
