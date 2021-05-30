from django.http import HttpResponseForbidden

from .utils import CacheUsersMsgs


def UserInDialog(info, dialog_id):
    if info.context.user.id not in CacheUsersMsgs.get_dialog_get_or_set(dialog_id):
        return HttpResponseForbidden()
