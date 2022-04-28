from django.test import TestCase, Client
from bs4 import BeautifulSoup
from blog.models import Post


class TestView(TestCase):
    def setup(self):
        self.client = Client()

    def text_post_list(self):
        # 1.1
        response = self.client.get('blog/')
        # 1.2
        self.assertEqual(response.status_code, 200)
        # 1.3
        soup = BeautifulSoup(response.content, 'html.parse')
        self.assertEqual(soup.title.text, 'Blog')
        # 1.4
        navbar = soup.nav
        # 1.5
        self.assertin('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

        # 2.1
        self.assertEqual(Post.objects.count(), 0)
        # 2.2
        main_area = soup.find('div',id='main_area')
        self.assertIn('아직 게시물이 없습니다', main_area.text)

        # 3.1
        post_001 = Post.objects.create(
            title='첫번째 포스트입니다.',
            content='Hello World. We are the world.',
        )
        post_002 = Post.objects.create(
            title='두번째 포스트입니다.',
            content='1등이 전부는 아니잖아요?',
        )
        self.assertEqual(Post.objects.count(), 2)

        # 3.2
        response = self.client.get('blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(response.status_code, 200)
        # 3.3
        main_area = soup.find('div', id='main-area')
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)
        # 3.4
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)

