import json
from woocommerce import API

mensajes_bot = []

# Definir wcapi globalmente
wcapi = API(
    url="http://telegran.test/",
    consumer_key="ck_16e6900c7bb7eae06702a478c8b3e455a00623a1",
    consumer_secret="cs_950614640a36fceb309c61141a16106db9afe11b",
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
        mensajes_bot.append(
            f"❌ Producto no encontrado para actualizar: {producto_local['name']}")
        return

    producto_id = producto_remoto["id"]
    cambios = {}

    campos_comparar = ["name", "price", "regular_price", "stock_quantity"]
    for campo in campos_comparar:
        if campo in producto_local and producto_local.get(campo) != producto_remoto.get(campo):
            cambios[campo] = producto_local[campo]

    if cambios:
        response = wcapi.put(f"products/{producto_id}", cambios).json()
        mensajes_bot.append(
            f"🔄 Producto actualizado: {producto_local['name']} ({producto_local['sku']})")
    else:
        mensajes_bot.append(
            f"✅ Sin cambios: {producto_local['name']} ({producto_local['sku']})")

    # Si el producto es variable, revisamos variaciones
    if producto_local["type"] == "variable":
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
            # Si no existe, se crea
            wcapi.post(f"products/{parent_id}/variations", variacion).json()
            mensajes_bot.append(f"🆕 Variación creada: {sku}")


def actualizar_productos():
    with open('product.json', 'r', encoding='utf-8') as file:
        productos = json.load(file)

    for producto in productos:
        if producto["type"] != "variation":
            actualizar_producto(producto)


if __name__ == "__main__":
    actualizar_productos()

    # Guardar mensajes
    with open("mensajes_bot.txt", "w", encoding="utf-8") as f:
        for m in mensajes_bot:
            f.write(m + "\n")
