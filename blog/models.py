from django.db import models
from django.urls import reverse  # new


class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
    )
    body = models.TextField()
    image = models.ImageField(blank=True, null=True, upload_to="images/")
    text = models.TextField(blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):  # new
        return reverse("post_detail", kwargs={"pk": self.pk})
