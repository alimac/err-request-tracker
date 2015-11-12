import re
import rt

from errbot import BotPlugin, botcmd, re_botcmd

class RT(BotPlugin):
    """Request Tracker plugin for Err"""

    tracker = None

    def get_configuration_template(self):
        return {'USER':'','PASSWORD':'','REST_URL':'', 'DISPLAY_URL':''}

    def check_configuration(self, configuration):
        pass

    def rt_login(self):
        if self.tracker:
           return

        self.tracker = rt.Rt(self.config['REST_URL'])
        response = self.tracker.login(self.config['USER'], self.config['PASSWORD'])

    @re_botcmd(pattern=r'(^| )(\d{3,})( |\?|\.|,|:|\!|$)', prefixed=False, flags=re.IGNORECASE)
    def find_ticket(self, message, match):
        ticket = match.group(2)
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
