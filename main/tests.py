from pathlib import Path
from tempfile import TemporaryDirectory

from django.contrib.auth import get_user_model
from django.contrib.staticfiles import finders
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test.utils import override_settings
from django.urls import reverse

from .models import Article, Evenement, ImageEvenement


class ArticlePagesTests(TestCase):
    def setUp(self):
        self.article = Article.objects.create(
            titre="Actualité du village",
            contenu="Une nouvelle importante pour le village.",
            image="https://example.com/village.jpg",
        )

    def test_accueil_displays_article_and_detail_link(self):
        response = self.client.get(reverse("accueil"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<title>Kédougou, terre des hommes - Accueil</title>", html=True)
        self.assertContains(response, "Kédougou, terre des hommes")
        self.assertContains(response, "Terre des hommes")
        self.assertContains(response, self.article.titre)
        self.assertContains(
            response,
            reverse("detail_article", args=[self.article.id]),
        )
        self.assertContains(response, self.article.image)
        self.assertContains(response, "/static/main/site.css")
        self.assertContains(response, "article-grid")
        self.assertLess(
            response.content.index(b"welcome-slide--gambia"),
            response.content.index(b"welcome-slide--bassari-1"),
        )
        stylesheet_path = finders.find("main/site.css")
        self.assertIsNotNone(stylesheet_path)
        stylesheet = Path(stylesheet_path).read_text(encoding="utf-8")
        self.assertIn("@keyframes welcome-pan", stylesheet)
        self.assertIn("animation-duration: 35s, 35s", stylesheet)
        self.assertIn("animation-delay: 5s, 5s", stylesheet)
        for image_name in (
            "bassari1.jpg",
            "bassari2.jpg",
            "bassari3.jpg",
            "NAVETANE1.jpg",
            "NAVETANE2.jpg",
            "NAVETANE3.jpg",
            "FLEUVE_GAMBIE.jpg",
        ):
            self.assertIn(image_name, stylesheet)


        self.assertContains(response, "welcome-slide--gambia")

    def test_detail_page_displays_article_content_and_image(self):
        response = self.client.get(
            reverse("detail_article", args=[self.article.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.article.titre)
        self.assertContains(response, self.article.contenu)
        self.assertContains(response, self.article.image)
        self.assertContains(response, "slideshow-hero")
        self.assertContains(response, "welcome-slide--gambia")
        self.assertContains(response, "welcome-slide--navetane-3")

    def test_detail_page_returns_404_for_missing_article(self):
        response = self.client.get(
            reverse("detail_article", args=[self.article.id + 1])
        )

        self.assertEqual(response.status_code, 404)


class EvenementPagesTests(TestCase):
    def setUp(self):
        self.evenement = Evenement.objects.create(
            titre="Fête du village",
            description="Une journée de rencontre pour les habitants.",
            date_heure="2027-06-15T10:00:00Z",
            lieu="Place du village",
        )

    def test_liste_evenements_affiche_les_evenements(self):
        response = self.client.get(reverse("liste_evenements"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "events-hero")
        self.assertContains(response, "welcome-slide--bassari-1")
        self.assertContains(response, "welcome-slide--navetane-3")
        self.assertContains(response, "welcome-slide--gambia")
        self.assertContains(response, self.evenement.titre)
        self.assertContains(response, self.evenement.lieu)
        self.assertContains(
            response,
            reverse("detail_evenement", args=[self.evenement.id]),
        )

    def test_liste_evenements_est_triee_par_date(self):
        evenement_suivant = Evenement.objects.create(
            titre="Marché du village",
            description="Marché annuel.",
            date_heure="2028-06-15T10:00:00Z",
            lieu="Place du village",
        )

        response = self.client.get(reverse("liste_evenements"))

        self.assertEqual(
            [
                evenement
                for evenement in response.context["evenements"]
                if evenement.date_heure is not None
            ],
            [self.evenement, evenement_suivant],
        )

    def test_detail_evenement_affiche_les_informations(self):
        response = self.client.get(
            reverse("detail_evenement", args=[self.evenement.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.evenement.titre)
        self.assertContains(response, self.evenement.description)
        self.assertContains(response, self.evenement.lieu)
        self.assertContains(response, "slideshow-hero")
        self.assertContains(response, "welcome-slide--gambia")
        self.assertContains(response, "welcome-slide--navetane-3")

    def test_evenement_sans_date_affiche_date_a_confirmer(self):
        evenement = Evenement.objects.create(
            titre="Rencontre culturelle bédik",
            description="Date à confirmer.",
            lieu="Kédougou",
        )

        liste_response = self.client.get(reverse("liste_evenements"))
        detail_response = self.client.get(
            reverse("detail_evenement", args=[evenement.id])
        )

        self.assertContains(liste_response, "Date à confirmer")
        self.assertContains(detail_response, "Date à confirmer")

    def test_evenement_peut_afficher_une_image_televersee(self):
        with TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root):
                ImageEvenement.objects.create(
                    evenement=self.evenement,
                    image=ContentFile(
                        b"image de test",
                        name="fete-village.png",
                    ),
                )

                liste_response = self.client.get(reverse("liste_evenements"))
                detail_response = self.client.get(
                    reverse("detail_evenement", args=[self.evenement.id])
                )

                self.assertContains(
                    liste_response,
                    "/media/evenements/fete-village.png",
                )
                self.assertContains(
                    detail_response,
                    "/media/evenements/fete-village.png",
                )

    def test_evenement_affiche_plusieurs_images(self):
        with TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root):
                for nom in ("fete-village-1.png", "fete-village-2.png"):
                    ImageEvenement.objects.create(
                        evenement=self.evenement,
                        image=ContentFile(b"image de test", name=nom),
                    )

                response = self.client.get(
                    reverse("detail_evenement", args=[self.evenement.id])
                )

                self.assertContains(response, "/media/evenements/fete-village-1.png")
                self.assertContains(response, "/media/evenements/fete-village-2.png")

    def test_evenement_refuse_les_fichiers_sans_extension_image(self):
        image_field = ImageEvenement._meta.get_field("image")

        with self.assertRaises(ValidationError):
            image_field.clean(
                SimpleUploadedFile("document.txt", b"pas une image"),
                None,
            )

    def test_admin_propose_plusieurs_champs_pour_les_images(self):
        admin = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="password",
        )
        self.client.force_login(admin)

        response = self.client.get(
            reverse("admin:main_evenement_change", args=[self.evenement.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="images-0-image"')
        self.assertContains(response, 'name="images-1-image"')
        self.assertContains(response, 'name="images-2-image"')

    def test_detail_evenement_returns_404_for_missing_event(self):
        response = self.client.get(
            reverse("detail_evenement", args=[self.evenement.id + 1])
        )

        self.assertEqual(response.status_code, 404)


class InformationalPagesTests(TestCase):
    def test_nouvelles_pages_sont_accessibles_et_dans_la_navigation(self):
        pages = (
            ("histoire", "Histoire de Kédougou"),
            ("galerie", "Galerie photos - Kédougou"),
            ("informations_pratiques", "Informations pratiques - Kédougou"),
            ("contact", "Contact - Kédougou"),
        )

        for nom_url, titre in pages:
            with self.subTest(page=nom_url):
                response = self.client.get(reverse(nom_url))

                self.assertEqual(response.status_code, 200)
                self.assertContains(response, f"<title>{titre}</title>", html=True)
                self.assertContains(response, reverse("histoire"))
                self.assertContains(response, reverse("galerie"))
                self.assertContains(response, reverse("informations_pratiques"))
                self.assertContains(response, reverse("contact"))
                self.assertContains(response, "slideshow-hero")
                self.assertContains(response, "welcome-slide--gambia")
                self.assertContains(response, "welcome-slide--navetane-3")

    def test_galerie_affiche_les_images_du_site(self):
        response = self.client.get(reverse("galerie"))

        self.assertContains(response, "FLEUVE_GAMBIE.jpg")
        self.assertContains(response, "Cascade_dindefelo_2.jpg")
        self.assertContains(response, "bassari1.jpg")
        self.assertContains(response, "NAVETANE1.jpg")

    def test_contact_affiche_l_adresse_electronique(self):
        response = self.client.get(reverse("contact"))

        self.assertContains(response, "diallogassim697@gmail.com")
        self.assertContains(
            response,
            'href="mailto:diallogassim697@gmail.com"',
        )
