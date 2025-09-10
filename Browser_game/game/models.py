from django.db import models
from django.contrib.auth.models import User


class CharacterClass(models.Model):
    # Выбор класса для игрока
    name = models.CharField(max_length=50, verbose_name='Класс персонажа')
    intelligence = models.IntegerField(default=5)  # Инта
    dexterity = models.IntegerField(default=5)  # Ловкость
    strength = models.IntegerField(default=5)  # Сила
    primary_stat = models.CharField(max_length=50)  # Атрибут для механики
    miniature = models.ImageField(upload_to='miniatures/classes/', null=True,
                                  blank=True, verbose_name='Миниатюра класса')

    def __str__(self):
        return self.name


class Character(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    character_class = models.ForeignKey(CharacterClass,
                                        on_delete=models.CASCADE)
    intelligence = models.IntegerField(default=5)
    dexterity = models.IntegerField(default=5)
    strength = models.IntegerField(default=5)
    health = models.IntegerField(default=100)
    miniature = models.ImageField(upload_to='miniatures/characters/', null=True,
                                  blank=True,
                                  verbose_name='Миниатюра персонажа')
    is_alive = models.BooleanField(default=True, verbose_name='Жив')

    def __str__(self):
        return f"{self.name} ({self.character_class.name})"


class Enemy(models.Model):
    name = models.CharField(max_length=100)
    intelligence = models.IntegerField()
    dexterity = models.IntegerField()
    strength = models.IntegerField()
    health = models.IntegerField()
    miniature = models.ImageField(upload_to='miniatures/enemies/', null=True,
                                  blank=True, verbose_name='Миниатюра врага')

    def __str__(self):
        return self.name


class Scene(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    enemy = models.ForeignKey(Enemy, on_delete=models.SET_NULL, null=True,
                              blank=True)
    success_scene = models.ForeignKey('self', on_delete=models.SET_NULL,
                                      null=True, blank=True,
                                      related_name='success_from')
    failure_scene = models.ForeignKey('self', on_delete=models.SET_NULL,
                                      null=True, blank=True,
                                      related_name='failure_from')
    background_image = models.ImageField(upload_to='backgrounds/', null=True,
                                         blank=True, verbose_name='Фон локации')

    def __str__(self):
        return self.title
