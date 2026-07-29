import uuid
from django.db import models
from django.conf import settings
from django.utils.text import slugify

class BlogCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, unique=True, blank=True)

    class Meta:
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class BlogTag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, unique=True, blank=True)

    class Meta:
        verbose_name = "Blog Tag"
        verbose_name_plural = "Blog Tags"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, related_name='posts')
    tags = models.ManyToManyField(BlogTag, related_name='posts', blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    summary = models.TextField()
    content = models.TextField(help_text="Markdown support enabled")
    read_time_minutes = models.IntegerField(default=5)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # SEO & Schema Automation Fields
    meta_title = models.CharField(max_length=255, blank=True, help_text="Optional SEO Title override")
    meta_description = models.TextField(blank=True, help_text="Optional SEO Meta Description override")
    meta_keywords = models.TextField(blank=True, help_text="Comma-separated keywords")
    focus_keyword = models.CharField(max_length=255, blank=True, help_text="Primary keyword targeted for optimization")
    seo_score = models.IntegerField(default=0, help_text="Automated SEO readability/health score (0-100)")
    canonical_url = models.URLField(max_length=500, blank=True, help_text="Custom canonical link override if needed")
    og_image = models.ImageField(upload_to='blog/og/', blank=True, null=True, help_text="Social sharing Open Graph image override")

    class Meta:
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
        ordering = ['-published_at', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        if not self.meta_title:
            self.meta_title = self.title

        if not self.meta_description:
            self.meta_description = self.summary[:160] if len(self.summary) > 160 else self.summary

        if not self.focus_keyword:
            words = self.title.split()
            self.focus_keyword = words[-1].lower().strip(".,;:!?\"'") if words else "technology"

        if not self.meta_keywords:
            self.meta_keywords = f"blueshore technologies, {self.category.name.lower()}, {self.focus_keyword}"

        if not self.canonical_url:
            self.canonical_url = f"https://www.blueshoretech.com/blog/{self.slug}/"

        # Calculate dynamic seo_score if it is 0 or below passing mark
        if not self.seo_score or self.seo_score < 70:
            score = 70  # base passing score

            # 1. Focus keyword in title
            if self.focus_keyword.lower() in self.title.lower():
                score += 10

            # 2. Focus keyword in content
            if self.focus_keyword.lower() in self.content.lower():
                score += 10

            # 3. Headers present (markdown ## or #)
            if '##' in self.content or '#' in self.content:
                score += 5

            # 4. Length check
            if len(self.content.split()) > 300:
                score += 5

            self.seo_score = min(100, score)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class AuthorProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_profile')
    role = models.CharField(max_length=100, blank=True, help_text="e.g. Co-Founder & Director")
    expertise = models.CharField(max_length=255, blank=True, help_text="e.g. Enterprise Software Architect")
    linkedin_url = models.URLField(blank=True, help_text="Full LinkedIn profile URL")
    github_url = models.URLField(blank=True, help_text="Full GitHub profile URL")
    twitter_url = models.URLField(blank=True, help_text="Full X/Twitter profile URL")
    organization = models.CharField(max_length=255, default="Blueshore Technologies")
    bio = models.TextField(blank=True, help_text="Author biography")
    avatar = models.ImageField(upload_to='authors/', blank=True, null=True)

    @property
    def slug(self):
        username = self.user.username.lower()
        if username == 'abhishek':
            return 'abhishek-kashyap'
        elif username == 'ashish':
            return 'ashish-kushwaha'
        from django.utils.text import slugify
        return slugify(username)

    @property
    def profile_url(self):
        return f"/authors/{self.slug}/"

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.role})"

