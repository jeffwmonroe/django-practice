from django.test import TestCase
from django.urls import resolve, reverse
from ..views import board
from ..models import Board


class BoardTopicsTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='Django board.')

    def tearDown(self):
        pass

    def test_board_view_success_status_code(self):
        url = reverse('board', kwargs={'board_name': 'Django'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_board_view_not_found_status_code(self):
        url = reverse('board', args=["not there"])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_board_url_resolves_board_view(self):
        view = resolve('/boards/Jeff/')
        self.assertEquals(view.func, board)

    def test_board_view_contains_link_back_to_homepage(self):
        board_url = reverse('board', kwargs={'board_name': 'Django'})
        response = self.client.get(board_url)
        homepage_url = reverse('home')
        self.assertContains(response, 'href="{0}"'.format(homepage_url))

    def test_board_view_contains_navigation_links(self):
        board_url = reverse('board', kwargs={'board_name': 'Django'})
        homepage_url = reverse('home')
        new_topic_url = reverse('new_topic', kwargs={'board_name': 'Django'})

        response = self.client.get(board_url)

        self.assertContains(response, 'href="{0}"'.format(homepage_url))
        self.assertContains(response, 'href="{0}"'.format(new_topic_url))

