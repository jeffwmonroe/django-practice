from django.test import TestCase
from django.urls import resolve, reverse
from ..views import home
from ..models import Board


class HomeTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django board.')
        url = reverse('home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)

    def test_home_view_contains_link_to_topics_page(self):
        board_url = reverse('board', kwargs={'board_name': 'Django'})
        self.assertContains(self.response, 'href="{0}"'.format(board_url))

