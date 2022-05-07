from hashlib import md5


def hash_password_in_dict(json_data: dict) -> dict:
    password = json_data.get('user_password')
    if password is not None:
        json_data['user_password'] = md5(password.encode()).hexdigest()
    return json_data


def patch_json_data(json_data, post_data):
    result_data = {}
    for key_name in json_data.keys():
        if key_name == 'id':
            continue
        result_data.setdefault(key_name, post_data.get(key_name, json_data.get(key_name)))
    return result_data



