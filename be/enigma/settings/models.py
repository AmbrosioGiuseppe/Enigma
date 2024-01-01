from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

LANGUAGE = [
    ('ENGLISH', 'ENGLISH'),
    ('ITALIAN', 'ITALIAN'),
]

class AllSetting(models.Model):
    language = models.CharField(max_length=250,choices=LANGUAGE)
    
    def save(self, *args, **kwargs):
        if not self.pk and AllSetting.objects.exists():
            raise ValidationError('A general configuration already exists.')
        return super(AllSetting, self).save(*args, **kwargs)
    
    @classmethod
    def load(cls):
        obj = cls.objects.order_by('-id').first()
        return obj
    
    def __str__(self):
        return f"Language: {self.language}"
    
