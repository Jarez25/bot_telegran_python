import csv
from conn.woocommerce_config import wcapi


def exportar_productos_csv(nombre_archivo="productos.csv"):
    pagina = 1
    productos = []

    while True:
        respuesta = wcapi.get("products", params={
                              "per_page": 100, "page": pagina})
        lote = respuesta.json()

        if not isinstance(lote, list) or not lote:
            break

        productos.extend(lote)
        pagina += 1

    if not productos:
        raise Exception("No se encontraron productos.")

    with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as archivo_csv:
        campos = [
            'ID', 'Nombre', 'SKU', 'Precio Regular', 'Precio de Oferta',
            'Stock', 'Estado', 'Categorías', 'Etiquetas'
        ]
        writer = csv.DictWriter(archivo_csv, fieldnames=campos)
        writer.writeheader()

        for producto in productos:
            categorias = [cat.get('name', '')
                          for cat in producto.get('categories', [])]
            etiquetas = [tag.get('name', '')
                         for tag in producto.get('tags', [])]

            writer.writerow({
                'ID': producto.get('id'),
                'Nombre': producto.get('name', ''),
                'SKU': producto.get('sku', ''),
                'Precio Regular': producto.get('regular_price', ''),
                'Precio de Oferta': producto.get('sale_price', ''),
                'Stock': producto.get('stock_quantity', ''),
                'Estado': producto.get('status', ''),
                'Categorías': ' | '.join(categorias),
                'Etiquetas': ' | '.join(etiquetas)
            })

    return nombre_archivo
