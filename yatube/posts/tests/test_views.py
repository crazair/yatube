from django import forms
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post, User


class PostPagesTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_author = User.objects.create_user(username='TestAuthor')
        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user_author,
            group=cls.group,
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='HasNoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.author_client = Client()
        self.author_client.force_login(self.user_author)

    def test_pages_uses_correct_template_all_users(self):
        """URL-адрес использует соответствующий шаблон.(posts)."""
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:profile', kwargs={'username': self.user_author}):
                'posts/profile.html',
            reverse('posts:post_detail', kwargs={'post_id': self.post.id}):
                'posts/post_detail.html',
            reverse('posts:group_list', kwargs={'slug': self.group.slug}):
                'posts/group_list.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}):
                'posts/create_post.html',
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.author_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.author_client.get(reverse('posts:index'))
        self.assertEqual(
            response.context['page_obj'].object_list[0], self.post)

    def test_group_list_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = (self.author_client.get(
                    reverse('posts:group_list',
                            kwargs={'slug': self.group.slug})))
        self.assertEqual(response.context.get('group'), self.group)

    def test_profile_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = (self.author_client.get(
                    reverse('posts:profile',
                            kwargs={'username': self.post.author})))
        self.assertEqual(response.context.get('author'), self.user_author)

    def test_post_detail_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контестом."""
        response = (self.author_client.get(
                    reverse('posts:post_detail',
                            kwargs={'post_id': self.post.id})))
        self.assertEqual(response.context.get('post'), self.post)

    def test_create_post_show_correct_context(self):
        """Шаблон create_post сформирован с правильным контекстом."""
        response = (self.author_client.get(reverse('posts:post_create')))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_create_post_show_correct_context_in_edit(self):
        """Шаблон create_post сформирован с правильным контекстом
        при редактировании поста."""
        response = (self.author_client.get(
                    reverse('posts:post_edit',
                            kwargs={'post_id': self.post.id})))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_check_post_on_create(self):
        """Проверка, что пост правильно добавляется на страницы."""
        pages = {
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': self.group.slug}),
            reverse('posts:profile', kwargs={'username': self.user_author}),
        }
        for address in pages:
            with self.subTest(address=address):
                response = self.author_client.get(address)
                self.assertEquals(response.context.get('page_obj')[0],
                                  self.post)


class PostViewPaginatorTests(TestCase):
    """Тест пагинатора приложения posts."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.COUNT_TEST_POST = 13
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test',
            description='Тестовое описание')
        for i in range(cls.COUNT_TEST_POST):
            Post.objects.create(
                author=cls.user,
                group=cls.group,
                text=f'{i}'
            )

    def setUp(self):
        """Создаем авторизованного пользователя."""
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_views_context(self):
        """Шаблоны сформирован с правильным пагинатором."""
        remains_post_count = Post.objects.count() - 10
        urls = [
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': self.group.slug}),
            reverse('posts:profile',
                    kwargs={'username': self.user.username})
        ]

        for url in urls:
            with self.subTest(url=url):
                response_1 = self.authorized_client.get(url)
                response_2 = self.authorized_client.get(
                    url + '?page=2')
                self.assertEqual(
                    len(response_1.context['page_obj']), 10)
                self.assertEqual(
                    len(response_2.context['page_obj']),
                    remains_post_count)
