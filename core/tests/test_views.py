from .test_setup import TestSetUp
from core.models import User


class TestViews(TestSetUp):
  
  def test_user_cannot_register_without_data(self):
    res = self.client.post(self.register_url)
    # import pdb
    # pdb.set_trace()
    self.assertEqual(res.status_code, 400)
    
  def test_user_can_register_with_correct_data(self):
    res = self.client.post(self.register_url, self.user_data, format="json")
    # import pdb
    # pdb.set_trace()
    self.assertEqual(res.data['email'], self.user_data['email'])
    self.assertEqual(res.data['username'], self.user_data['username'])
    self.assertEqual(res.status_code, 201)
    
  def test_user_cannot_login_with_unverified_email(self):
    self.client.post(self.register_url, self.user_data, format="json")
    res = self.client.post(self.login_url, self.user_data, format="json")
    self.assertEqual(res.status_code, 401)
    
  def test_user_can_login_with_verified_email(self):
    response = self.client.post(self.register_url, self.user_data, format="json")
    email = response.data['email']
    user = User.objects.get(email=email)
    user.is_verified = True
    user.save()
    res = self.client.post(self.login_url, self.user_data, format="json")
    self.assertEqual(res.status_code, 200)
  