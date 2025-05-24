import time
import requests
from conn.woocommerce_config import wcapi, mensajes_bot
from funciones.obtener_producto_sku import obtener_producto_por_sku
from funciones.actualizar_variaciones import actualizar_variaciones


def actualizar_producto(producto_local):
    try:
        producto_remoto = obtener_producto_por_sku(producto_local["sku"])
    except Exception as e:
        mensajes_bot.append(
            f"❌ Error al obtener producto remoto ({producto_local['sku']}): {e}")
        return

    try:
        if not producto_remoto:
            wcapi.post("products", producto_local).json()
            mensajes_bot.append(
                f"🆕 Producto creado: {producto_local['name']} ({producto_local['sku']})")
            return

        producto_id = producto_remoto["id"]
        cambios = {}

        campos_comparar = ["name", "price", "regular_price", "stock_quantity"]
        for campo in campos_comparar:
            if campo in producto_local and producto_local.get(campo) != producto_remoto.get(campo):
                cambios[campo] = producto_local[campo]

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

    except requests.exceptions.ReadTimeout:
        mensajes_bot.append(
            f"⏰ Timeout al procesar {producto_local['sku']}. Reintentando en 5s...")
        time.sleep(5)
        try:
            if not producto_remoto:
                wcapi.post("products", producto_local).json()
            else:
                wcapi.put(f"products/{producto_id}", cambios).json()
            mensajes_bot.append(
                f"🔁 Reintento exitoso: {producto_local['name']} ({producto_local['sku']})")
        except Exception as e:
            mensajes_bot.append(
                f"❌ Falló reintento para {producto_local['sku']}: {e}")
    except Exception as e:
        mensajes_bot.append(
            f"❌ Error inesperado con {producto_local['sku']}: {e}")
