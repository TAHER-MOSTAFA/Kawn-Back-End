from django.core.cache import cache


def cache_userstate_key(user_pk):
    return f"{user_pk}IsOnline"


def cache_user_is_online(user_pk):
    key = cache_userstate_key(user_pk)
    cache.set(key, True)


def cache_clear_userstate(user_pk):
    key = cache_userstate_key(user_pk)
    cache.delete(key)


def is_online(pk):
    state = cache.get(cache_userstate_key(pk))
    if state == None:
        return False
    return True
