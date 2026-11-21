from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse


class AccountsAuthenticationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.fo_group = Group.objects.create(name='Field Officer')
        self.admin_group = Group.objects.create(name='Administrator')
        self.sup_group = Group.objects.create(name='Supervisor')
        self.read_group = Group.objects.create(name='Read-only User')

        self.officer = User.objects.create_user(
            username='officer_test',
            password='TestPassword123!'
        )
        self.officer.groups.add(self.fo_group)

        self.admin = User.objects.create_user(
            username='admin_test',
            password='TestPassword123!',
            is_staff=True
        )
        self.admin.groups.add(self.admin_group)

    def test_at01_anonymous_user_redirected_from_dashboard(self):
        """AT-01: Anonymous user opens /dashboard/ -> redirected to login; no protected data shown."""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_at02_valid_user_login_and_logout(self):
        """AT-02: Valid user logs in and logs out. Session starts and ends; protected routes require login."""
        # 1. Login with valid credentials
        login_resp = self.client.post(reverse('login'), {
            'username': 'officer_test',
            'password': 'TestPassword123!'
        })
        self.assertEqual(login_resp.status_code, 302)

        # Dashboard accessible after login
        dash_resp = self.client.get(reverse('dashboard'))
        self.assertEqual(dash_resp.status_code, 200)
        self.assertContains(dash_resp, "Forensic Operations Dashboard")

        # 2. Logout via POST
        logout_resp = self.client.post(reverse('logout'))
        self.assertEqual(logout_resp.status_code, 302)

        # Dashboard is no longer accessible
        post_logout_resp = self.client.get(reverse('dashboard'))
        self.assertEqual(post_logout_resp.status_code, 302)
        self.assertIn(reverse('login'), post_logout_resp.url)

    def test_at03_field_officer_blocked_from_admin_user_management(self):
        """AT-03: Field Officer attempts admin-only user management -> Access denied (403 or safe redirect)."""
        self.client.login(username='officer_test', password='TestPassword123!')
        response = self.client.get(reverse('user_list'))
        # Should return 403 PermissionDenied
        self.assertEqual(response.status_code, 403)

    def test_admin_can_access_user_management(self):
        """Verify Administrator can access user management."""
        self.client.login(username='admin_test', password='TestPassword123!')
        response = self.client.get(reverse('user_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "User Account &amp; Role Governance")
