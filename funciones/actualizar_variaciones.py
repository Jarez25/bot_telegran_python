from conn.woocommerce_config import wcapi, mensajes_bot


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
