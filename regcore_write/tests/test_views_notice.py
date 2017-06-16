import json
from unittest import TestCase

from django.test.client import Client
from mock import patch, call

from regcore_write.views.notice import *


class ViewsNoticeTest(TestCase):

    def test_add_not_json(self):
        url = '/notice/111/docdoc'
        response = Client().put(url, content_type='application/json',
                                data='{Invalid}')
        self.assertEqual(400, response.status_code)

    @patch('regcore_write.views.notice.db')
    def test_add_success(self, db):
        # Add a notice 
        url = '/notice/111/docdoc'
        response = Client().put(url, content_type='application/json',
                                data=json.dumps({'some': 'struct'}))
        self.assertTrue(db.Notices.return_value.put.called)
        args = db.Notices.return_value.put.call_args[0]
        self.assertEqual('docdoc', args[0])
        self.assertEqual('111', args[1])
        self.assertEqual({'some': 'struct'}, args[2])

    @patch('regcore_write.views.notice.db')
    def test_add_all_success(self, db):

        # Add a notice that applies to multiple parts
        url = '/notice/docdoc'
        notice = {'some': 'struct',
                  'cfr_parts': ['111', '222']}
        response = Client().put(url, content_type='application/json',
                                data=json.dumps(notice))

        # This should result in multiple calls to the put method
        calls = [
            call(u'docdoc', '111', 
                 {'some': 'struct', 'cfr_parts': ['111', '222']}),
            call(u'docdoc', '222', 
                 {'some': 'struct', 'cfr_parts': ['111', '222']}),
        ]
        self.assertTrue(db.Notices.return_value.put.called)
        db.Notices.return_value.put.assert_has_calls(
            calls, any_order=True)
