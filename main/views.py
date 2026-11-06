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


def histoire(request):
    return render(request, 'main/histoire.html')


def galerie(request):
    photos = [
        {
            "fichier": "evenements/FLEUVE_GAMBIE.jpg",
            "titre": "Le fleuve Gambie",
            "description": "Un paysage emblématique de la région de Kédougou.",
        },
        {
            "fichier": "evenements/Cascade_dindefelo_2.jpg",
            "titre": "La cascade de Dindéfélo",
            "description": "Un site naturel remarquable de la région.",
        },
        {
            "fichier": "evenements/Kedougou_Region_Senegal.jpg",
            "titre": "Kédougou et ses paysages",
            "description": "Une image pour découvrir le territoire de Kédougou.",
        },
        {
            "fichier": "evenements/bassari1.jpg",
            "titre": "Culture bassari",
            "description": "Une scène de vie culturelle à Kédougou.",
        },
        {
            "fichier": "evenements/bassari2.jpg",
            "titre": "Traditions de Kédougou",
            "description": "Les cultures locales font la richesse du territoire.",
        },
        {
            "fichier": "evenements/bassari3.jpg",
            "titre": "Rencontres culturelles",
            "description": "Un aperçu des traditions et des rencontres de la région.",
        },
        {
            "fichier": "evenements/NAVETANE1.jpg",
            "titre": "Le Navétane",
            "description": "Un moment de sport et de rassemblement.",
        },
        {
            "fichier": "evenements/NAVETANE2.jpg",
            "titre": "Sport et vie locale",
            "description": "Les activités sportives réunissent les habitants.",
        },
        {
            "fichier": "evenements/NAVETANE3.jpg",
            "titre": "Rencontres sportives",
            "description": "La vie locale en images.",
        },
    ]
    return render(request, 'main/galerie.html', {'photos': photos})


def informations_pratiques(request):
    return render(request, 'main/informations_pratiques.html')


def contact(request):
    return render(request, 'main/contact.html')