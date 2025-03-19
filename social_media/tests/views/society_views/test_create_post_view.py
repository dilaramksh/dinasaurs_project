from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import resolve_url
from social_media.models import Post
from social_media.forms import PostForm

class CreatePostViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.url = reverse('create_post')

    def test_create_post_view_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f'/accounts/login/?next={self.url}')

    def test_create_post_view_post_valid_data(self):
        self.client.login(username='testuser', password='password123')
        post_data = {'title': 'Test Post', 'content': 'This is a test post.'}

        response = self.client.post(self.url, post_data)

        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.first()
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.content, 'This is a test post.')
        self.assertEqual(post.author, self.user)

        self.assertContains(response, 'Post created successfully!')
        self.assertRedirects(response, reverse('society_dashboard'))

    def test_create_post_view_post_invalid_data(self):
        self.client.login(username='testuser', password='password123')
        post_data = {'title': '', 'content': ''}

        response = self.client.post(self.url, post_data)

        self.assertFormError(response, 'form', 'title', 'This field is required.')
        self.assertFormError(response, 'form', 'content', 'This field is required.')

        self.assertContains(response, 'Create a New Post')
        self.assertContains(response, 'Submit')

    def test_create_post_view_post_redirects_on_valid_data(self):
        self.client.login(username='testuser', password='password123')
        post_data = {'title': 'Test Post', 'content': 'This is a valid test post.'}

        response = self.client.post(self.url, post_data)

        self.assertRedirects(response, reverse('society_dashboard'))

    def test_create_post_view_logged_in_user_can_see_their_posts(self):
        self.client.login(username='testuser', password='password123')
        post_data = {'title': 'Test Post', 'content': 'This is a test post.'}
        self.client.post(self.url, post_data)

        response = self.client.get(self.url)

        self.assertContains(response, 'Your Posts')
        self.assertContains(response, 'Test Post')
        self.assertContains(response, 'This is a test post.')

    def test_create_post_view_invalid_post_data(self):
        self.client.login(username='testuser', password='password123')
        post_data = {'title': '', 'content': ''}

        response = self.client.post(self.url, post_data)

        self.assertFormError(response, 'form', 'title', 'This field is required.')
        self.assertFormError(response, 'form', 'content', 'This field is required.')
