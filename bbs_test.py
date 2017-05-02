from bbs import app, db
import unittest

class TestBBS(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        db.create_all()

    def test_go_to_login(self): # ログインページに移動できるか
        response = self.app.get('/login')
        assert response.status_code == 200

    def test_go_to_signup(self): # サインアップページに移動できるか
        response = self.app.get('/signup')
        assert response.status_code == 200

    def test_can_not_go_to_root(self): # 認証情報なしでアクセスできないことを確認
        response = self.app.get('/')
        assert response.status_code != 200

    def test_signup(self): # サインアップして認証情報が得られているか確認
        self.signup(name = 'takumi', email = 'takumi@nara.com', password = 'password')
        #print(vars(response))
        #print(response.headers['Set-Cookie'])
        valid_signup = self.app.get('/')
        assert valid_signup.status_code == 200

    def test_login(self): # ログインして認証情報が得られているか確認
        response = self.login(email = 'takumi@nara.com', password = 'password')
        #print(vars(response))
        valid_login = self.app.get('/', headers = {'Set-Cookie': response.headers['Set-Cookie']}, follow_redirects = True)
        #print(vars(valid_login))
        assert valid_login.status_code == 200

    def test_go_to_new_thread(self): # 認証情報がある場合のみアクセス可
        self.login(email = 'takumi@nara.com', password = 'password')
        response = self.app.get('/thread/new', follow_redirects = True)
        assert response.status_code == 200

    def test_create_thread(self): # 認証情報がある場合のみスレッドの作成が可能
        self.login(email = 'takumi@nara.com', password = 'password')
        response = self.app.post('/thread', data = dict(title = 'test'), follow_redirects = True)
        assert response.status_code == 200

    def signup(self, name, email, password):
        return self.app.post('/signup', data = dict(
            name = name,
            email = email,
            password = password
        ), follow_redirects = False)

    def login(self, email, password):
        return self.app.post('/login', data = dict(
            email = email,
            password = password
        ), follow_redirects = False)

if __name__ == '__main__':
    unittest.main()
