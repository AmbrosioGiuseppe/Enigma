from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

LANGUAGE = [
    ('ENGLISH', 'ENGLISH'),
    ('ITALIAN', 'ITALIAN'),
]

#NOTE: If you try to create a new record in the AllSetting table with a record already existing, it will give an error.
class AllSetting(models.Model):
    language    = models.CharField(max_length=250,choices=LANGUAGE)
    urlDomain   = models.CharField(max_length=250)
    
    def save(self, *args, **kwargs):
        if not self.pk and AllSetting.objects.exists():
            raise ValidationError('A general configuration already exists.')
        return super(AllSetting, self).save(*args, **kwargs)
    
    @classmethod
    def load(cls):
        try:
            obj = cls.objects.order_by('-id').first()
            return obj
        except Exception as e:
            # Log dell'errore o gestione specifica
            return None
    
    def __str__(self):
        return f"Language: {self.language}"
