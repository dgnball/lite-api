from users.libraries.token import Token


def token_to_user_pk(token):
    data = Token.decode_to_json(token)
    pk = data['id']
    return pk
