from django.test import TestCase
from django.contrib.auth.models import User

class UserRegistrationTest(TestCase):
    def test_user_registration(self):
        # Create a new user
        password = 'test_password'
        first_name = 'test_first'
        last_name = 'test_last'
        email = 'test_email'
        phone_number = 'test_phone'
        User.objects.register(password=password, first_name=first_name, last_name=last_name, email=email, phone_number=phone_number)
        
        # Check if the user was created successfully
        self.assertTrue(User.objects.filter(username=username).exists())


class ExpenseCreationTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.register(password=password, first_name=first_name, last_name=last_name, email=email, phone_number=phone_number)
        
    def test_add_expense(self):
        # Create an expense
        Expense.objects.create(
            description='Test Expense',
            amount=50.00,
            user=self.user,
        )
        
        # Check if the expense was created successfully
        self.assertTrue(Expense.objects.filter(description='Test Expense').exists())

class GroupManagementTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='test_user', password='test_password')

    def test_create_group(self):
        # Create a group
        group = Group.objects.create(name='Test Group')
        
        # Add user to the group
        group.members.add(self.user)
        
        # Check if the group was created successfully
        self.assertTrue(Group.objects.filter(name='Test Group').exists())

    def test_group_membership(self):
        # Create a group
        group = Group.objects.create(name='Test Group')
        
        # Add user to the group
        group.members.add(self.user)
        
        # Retrieve the group's members
        group_members = group.members.all()
        
        # Check if the user is a member of the group
        self.assertIn(self.user, group_members)

