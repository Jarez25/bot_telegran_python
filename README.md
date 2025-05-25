# 🤖 Bot de Telegram para Gestión de WooCommerce

Este bot de Telegram está desarrollado usando la librería [pyTelegramBotAPI (Telebot)](https://pytba.readthedocs.io/en/latest/install.html). Su objetivo principal es permitir la interacción con una tienda WooCommerce directamente desde Telegram, facilitando tareas como sincronizar productos, consultar información y administrar categorías.

---

## 🚀 Características

- Comando `/start` para dar la bienvenida al usuario.
- Comando `/help` para mostrar la lista de comandos disponibles.
- Comando `/woo` para iniciar sincronización de productos.
- Comando `/update` para actualizar productos.
- Comando `/producto SKU` para consultar información de un producto.
- Comando `/nueva_categoria Nombre` para crear una categoría.
- Comando `/categorias` para listar todas las categorías.
- Comando `/editar_categoria ID NuevoNombre` para editar una categoría.
- Comando `/eliminar_categoria ID` para eliminar una categoría.
- Manejo del archivo `.env` para proteger credenciales.

---

## 📦 Requisitos

- Python 3.7 o superior
- pip
- Una tienda WooCommerce con la API REST habilitada

---

## 🛠️ Instalación

1. **Clona el repositorio:**

   ```bash
   git clone https://github.com/Jarez25/bot_telegran_python.git
   cd tu-repo

    Crea un entorno virtual (opcional pero recomendado):

python -m venv venv
# En Linux/macOS:
source venv/bin/activate
# En Windows:
venv\Scripts\activate

Instala las dependencias:

pip install -r requirements.txt

Crea un archivo .env con tu token de bot y claves de WooCommerce:

    TELEGRAM_TOKEN=tu_token_de_telegram
    WC_URL=https://tu-tienda.com
    WC_CONSUMER_KEY=ck_xxxxxxxxxxxxxxxxxxxxx
    WC_CONSUMER_SECRET=cs_xxxxxxxxxxxxxxxxxxxxx

▶️ Ejecutar el bot

python main.py

📚 Documentación oficial

    pyTelegramBotAPI

    WooCommerce REST API

🛡️ Notas de seguridad

    Nunca subas tu archivo .env a un repositorio público.

    Usa .gitignore para excluir archivos sensibles como .env.

📄 Licencia

MIT License.


¿Deseas que este `README.md` se guarde como archivo dentro del proyecto también?