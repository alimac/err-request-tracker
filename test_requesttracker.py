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
