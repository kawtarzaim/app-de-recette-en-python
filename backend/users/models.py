from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True, max_length=500)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

    @property
    def recipe_count(self):
        from recettes.models import Recipe
        return Recipe.objects.filter(author=self.user).count()

    @property
    def favorite_count(self):
        from recettes.models import Favorite
        return Favorite.objects.filter(user=self.user).count()

    @property
    def comment_count(self):
        from recettes.models import Comment
        return Comment.objects.filter(user=self.user).count()
