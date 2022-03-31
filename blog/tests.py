from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post


class BlogPostTest(TestCase):
    # run for each test
    """def setUp(self):
        self.user = User.objects.create(username='ali')
        self.post1 = Post.objects.create(
            title='django',
            text='this is for test our blog',
            author=self.user,
            status=Post.STATUS_CHOICES[0][0],
        )
        self.post2 = Post.objects.create(
            title='test2',
            text='this is for test2',
            author=self.user,
            status=Post.STATUS_CHOICES[1][0]
        )"""
    # run just one time
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='ali')
        cls.post1 = Post.objects.create(
            title='django',
            text='this is for test our blog',
            author=cls.user,
            status=Post.STATUS_CHOICES[0][0],
        )
        cls.post2 = Post.objects.create(
            title='test2',
            text='this is for test2',
            author=cls.user,
            status=Post.STATUS_CHOICES[1][0]
        )

    def test_post_model_str(self):
        post = self.post1
        self.assertEqual(str(post), post.title)

    def test_post_list_detail(self):
        self.assertEqual(self.post1.title, 'django')
        self.assertEqual(self.post1.text, 'this is for test our blog')

    def test_post_list_url(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

    def test_post_list_url_by_name(self):
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)

    def test_post_title_on_blog_list_page(self):
        response = self.client.get(reverse('post_list'))
        self.assertContains(response, self.post1.title)

    def test_post_detail_url(self):
        response = self.client.get('/blog/1', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_post_detail_by_name(self):
        response = self.client.get(reverse('post_detail', args=[self.post1.id]))
        self.assertEqual(response.status_code, 200)

    def test_post_detail_on_blog_detail_page(self):
        response = self.client.get(reverse('post_detail', args=[self.post1.id]))
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post1.text)

    def test_status_404_if_post_id_not_exist(self):
        response = self.client.get(reverse('post_detail', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_draft_post_not_show_in_post_list(self):  # TDD
        response = self.client.get(reverse('post_list'))
        self.assertContains(response, self.post1.title)
        self.assertNotContains(response, self.post2.title)

    def test_post_create_view(self):
        response = self.client.post(reverse('post_create'), {
            'title': 'test title',
            'text': 'test for creating an object in db',
            'status': 'pub',
            'author': self.user.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'test title')
        self.assertEqual(Post.objects.last().text, 'test for creating an object in db')

    def test_post_update_view(self):
        response = self.client.post(reverse('post_update', args=[self.post2.id], ), {
            'title': 'test2 update',
            'text': 'updating of post2',
            'status': 'pub',
            'author': self.user.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'test2 update')
        self.assertEqual(Post.objects.last().text, 'updating of post2')

    def test_post_delete_view(self):
        response = self.client.post(reverse('post_delete', args=[self.post2.id]))
        self.assertEqual(response.status_code, 302)
