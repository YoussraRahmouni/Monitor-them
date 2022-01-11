import unittest
from script1 import log_parsing

class TestStringMethods(unittest.TestCase):

    def test_parser1(self):
        template = '127.1.1.1 - - [09/Jan/2011:18:22:48 +0100] "GET / HTTP/1.1" 302 243 "-" "Mozilla/5.0 (X11; U; Linux i686; fr; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.04 (lucid) Firefox/3.6.13"'
        self.assertEqual(log_parsing(template)['remote_host'], '127.1.1.1')
        self.assertEqual(log_parsing(template)['status'], '302')
        self.assertEqual(log_parsing(template)['time_received'], '[09/Jan/2011:18:22:48 +0100]')
        self.assertEqual(log_parsing(template)['request_method'], 'GET')

    def test_parser2(self):
        template= 'localhost:80 127.0.0.1 - - [11/Jan/2022:09:50:01 +0100] "GET /wp-cron.php HTTP/1.1" 200 131 "-" "Mozilla/5.0'
        self.assertEqual(log_parsing(template)['remote_logname'], '127.0.0.1')
        self.assertEqual(log_parsing(template)['status'], '200')
        self.assertEqual(log_parsing(template)['time_received'], '[11/Jan/2022:09:50:01 +0100]')
        self.assertEqual(log_parsing(template)['request_method'], 'GET')

if __name__ == '__main__':
    unittest.main()
