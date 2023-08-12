import requests
# from create import TOKEN_BOT, CHAT_ID
#
#
# def send_message(message: str) -> None:
#     """Send message to the Telegram channel."""
#     url = f'https://api.telegram.org/bot{TOKEN_BOT}/sendMessage'
#     data = {'chat_id': CHAT_ID, 'text': message}
#     requests.post(url, data=data)
# Create a generator output the dict_test.
def generator_dict(dict_test: dict) -> str:
    """Generator output the dict_test."""
    for key, value in dict_test.items():
        yield f'{key} {value}'



if __name__ == '__main__':
    dict_test = {'a': 1, 'b': 2, 'c': 3}
    if dict_test.get('e', False) & False:
        print(1)

