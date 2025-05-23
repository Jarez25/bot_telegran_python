# -*- coding: utf-8 -*-
import json
from woocommerce import API

# Configurar WooCommerce API
wcapi = API(
    url="http://172.26.160.1",
    consumer_key="ck_16e6900c7bb7eae06702a478c8b3e455a00623a1",
    consumer_secret="cs_950614640a36fceb309c61141a16106db9afe11b",
    version="wc/v3"
)

# Leer el archivo JSON
with open('product.json', 'r', encoding='utf-8') as file:
    productos = json.load(file)

parent_id = None
for producto in productos:
    try:
        if producto["type"] == "variation":
            if parent_id:
                response = wcapi.post(f"products/{parent_id}/variations", producto).json()
                print("Variación creada:", response.get("id"))
            else:
                print("❌ No hay producto padre definido para la variación:", producto["name"])
        else:
            response = wcapi.post("products", producto).json()
            print("Producto creado:", response.get("id"))
            if producto["type"] == "variable":
                parent_id = response.get("id")
    except Exception as e:
        print("Error al crear producto:", producto.get("name"), e)
