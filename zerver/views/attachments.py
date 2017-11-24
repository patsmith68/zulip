from django.http import HttpRequest, HttpResponse

from zerver.models import Attachment, UserProfile
from zerver.lib.validator import check_int
from zerver.lib.response import json_success
from zerver.lib.attachments import user_attachments, remove_attachment, \
    access_attachment_by_id
from zerver.lib.actions import notify_attachment_update


def list_by_user(request, user_profile):
    # type: (HttpRequest, UserProfile) -> HttpResponse
    return json_success({"attachments": user_attachments(user_profile)})


def remove(request, user_profile, attachment_id):
    # type: (HttpRequest, UserProfile, int) -> HttpResponse
    attachment = access_attachment_by_id(user_profile, attachment_id,
                                         needs_owner=True)
    if attachment is not None:
        attachment_dict = attachment.to_dict()
    remove_attachment(user_profile, attachment)
    notify_attachment_update(user_profile, "remove", attachment_dict)
    return json_success()
