from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', verbose_name='User', on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True, verbose_name='Avatar')
    nick_name = models.CharField(max_length=256, verbose_name='Nickname')
    date_joined = models.DateField(auto_now_add=True, verbose_name='Date joined')

    class Meta:
        verbose_name = 'User profile'
        verbose_name_plural = 'User profiles'

    def __str__(self):
        return self.nick_name