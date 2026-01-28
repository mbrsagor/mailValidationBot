from django.db import models
from user.models import Timestamp


class Slider(Timestamp):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True, default='')
    button_text = models.CharField(max_length=255, blank=True, null=True, default='')
    button_url = models.URLField(blank=True, null=True, default='')
    image = models.ImageField(upload_to='sliders', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Slider'
        verbose_name_plural = 'Sliders'
