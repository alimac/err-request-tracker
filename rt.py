import re
import rt

from errbot import BotPlugin, botcmd, re_botcmd

class RT(BotPlugin):
    """Request Tracker plugin for Err"""

    tracker = None

    def get_configuration_template(self):
        return {'USER':'changeme','PASSWORD':'changeme','URL':'http://changeme'}

    def check_configuration(self, configuration):
        pass

    def rt_login(self):
        if self.tracker:
           return

        self.tracker = rt.Rt('%s/REST/1.0/' % self.config['URL'])
        response = self.tracker.login(self.config['USER'], self.config['PASSWORD'])

    @re_botcmd(pattern=r'(^| )(\d{6,})( |$)', prefixed=False, flags=re.IGNORECASE)
    def find_ticket(self, message, match):
        ticket = match.group(2)
        self.send(message.frm, self.ticket_summary(ticket), message_type=message.type)

    def ticket_summary(self, ticket_id):
        ticket_url = self.config['URL'] + "/Ticket/Display.html?id=" + ticket_id

        self.rt_login()
        ticket = self.tracker.get_ticket(ticket_id)

        return "'%s' in %s from %s\n%s" % (
            format(ticket.get("Subject", "No subject")),
            format(ticket.get("Queue")),
            format(ticket.get("Requestors")),
            format(ticket_url),
        )
