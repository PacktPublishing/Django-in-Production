from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.utils import timezone
from django.test import tag

from freezegun import freeze_time

from blog.factoryboy import BlogFactory, AuthorFactory
from blog import public

#
class BasicTests(APITestCase):
    def test_basic_req(self):
        """
        Test the basic url path response.
        """
        # ARRANGE-Create a reverse URL and expected response.
        url = '/blog/hello-world/'

        expected_data = {"msg": "hello world!"}
        # ACT – Perform API call by DRF’s test APIClient.
        response = self.client.get(url, format='json')

        # ASSERT- Verify the response.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)


class BasicTests2(APITestCase):
    def test_unauthenticated_req(self):
        url = '/blog/hello-world-2/'
        response = self.client.get(url, format='json')

        # Since the user is not logged in it would get 401.
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_req(self):
        url = '/blog/hello-world-2/'
        expected_data = {"msg": "hello world!"}
        # Create a user and get the token. This is important.
        user = User.objects.create_user(username='demouser', password='demopass')
        token, created = Token.objects.get_or_create(user=user)

        # Login to the request using the HTTP header token.
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        response = self.client.get(url, format='json')

        # User is logged in we would get the expected 200 response code.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_wrong_authenticated_req(self):
        url = '/blog/hello-world-2/'

        # Login to the request using a random wrong token.
        self.client.credentials(HTTP_AUTHORIZATION=f'Token random')
        response = self.client.get(url, format='json')

        # Request has the wrong token so it would get 401.
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_force_authenticate_with_user(self):
        """
        Setting `.force_authenticate()` with a user forcibly authenticates.
        """
        u1 = User.objects.create_user('a1', 'a1@abc.co')
        url = '/blog/hello-world/'

        # Forcefully login and update request.user
        self.client.force_authenticate(user=u1)
        response = self.client.get(url)
        expected_data = {"msg": "hello world!"}
        # Tests work with the login user.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)


class BasicTests3(APITestCase):

    def setUp(self):
        self.url = '/blog/hello-world/'
        user = User.objects.create_user('a1', 'a1@abc.co')
        self.client.force_authenticate(user=user)
        print('Running Setup')

    def test_with_setup_authenticated_req(self):
        print('test 1 running')
        expected_data = {"msg": "hello world!"}
        response = self.client.get(self.url, format='json')

        # User is logged in, expected 200 response code.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

        # demo test

    def test_demo(self):
        print('test 2 running')
        self.assertEqual(1, 1)

    def tearDown(self):
        self.client.logout()
        print('Running teardown')


class BlogTestCase4(APITestCase):

    def test_total_blogs(self):
        blogs = BlogFactory.create_batch(4)
        url = '/blog/unpaginated/'

        resp = self.client.get(url, format='json')

        self.assertEqual(len(resp.data['blogs']), 4)


class BlogTestCase5(APITestCase):
    def setUp(self):
        self.blog = BlogFactory(title='a1', content='a b c')
        print('Running Setup multiple times')

    def test_word_count_1(self):
        expected_count = 3
        print('test_word_count_1 running')
        self.assertEqual(expected_count, 3)

    def test_title_length_1(self):
        expected_length = 2
        print('test_title_length_1 running')
        self.assertEqual(expected_length, 2)


class BlogTestCase6(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.blog = BlogFactory(title='a1', content='a b c')
        print('Running Setup only once')

    def test_word_count_2(self):
        expected_count = 3
        print('test_word_count_2 running')
        self.assertEqual(expected_count, 3)

    def test_title_length_2(self):
        expected_length = 2
        print('test_title_length_2 running')
        self.assertEqual(expected_length, 2)


class BlogTests7(APITestCase):
    def test_blog_time_block(self):
        today = timezone.now().date()
        tomo = timezone.now().date() + timezone.timedelta(days=1)

        with freeze_time(today) as frozentime:
            # Post 10 blogs
            author = AuthorFactory()
            create_10_blogs = BlogFactory.create_batch(10, author=author)
            # Check if the user can post more blogs today
            user_can_post = public.check_if_allowed_to_publish_blog(author)
            # Validate that the user cannot post a blog today.
            self.assertFalse(user_can_post)

            # Move the date to the next day
            frozentime.move_to(tomo)
            # Validate that the user cannot post a blog tomorrow.
            result = public.check_if_allowed_to_publish_blog(author)
            self.assertTrue(result)


class BlogTests8(APITestCase):
    @tag("fast")
    def test_fast(self):
        print("fast test running")

    @tag("slow")
    def test_slow(self):
        print("slow test running")

    @tag("slow", "core")
    def test_slow_but_core(self):
        print("slow but core test running")