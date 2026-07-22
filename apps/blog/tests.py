from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.blog.models import BlogCategory, BlogTag, BlogPost

class BlogModelTest(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(username="author", password="pass")
        self.cat = BlogCategory.objects.create(name="AI & Automation")
        self.tag = BlogTag.objects.create(name="Python")

    def test_category_and_tag_slugs(self):
        self.assertEqual(self.cat.slug, "ai-automation")
        self.assertEqual(self.tag.slug, "python")
        self.assertEqual(str(self.cat), "AI & Automation")
        self.assertEqual(str(self.tag), "Python")

    def test_blog_post_creation(self):
        post = BlogPost.objects.create(
            title="The Future of AI Systems",
            category=self.cat,
            author=self.user,
            summary="Intro to AI systems.",
            content="Full markdown content.",
            is_published=True
        )
        post.tags.add(self.tag)
        self.assertEqual(post.slug, "the-future-of-ai-systems")
        self.assertEqual(post.tags.first(), self.tag)
        self.assertEqual(str(post), "The Future of AI Systems")

class BlogViewTest(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(username="writer", password="pass")
        self.cat = BlogCategory.objects.create(name="Business Tech")
        self.post = BlogPost.objects.create(
            title="Business Tech Insights 2026",
            category=self.cat,
            author=self.user,
            summary="A summary.",
            content="Some text.",
            is_published=True
        )

    def test_blog_list_view(self):
        url = reverse('blog')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Business Tech Insights 2026")

    def test_blog_detail_view(self):
        url = reverse('blog-detail', kwargs={'slug': self.post.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Business Tech Insights 2026")
        self.assertContains(response, "Some text.")
