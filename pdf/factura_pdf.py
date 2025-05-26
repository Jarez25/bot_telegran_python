from conn.woocommerce_config import wcapi
from fpdf import FPDF
from datetime import datetime


class FacturaPDF(FPDF):
    def header(self):
        # Encabezado
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, "Factura Comercial", border=False, ln=True, align='C')
        self.set_font('Arial', '', 12)
        self.cell(
            0, 10, f"Fecha: {datetime.now().strftime('%d/%m/%Y')}", ln=True, align='R')
        self.ln(5)

    def footer(self):
        # Pie de página
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', align='C')


def generar_factura_ultimo_pedido(nombre_archivo="factura_ultimo_pedido.pdf"):
    response = wcapi.get(
        "orders", params={"orderby": "date", "order": "desc", "per_page": 1})
    if response.status_code != 200:
        print(f"Error API WooCommerce: {response.status_code}")
        return None

    pedidos = response.json()
    if not pedidos:
        print("No hay pedidos disponibles.")
        return None

    pedido = pedidos[0]
    billing = pedido.get("billing", {})
    productos = pedido.get("line_items", [])
    total_pedido = pedido.get("total", "0.00")

    pdf = FacturaPDF()
    pdf.add_page()

    # Datos del cliente
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Datos del Cliente:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(
        0, 8, f"Nombre: {billing.get('first_name', '')} {billing.get('last_name', '')}", ln=True)
    pdf.cell(0, 8, f"Email: {billing.get('email', '')}", ln=True)
    pdf.cell(0, 8, f"Teléfono: {billing.get('phone', '')}", ln=True)
    pdf.ln(5)

    # Línea separadora
    pdf.set_draw_color(200, 200, 200)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)

    # Tabla de productos
    pdf.set_font("Arial", "B", 12)
    pdf.cell(100, 10, "Producto", border=1)
    pdf.cell(30, 10, "Cantidad", border=1, align="C")
    pdf.cell(60, 10, "Total", border=1, align="R")
    pdf.ln()

    pdf.set_font("Arial", "", 12)
    for item in productos:
        nombre = item.get("name", "Producto")
        cantidad = str(item.get("quantity", 1))
        total = f"${item.get('total', '0.00')}"
        pdf.cell(100, 10, nombre, border=1)
        pdf.cell(30, 10, cantidad, border=1, align="C")
        pdf.cell(60, 10, total, border=1, align="R")
        pdf.ln()

    # Total
    pdf.set_font("Arial", "B", 12)
    pdf.cell(130, 10, "Total del Pedido", border=1)
    pdf.cell(60, 10, f"${total_pedido}", border=1, align="R")

    pdf.output(nombre_archivo)
    print(f"Factura generada: {nombre_archivo}")
    return nombre_archivo
