import uuid
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="The telephone number must be in the format: '+999999999'. Up to 15 digits are allowed."
)

LEVEL_USER = [
    ('DEFAULT', 'DEFAULT'),
    ('PREMIUM', 'PREMIUM'),
]

class User(AbstractUser):
    uid                 = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    telephoneNumber     = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    levelUser           = models.CharField(max_length=255,choices=LEVEL_USER,default='DEFAULT')
    is_active           = models.BooleanField(default=False)
    terms               = models.BooleanField(default=False)
    privacy             = models.BooleanField(default=False)
    newsletter          = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.username)
    

class EmailVerificationToken(models.Model):
    user                = models.ForeignKey(User,on_delete=models.CASCADE)
    token               = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at          = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"User: {self.user} - Token: {self.token}"


class AccountsEmailSetting(models.Model):
    #The expiration is calculated in hours, example: 48 means 48 hours before the link to validate the newly registered account expires
    emailLinkExpiration = models.IntegerField(blank=True,null=True)
    
    def save(self, *args, **kwargs):
        if not self.pk and AccountsEmailSetting.objects.exists():
            raise ValidationError('A general configuration already exists.')
        return super(AccountsEmailSetting, self).save(*args, **kwargs)
    
    @classmethod
    def load(cls):
        obj = cls.objects.order_by('-id').first()
        return obj
    
    def __str__(self):
        return f"Email Link Expiration: {self.emailLinkExpiration}"
    