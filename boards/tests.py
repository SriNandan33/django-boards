from django.contrib.auth.models import User
from django.urls import reverse, resolve
from django.test import TestCase
from .models import Board, Topic, Post
from .views import home, board_topics, new_topic
from .forms import NewTopicForm

class HomeTests(TestCase):
	def setUp(self):
		self.board = Board.objects.create(name='Django', description='django discussion board')
		url = reverse('home')
		self.response = self.client.get(url)

	def test_home_view_status_code(self):
		self.assertEquals(self.response.status_code, 200)

	def test_home_url_resolves_home_view(self):
		view = resolve('/')
		self.assertEquals(view.func, home)

	def test_home_view_contains_link_to_topics_page(self):
		board_topics_url = reverse('board_topics', kwargs={'pk': self.board.pk})
		self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))


class BoardTopicTests(TestCase):
	def setUp(self):
		Board.objects.create(name='Django', description='Django discussion Board')

	def test_board_topics_view_success_status_code(self):
		url = reverse('board_topics', kwargs={'pk': 1})
		response = self.client.get(url)
		self.assertEquals(response.status_code, 200)

	def test_board_topics_view_not_found_status_code(self):
		url = reverse('board_topics', kwargs={'pk': 9999})
		response = self.client.get(url)
		self.assertEquals(response.status_code, 404)

	def test_board_topics_url_resolves_board_topics_view(self):
		view = resolve('/boards/1/')
		self.assertEquals(view.func, board_topics)

	def test_board_topics_view_contains_navigation_links(self):
		board_topics_url = reverse('board_topics', kwargs={'pk': 1})
		response = self.client.get(board_topics_url)
		home_page_url = reverse('home')
		new_topic_url = reverse('new_topic', kwargs={'pk': 1})
		self.assertContains(response, 'href="{0}"'.format(home_page_url))
		self.assertContains(response, 'href="{0}"'.format(new_topic_url))


class newTopicTests(TestCase):
	def setUp(self):
		self.board = Board.objects.create(name='Django', description='Django discussion board')
		self.user = User.objects.create_user(username='Nandu', email='jhon@gmail.com', password='nandu12345')


	def test_new_topic_view_success_status_code(self):
		url = reverse('new_topic', kwargs={'pk': self.board.pk})
		response = self.client.get(url)
		self.assertEquals(response.status_code, 200)

	def test_new_topic_view_not_found_status_code(self):
		url = reverse('new_topic', kwargs={'pk': 999})
		response = self.client.get(url)
		self.assertEquals(response.status_code, 404)

	def test_new_topic_url_resolves_new_topic_view(self):
		view = resolve('/boards/{0}/new/'.format(self.board.pk))
		self.assertEquals(view.func, new_topic)

	def test_new_topic_view_contains_link_to_board_topics_view(self):
		new_topic_url = reverse('new_topic', kwargs={'pk': self.board.pk})
		board_topics_url = reverse('board_topics', kwargs={'pk': self.board.pk})
		response = self.client.get(new_topic_url)
		self.assertContains(response, 'href="{0}"'.format(board_topics_url))

	def test_csrf(self):
		url = reverse('new_topic', kwargs={'pk': 1})
		response = self.client.get(url)
		self.assertContains(response, 'csrfmiddlewaretoken')

	def test_new_topic_valid_post_data(self):
		url = reverse('new_topic', kwargs={'pk':1})
		data = {
			'subject': 'Learn Django',
			'message': 'learning Django'
		}
		response = self.client.post(url, data)
		self.assertTrue(Topic.objects.exists())
		self.assertTrue(Post.objects.exists())
		self.assertEquals(response.status_code, 302)

	def test_new_topic_invalid_post_data(self):
		url = reverse('new_topic', kwargs={'pk': 1})
		response = self.client.post(url, {})
		form = response.context.get('form')
		self.assertEquals(response.status_code, 200)
		self.assertTrue(form.errors)

	def test_new_topic_invalid_post_data_empty_fields(self):
		url = reverse('new_topic', kwargs={'pk': 1})
		data = {
			'subject': '',
			'message': ''
		}
		response = self.client.post(url, data)
		self.assertEquals(response.status_code, 200)
		self.assertFalse(Topic.objects.exists())
		self.assertFalse(Post.objects.exists())

	def test_contains_form(self):
		url = reverse('new_topic', kwargs={'pk':1})
		response = self.client.get(url)
		form = response.context.get('form')
		self.assertIsInstance(form, NewTopicForm)