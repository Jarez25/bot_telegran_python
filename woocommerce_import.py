import json
import requests
from woocommerce import API

mensajes_bot = []

# Conexión WooCommerce
wcapi = API(
    url="http://teleapp.test/",  # Asegúrate de que este dominio sea válido
    consumer_key="ck_3c69dfb55e7a995cd4305c9fda440350bce945eb",
    consumer_secret="cs_67bd944bb29e230039a4d311be133ee24a1d7717",
    version="wc/v3"
)


def obtener_producto_por_sku(sku):
    response = wcapi.get("products", params={"sku": sku}).json()
    if isinstance(response, list) and response:
        return response[0]
    return None


def actualizar_producto(producto_local):
    producto_remoto = obtener_producto_por_sku(producto_local["sku"])

    if not producto_remoto:
        # Crear producto si no existe
        response = wcapi.post("products", producto_local).json()
        mensajes_bot.append(
            f"🆕 Producto creado: {producto_local['name']} ({producto_local['sku']})")
        return

    producto_id = producto_remoto["id"]
    cambios = {}

    campos_comparar = ["name", "price", "regular_price", "stock_quantity"]
    for campo in campos_comparar:
        if campo in producto_local and producto_local.get(campo) != producto_remoto.get(campo):
            cambios[campo] = producto_local[campo]

    # Verificar imagen
    imagen_local = producto_local.get("images", [])
    imagen_remota = producto_remoto.get("images", [])

    if imagen_local and (not imagen_remota or imagen_local[0]["src"] != imagen_remota[0]["src"]):
        cambios["images"] = imagen_local

    if cambios:
        wcapi.put(f"products/{producto_id}", cambios).json()
        mensajes_bot.append(
            f"🔄 Producto actualizado: {producto_local['name']} ({producto_local['sku']})")
    else:
        mensajes_bot.append(
            f"✅ Sin cambios: {producto_local['name']} ({producto_local['sku']})")

    if producto_local.get("type") == "variable":
        actualizar_variaciones(
            producto_id, producto_local.get("variations", []))


def actualizar_variaciones(parent_id, variaciones_locales):
    variaciones_remotas = wcapi.get(f"products/{parent_id}/variations").json()
    skus_remotos = {v["sku"]: v for v in variaciones_remotas if v["sku"]}

    for variacion in variaciones_locales:
        sku = variacion.get("sku")
        if not sku:
            continue

        if sku in skus_remotos:
            var_remota = skus_remotos[sku]
            cambios = {}
            campos = ["price", "regular_price", "stock_quantity", "attributes"]
            for campo in campos:
                if variacion.get(campo) != var_remota.get(campo):
                    cambios[campo] = variacion[campo]

            if cambios:
                wcapi.put(
                    f"products/{parent_id}/variations/{var_remota['id']}", cambios).json()
                mensajes_bot.append(f"🔄 Variación actualizada: {sku}")
            else:
                mensajes_bot.append(f"✅ Sin cambios en variación: {sku}")
        else:
            wcapi.post(f"products/{parent_id}/variations", variacion).json()
            mensajes_bot.append(f"🆕 Variación creada: {sku}")


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
