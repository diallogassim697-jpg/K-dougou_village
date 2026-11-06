from django.db import models
from django.core.validators import FileExtensionValidator

class Article(models.Model):
    titre = models.CharField(max_length=200, verbose_name="Titre")
    contenu = models.TextField(verbose_name="Contenu")
    # On utilise un champ texte pour l'image (nom du fichier ou URL)
    image = models.CharField(max_length=255, blank=True, null=True, verbose_name="Nom de l'image")
    date_publication = models.DateTimeField(auto_now_add=True, verbose_name="Date de publication")

    def __str__(self):
        return self.titre


class Evenement(models.Model):
    titre = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(verbose_name="Description")
    date_heure = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Date et heure",
        help_text="Laissez vide si la date n'est pas encore confirmée.",
    )
    lieu = models.CharField(max_length=200, verbose_name="Lieu")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    class Meta:
        ordering = ["date_heure"]
        verbose_name = "événement"
        verbose_name_plural = "événements"

    def __str__(self):
        return self.titre


class ImageEvenement(models.Model):
    evenement = models.ForeignKey(
        Evenement,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Événement",
    )
    image = models.FileField(
        upload_to="evenements/",
        validators=[FileExtensionValidator(["jpg", "jpeg", "png", "webp"])],
        verbose_name="Image",
    )

    class Meta:
        verbose_name = "image d'événement"
        verbose_name_plural = "images d'événement"

    def __str__(self):
        return f"Image - {self.evenement.titre}"
