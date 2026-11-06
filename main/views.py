from django.shortcuts import render, get_object_or_404
from .models import Article, Evenement

# Page d'accueil : liste tous les articles avec leurs images
def accueil(request):
    articles = Article.objects.all().order_by('-date_publication')
    return render(request, 'main/index.html', {'articles': articles})

# Page de détail : affiche un article complet sur une page dédiée
def detail_article(request, id):
    article = get_object_or_404(Article, id=id)
    return render(request, 'main/detail.html', {'article': article})


def liste_evenements(request):
    evenements = Evenement.objects.prefetch_related("images")
    return render(request, 'main/evenements.html', {'evenements': evenements})


def detail_evenement(request, id):
    evenement = get_object_or_404(
        Evenement.objects.prefetch_related("images"),
        id=id,
    )
    return render(request, 'main/evenement_detail.html', {'evenement': evenement})