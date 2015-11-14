import re
import rt
from itertools import chain
from errbot import BotPlugin, botcmd, re_botcmd

CONFIG_TEMPLATE = { 'USER':'',
                    'PASSWORD':'',
                    'REST_URL':'',
                    'DISPLAY_URL':'',
                    'MINIMUM_TICKET_ID':1 }


class RT(BotPlugin):
    """Request Tracker plugin for Err"""

    tracker = None

    def get_configuration_template(self):
        return CONFIG_TEMPLATE

    def configure(self, configuration):
        if configuration is not None and configuration != {}:
            config = dict(chain(CONFIG_TEMPLATE.items(), configuration.items()))
        else:
            config = CONFIG_TEMPLATE

        super(RT, self).configure(config)

    def check_configuration(self, config):

        for key in ['REST_URL','DISPLAY_URL','USER','PASSWORD']:

           if key not in config:
               raise Exception(key + "is missing")

    def rt_login(self):
        if self.tracker:
           return

        self.tracker = rt.Rt(self.config['REST_URL'])
        response = self.tracker.login(self.config['USER'], self.config['PASSWORD'])

    @re_botcmd(pattern=r'(^| |https?\:\/\/.+=)(\d{1,})( |\?|\.|,|:|\!|$)', prefixed=False, flags=re.IGNORECASE)
    def find_ticket(self, message, match):
        """ Look up ticket metadata (also works without prefix). Example: 12345 """
        url = match.group(1)
        ticket = match.group(2)

        if url and url != self.config['DISPLAY_URL']:
            return

        if int(ticket) >= self.config['MINIMUM_TICKET_ID']:
            self.send(message.frm, self.ticket_summary(ticket), message_type=message.type)

    def ticket_summary(self, ticket_id):

        self.rt_login()

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
