from django.shortcuts import render, get_object_or_404
from apps.blog.models import BlogPost, BlogCategory, BlogTag

def blog_view(request):
    posts = BlogPost.objects.filter(is_published=True)
    categories = BlogCategory.objects.all()
    tags = BlogTag.objects.all()

    # Category filter
    category_slug = request.GET.get('category')
    if category_slug:
        posts = posts.filter(category__slug=category_slug)

    # Tag filter
    tag_slug = request.GET.get('tag')
    if tag_slug:
        posts = posts.filter(tags__slug=tag_slug)

    # Search filter
    search_query = request.GET.get('q')
    if search_query:
        posts = posts.filter(title__icontains=search_query) | posts.filter(content__icontains=search_query)

    # Featured posts vs regular posts
    featured_posts = posts.filter(is_featured=True)
    regular_posts = posts.filter(is_featured=False)

    context = {
        'posts': posts,
        'featured_posts': featured_posts,
        'regular_posts': regular_posts,
        'categories': categories,
        'tags': tags,
        'selected_category': category_slug,
        'selected_tag': tag_slug,
        'search_query': search_query,
    }
    return render(request, 'blog.html', context)

def blog_detail_view(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    # Fetch related posts in the same category (excluding current post)
    related_posts = BlogPost.objects.filter(category=post.category, is_published=True).exclude(id=post.id)[:3]
    
    context = {
        'post': post,
        'related_posts': related_posts,
    }
    return render(request, 'blog_detail.html', context)

def author_detail_view(request, slug):
    username_map = {
        'abhishek-kashyap': 'abhishek',
        'ashish-kushwaha': 'ashish',
    }
    username = username_map.get(slug.lower())
    if not username:
        username = slug.split('-')[0].lower()
        
    from apps.blog.models import AuthorProfile
    profile = get_object_or_404(AuthorProfile, user__username=username)
    posts = BlogPost.objects.filter(author=profile.user, is_published=True)
    
    context = {
        'profile': profile,
        'posts': posts,
    }
    return render(request, 'author_detail.html', context)
