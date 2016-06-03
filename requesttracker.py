import re
import rt
from itertools import chain
from errbot.utils import ValidationException
from errbot import BotPlugin, botcmd, re_botcmd

CONFIG_TEMPLATE = {'USER': '',
                   'PASSWORD': '',
                   'REST_URL': '',
                   'DISPLAY_URL': '',
                   'MINIMUM_TICKET_ID': 1}


class RT(BotPlugin):
    """Request Tracker plugin for Err"""

    tracker = None
    re_find_ticket = r'(^| |(https?\:\/\/.+=))(\d{1,})( |\?|\.|,|:|\!|$)'

    def get_configuration_template(self):
        return CONFIG_TEMPLATE

    def configure(self, configuration):
        if configuration is not None and configuration != {}:
            config = dict(chain(CONFIG_TEMPLATE.items(),
                                configuration.items()))
        else:
            config = CONFIG_TEMPLATE

        super(RT, self).configure(config)

    def check_configuration(self, config):

        rt_login = False

        for key in ['REST_URL', 'DISPLAY_URL', 'USER', 'PASSWORD']:

            if key not in config:
                raise ValidationException("missing config value: " + key)

        try:
            tracker = rt.Rt('%s/REST/1.0/' % config['REST_URL'])
            rt_login = tracker.login(config['USER'], config['PASSWORD'])

        except Exception as error:
            raise ValidationException("Cannot connect to RT as %s: %s." % (
                config['USER'], format(error),
            ))

        if rt_login is False:
            raise ValidationException("Authentication failed")

    @re_botcmd(pattern=re_find_ticket, prefixed=False, flags=re.IGNORECASE)
    def find_ticket(self, message, match):
        """ Look up ticket metadata (works without prefix). Example: 12345 """
        url = match.group(2)
        ticket = match.group(3)

        if url and url != self.config['DISPLAY_URL']:
            return

        if int(ticket) >= self.config['MINIMUM_TICKET_ID']:
            return self.ticket_summary(ticket)

    def ticket_summary(self, ticket_id):

        self.tracker = rt.Rt(self.config['REST_URL'])
        self.tracker.login(self.config['USER'], self.config['PASSWORD'])

        try:
            ticket = self.tracker.get_ticket(ticket_id)

            return "[%s](%s) in %s from %s" % (
                format(ticket.get("Subject", "No subject")),
                format(self.config['DISPLAY_URL'] + ticket_id),
                format(ticket.get("Queue")),
                format(', '.join(ticket.get("Requestors")))
            )

        except:
            return "Sorry, that ticket does not exist or I cannot access it."
