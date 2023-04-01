# python -m unittest discover -p '*_dam.py'
from unittest.mock import MagicMock
import unittest

from yourmeals.data_access.data_access_module import DataAccessModule as DAM
from yourmeals.data_access.model.user import User


class TestDataAccessModule(unittest.TestCase):
    def setUp(self):
        self.user = User(
            email='test@example.com',
            name='Test User',
            age=30,
            weight=70,
            height=180,
            gender='man',
            strategy='loss',
        )

    def test_save_user(self):   
        data_access = DAM()
        data_access.save_user = MagicMock()
        data_access.save_user(self.user)
        
    def test_update_user(self):
        data_access = DAM()
        data_access.update_user = MagicMock(return_value=True)
            
        self.assertTrue(data_access.update_user())
        
    def test_get_user(self):
        orm_user = MagicMock(
            email='test@example.com',
            name='Test User',
            age=30,
            weight=70,
            height=180,
            gender='man',
            strategy='loss',
        )
        data_access = DAM()
        data_access.get_user = MagicMock(return_value=orm_user)
        user = data_access.get_user()
        self.assertEqual(user.email, orm_user.email)
        self.assertEqual(user.name, orm_user.name)
        self.assertEqual(user.age, orm_user.age)
        self.assertEqual(user.weight, orm_user.weight)
        self.assertEqual(user.height, orm_user.height)
        self.assertEqual(user.gender, orm_user.gender)
        self.assertEqual(user.strategy, orm_user.strategy)
