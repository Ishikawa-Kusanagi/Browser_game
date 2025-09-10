from django.contrib import admin
from .models import CharacterClass, Character, Enemy, Scene


# Регистрация модели CharacterClass
@admin.register(CharacterClass)
class CharacterClassAdmin(admin.ModelAdmin):
    list_display = (
    'name', 'intelligence', 'dexterity', 'strength', 'primary_stat')
    search_fields = ('name',)
    list_filter = ('primary_stat',)


# Регистрация модели Character
@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = (
    'name', 'user', 'character_class', 'intelligence', 'dexterity', 'strength',
    'health')
    search_fields = ('name', 'user__username')
    list_filter = ('character_class',)


# Регистрация модели Enemy
@admin.register(Enemy)
class EnemyAdmin(admin.ModelAdmin):
    list_display = ('name', 'intelligence', 'dexterity', 'strength', 'health')
    search_fields = ('name',)


# Регистрация модели Scene
@admin.register(Scene)
class SceneAdmin(admin.ModelAdmin):
    list_display = ('title', 'enemy', 'success_scene', 'failure_scene')
    search_fields = ('title', 'description')
    list_filter = ('enemy',)
