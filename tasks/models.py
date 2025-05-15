from django.db import models
from django.utils.text import slugify


# Create your models here.
# ----------------------------------------
# Middleware to manage user's theme choice
# ----------------------------------------
class ThemeMiddleware:
    """
    Middleware that sets up the session cookie.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        theme = request.GET.get("theme")
        if theme in ["classique", "techno", "medieval", "coquette", "lac"]:
            request.session["theme"] = theme
        request.theme = request.session.get("theme", "classique")
        return self.get_response(request)


# ----------------------------------------
# Model representing a task collection
# ----------------------------------------
class Collection(models.Model):
    """
    Represents a collection of tasks.

    Attributes:
        name (str): The name of the collection.
        slug (str): A URL-friendly version of the name.
    """
    name = models.CharField(max_length=80)
    slug = models.SlugField()

    @classmethod
    def get_default_collection(cls) -> "Collection":
        """
        Returns the default collection instance, creating it if necessary.
        :return:
        """
        collection, _ = cls.objects.get_or_create(name='Défaut', slug='_defaut')
        return collection

    def __str__(self):
        """
        Returns the name of the collection.
        :return:
        """
        return self.name

    def save(self, *args, **kwargs):
        """
        Automatically generates a slug from the name if not set,
        then saves the object as usual.
        :param args:
        :param kwargs:
        :return:
        """
        self.slug = self.slug or slugify(self.name)
        super().save(*args, **kwargs)

# ----------------------------------------
# Model representing a task
# ----------------------------------------
class Task(models.Model):
    description = models.CharField(max_length=300)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)


    def __str__(self):
        """
        Returns the name of the task.
        :return:
        """
        return self.description