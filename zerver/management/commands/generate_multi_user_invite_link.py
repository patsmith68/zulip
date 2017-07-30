from __future__ import absolute_import
from __future__ import print_function

from typing import Any

from argparse import ArgumentParser
from confirmation.models import Confirmation, create_confirmation_link
from zerver.lib.management import ZulipBaseCommand
from zerver.models import MultiUserInvitation

class Command(ZulipBaseCommand):
    help = "Generate user invitation links which can be used multiple times"

    def add_arguments(self, parser):
        # type: (ArgumentParser) -> None
        parser.add_argument("-l", "--limit",
                            dest="limit",
                            type=int,
                            help="Maximum number of users that can be invited using the link")

        self.add_realm_args(parser, True)

    def handle(self, *args, **options):
        # type: (*Any, **Any) -> None
        realm = self.get_realm(options)
        user_limit = options["limit"]
        invite = MultiUserInvitation(realm=realm, uses_remaining=user_limit)
        invite.save()
        invite_link = create_confirmation_link(invite, realm.host, Confirmation.MULTI_USER_INVITE)
        if user_limit is not None:
            print("You can use %s to invite upto %s people to the organization." % (invite_link, user_limit))
        else:
            print("You can use %s to invite as many number of people to the organization." % (invite_link,))
