import sys
import os
sys.path.append(os.path.abspath('.'))
import requests
import unittest
from HTMLRunnerTest import HTMLTestRunner
headers = {}
headers['sign'] = 'f7bb1e66a6ebd2a8a065997d6c1f6a39'
# userdata = {}
# userdata['userAccount'] = '17600000024'
# userdata['password'] = 'DpO0f6Ei54Ev5FzbZRWbLw=='
# userdata['loginType'] = '2'
# userdata['source'] = 'pc'
# r = requests.post('https://www.biaoshitong.com/lmbj-api/user/appLogin.do',data=userdata,headers=headers)
# print(r.text)
# print(r.json())
# print(r.json()['data']['accessToken'])

def login(userAccount='17600000024',password='DpO0f6Ei54Ev5FzbZRWbLw==',loginType='2',source='pc'):
    userdata = {}
    userdata['userAccount'] = userAccount
    userdata['password'] = password
    userdata['loginType'] = loginType
    userdata['source'] = source
    r = requests.post('https://www.biaoshitong.com/lmbj-api/user/appLogin.do', data=userdata, headers=headers)
    # accessToken = r.json()['data']['accessToken']
    # print(r.json())
    # print(accessToken)
    return(r.json())

print(login())
print(login()['status'])
status1 = login()['status']
status2 = login(password='123456')['status']
print(login(password='123456'))



class Testlogin(unittest.TestCase):
    def tearDown(self):
        print("111")
    def setUp(self):
        print("2222")

    def test_login_success(self):
        self.assertEqual(status1,1)

    def test_login_failure(self):
        self.assertEqual(status2,0)


if __name__ == '__main__':
    testunit = unittest.TestSuite()
    testunit.addTest(Testlogin("test_login_success"))
    testunit.addTest(Testlogin("test_login_failure"))
    fp = open('./result.html','wb')
    runner = HTMLTestRunner(stream=fp,title='hetest',description='测试报告')
    runner.run(testunit)
    fp.close()

