from django.shortcuts import render
from apps.portfolio.models import PortfolioProject

def portfolio_view(request):
    projects = PortfolioProject.objects.filter(is_published=True)
    return render(request, 'portfolio.html', {'projects': projects})
