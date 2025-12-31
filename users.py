users = {}

FREE_LIMIT = 5
PRO_LIMIT = 100


def get_user(user_id):
    if user_id not in users:
        users[user_id] = {
            "plan": "free",
            "requsts_left": FREE_LIMIT,
            "model": "yandex"
        }
    return users[user_id]



def can_use(user_id):
    user = get_user(user_id)

    if user["requests_left"] <= 0:
        return False
    
    user["requests_left"] -= 1
    return True