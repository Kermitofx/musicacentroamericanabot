import requests
from bottle import Bottle, response, request as bottle_request

class BotHandlerMixin:
  BOT_URL = None  

  def get_chat_id(self, data):
    """
    Method to extract chat id from telegram request.
    """
    chat_id = data['message']['chat']['id']

    return chat_id

  def get_message(self, data):
    """
    Method to extract message id from telegram request.
    """

    message_text = data['message']['text']

    return message_text

  def send_message(self, prepared_data):
    """
    Prepared data should be json which includes at least `chat_id` and `text`
    """
    message_url = self.BOT_URL + 'sendMessage'
    requests.post(message_url, json=prepared_data)

class TelegramBot(BotHandlerMixin, Bottle):
  BOT_URL = 'https://api.telegram.org/bot922819890:AAHxhX_b6dWU11fdSuHUMz6DBxu1aPBnr1k/'

  def __init__(self, *args, **kwargs):
    super(TelegramBot, self).__init__()
    self.route('/', callback=self.post_handler, method="POST")

  def change_text_message(self, text):
    """
    To enable turning our message inside out.
    """
    return text[::-1]

  def prepare_data_for_answer(self, data):
    message = self.get_message(data)
    answer = self.change_text_message(message)
    chat_id = self.get_chat_id(data)

    json_data = {
      "chat_id": chat_id,
      "text": answer,
    }

    return json_data

  def post_handler(self):
    data = bottle_request.json
    print(data)
    answer_data = self.prepare_data_for_answer(data)
    self.send_message(answer_data)

    return response


if __name__ == '__main__':
  app = TelegramBot()
  app.run(host='localhost', port=8080, debug=True)

