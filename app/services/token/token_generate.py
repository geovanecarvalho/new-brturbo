from secrets import token_hex


class Token:
    def __init__(self):
        self.token = token_hex(2).upper()

    def generate_new_token(self):
        self.token = token_hex(2).upper()

    def get_token(self):
        return self.token
