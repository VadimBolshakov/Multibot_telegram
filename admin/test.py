import requests
from create import TOKEN_BOT, CHAT_ID


def send_message(message: str) -> None:
    """Send message to the Telegram channel."""
    url = f'https://api.telegram.org/bot{TOKEN_BOT}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': message}
    requests.post(url, data=data)


if __name__ == '__main__':
    var = None
    if var:
        print('True')
    else:
        print('False')

    # send_message('Hello, world!')
