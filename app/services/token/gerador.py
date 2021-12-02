from secrets import token_hex


def generation_token():
    with open("app/services/token/token.txt", "w") as f:
        f.write(token_hex(2))


def read_token():
    with open("app/services/token/token.txt", "r") as f:
        token = f.readline()

    return token
