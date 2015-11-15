import os
import unittest
import rt
import requesttracker
from errbot.backends.test import testbot
from errbot import plugin_manager

RT_CONFIG = {'USER': os.environ.get('RT_USER'),
             'PASSWORD': os.environ.get('RT_PASSWORD'),
             'DISPLAY_URL': os.environ.get('RT_DISPLAY_URL'),
             'REST_URL': os.environ.get('RT_REST_URL')}


class TestRT(object):
    extra_plugin_dir = '.'

    def test_configuration(self, testbot):
        testbot.push_message('!plugin config RT ' + str(RT_CONFIG))
        assert 'Plugin configuration done.' in testbot.pop_message()

    def test_find_ticket(self, testbot):
        test_subject = 'err-request-tracker'
        test_requestor = 'foo@example.com'

        testbot.push_message('!plugin config RT ' + str(RT_CONFIG))
        assert 'Plugin configuration done.' in testbot.pop_message()

        tracker = rt.Rt(RT_CONFIG['REST_URL'])
        tracker.login(RT_CONFIG['USER'], RT_CONFIG['PASSWORD'])

        try:
            ticket_id = tracker.create_ticket(Queue='General',
                                              Subject=test_subject,
                                              Requestors=test_requestor)
            ticket = tracker.get_ticket(ticket_id)
        except Exception as e:
            raise Exception("Unable to create a test ticket: " + str(e))

        testbot.push_message(str(ticket_id))
        assert "%s (%s%s) in General from %s" % (
            test_subject,
            RT_CONFIG['DISPLAY_URL'],
            str(ticket_id),
            test_requestor) in testbot.pop_message()
