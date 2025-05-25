# import requests

# webhook que es ?
# webhook para woocommerce?

# def notificar_nuevo_pedido(pedido, bot_token, chat_id):
#     """
#     Envía una notificación a Telegram cuando se recibe un nuevo pedido.

#     :param pedido: Diccionario con los datos del pedido.
#     :param bot_token: Token del bot de Telegram.
#     :param chat_id: ID del usuario o grupo que recibirá la notificación.
#     """
#     try:
#         cliente = f"{pedido['billing']['first_name']} {pedido['billing']['last_name']}"
#         mensaje = (
#             f"🆕 *Nuevo pedido recibido*\n\n"
#             f"🧾 Pedido: #{pedido['id']}\n"
#             f"👤 Cliente: {cliente}\n"
#             f"💵 Total: ${pedido['total']}\n"
#             f"📅 Fecha: {pedido['date_created'][:10]}\n"
#             f"📦 Estado: {pedido['status'].capitalize()}"
#         )

#         url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
#         payload = {
#             "chat_id": chat_id,
#             "text": mensaje,
#             "parse_mode": "Markdown"
#         }

#         response = requests.post(url, json=payload)
#         if not response.ok:
#             print("❌ Error al enviar notificación:", response.text)
#     except Exception as e:
#         print(f"❌ Error al procesar la notificación: {e}")
