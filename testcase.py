import unittest
import mock

import scheduler

class Testscheduler(unittest.TestCase):
    def setUp(self):
        pass
    
    @mock.patch('scheduler.scrape_proxies')
    @mock.patch('scheduler.myproxy')
    @mock.patch('scheduler.voter')    
    def test_run(self,mock_getproxies, mock_proxy, mock_voter):
        mock_proxy.proxy_nums.return_value = 26
        #mock_proxy.get_one_proxy.return_value = {"protocol":"http", "ip":"183.207.228.9","port":80}
        mock_proxy.get_one_proxy.return_value = {}
        scheduler.run()

if __name__ == "__main__":
    unittest.main()