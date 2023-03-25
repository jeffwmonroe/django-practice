from django.test import TestCase
from django.urls import resolve, reverse
from ..views import new_topic
from ..models import Board, Topic, Post
from django.contrib.auth.models import User
from ..forms import NewTopicForm


# Create your tests here.


class NewTopicTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='Django board.')
        User.objects.create_user(username='john', email='john@doe.com',
                                 password='123')  # <- included this line here
        self.client.login(username='john', password='123')

    def test_new_topic_view_success_status_code(self):
        url = reverse('new_topic', kwargs={'board_name': 'Django'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_topic_view_not_found_status_code(self):
        url = reverse('new_topic', kwargs={'board_name': 'Django unfound'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_new_topic_url_resolves_new_topic_view(self):
        view = resolve('/boards/1/new/')
        self.assertEquals(view.func, new_topic)

    def test_new_topic_view_contains_link_back_to_board_view(self):
        new_topic_url = reverse('new_topic', kwargs={'board_name': 'Django'})
        board_url = reverse('board', kwargs={'board_name': 'Django'})
        response = self.client.get(new_topic_url)
        self.assertContains(response, 'href="{0}"'.format(board_url))

    def test_csrf(self):
        url = reverse('new_topic', kwargs={'board_name': 'Django'})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_topic_valid_post_data(self):
        url = reverse('new_topic', kwargs={'board_name': 'Django'})
        data = {
            'subject': 'Test title',
            'message': 'Lorem ipsum dolor sit amet'
        }
        response = self.client.post(url, data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())

    def test_new_topic_invalid_post_data_empty_fields(self):
        """
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        """
        url = reverse('new_topic', kwargs={'board_name': 'Django'})
        data = {
            'subject': '',
            'message': ''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())

    def test_contains_form(self):  # <- new test
        url = reverse('new_topic', kwargs={'board_name': 'Django'})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewTopicForm)

    def test_new_topic_invalid_post_data(self):  # <- updated this one
        """
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        """
        url = reverse('new_topic', kwargs={'board_name': 'Django'})
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

class LoginRequiredNewTopicTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='Django board.')
        self.url = reverse('new_topic', kwargs={'board_name': 'Django'})
        self.response = self.client.get(self.url)

    def test_redirection(self):
        login_url = reverse('login')
        self.assertRedirects(self.response,
                             '{login_url}?next={url}'.format(login_url=login_url, url=self.url))

    def test_new_topics_protected(self):  # <- new test
        url = reverse('new_topic', kwargs={'board_name': 'Django'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)


