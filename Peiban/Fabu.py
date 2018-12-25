import unittest
import requests,json
# import md5



class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.passurl='https://passport.17daxue.com/web-passport/user/login/newLogon?loginName=sigmajy3&password=123456'
        self.request=requests.get(url=self.passurl,headers={'Content-Type': 'application/json;charset=UTF-8'})
        self.response=self.request.json()
        # self.response = json.dumps(self.request.json(),indent=2,sort_keys=2,ensure_ascii=False)
        self.token = self.response['token']
        # print self.token
        self.host = 'https://sigma.17daxue.cn/web-sigma/api/v2/mathsGo/problem/publishProblem'
        self.boady = {"id": "150418", "publishStatus": 0}
        self.header =  {"Content-Type":"application/json",'X-Token': self.token,'Referer': 'http://cz.17daxue.com/'}
        self.requests = requests.post(url=self.host, data=json.dumps(self.boady),headers=self.header)




    def test_something(self):
        # print type(json.dumps(self.request.json(),indent=2,sort_keys=2,ensure_ascii=False))
        print (self.requests.text)
        # self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()

