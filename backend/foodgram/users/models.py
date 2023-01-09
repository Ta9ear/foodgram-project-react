from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **other_fields):
        """
        Create and save a User with the given email, password and extra fields.
        """
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **other_fields):
        """
        Create and save a SuperUser with the given
        email, password and extra fields.
        """
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self.create_user(email, password, **other_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(
        max_length=256,
        unique=True,
        verbose_name='Почта'
    )
    first_name = models.CharField(max_length=128, verbose_name='Имя')
    last_name = models.CharField(max_length=128, verbose_name='Фамилия')
    username = models.CharField(max_length=128, verbose_name='Никнейм')
    password = models.CharField(max_length=128, verbose_name='Пароль')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = CustomUserManager()

    class Meta:
        ordering = ['-pk']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email


class Subscription(models.Model):
    user = models.ForeignKey(
        CustomUser,
        related_name='follower',
        on_delete=models.CASCADE,
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        CustomUser,
        related_name='author',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписка'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='user_subscription_unique'
            )
        ]

    def __str__(self):
        return f'Пользователь {self.user} подписался на {self.author}'
