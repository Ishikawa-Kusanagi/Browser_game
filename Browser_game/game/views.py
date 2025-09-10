from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Character, Scene
from .forms import CharacterForm
import random


def home(request):
    if request.user.is_authenticated:
        # Если пользователь авторизован, редирект на создание персонажа или игру
        if Character.objects.filter(user=request.user, health__gt=0).exists():
            return redirect('start_scene')
        return redirect('create_character')
    # Для неавторизованных — рендер главной страницы
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('create_character')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def create_character(request):
    '''Создание персонажа'''
    if Character.objects.filter(user=request.user, health__gt=0).exists():
        # Проверяю, есть ои у пользователя перс с хп > 0, если есть
        # редиректим на первую сцену
        return redirect('start_scene')
    if request.method == 'POST':
        form = CharacterForm(request.POST)
        if form.is_valid():
            character = form.save(commit=False)  # сейвим перса с формы (но
            # сразу не отправляем в бд
            character.user = request.user
            character_class = form.cleaned_data['character_class']
            character.intelligence = character_class.intelligence + \
                                     form.cleaned_data['extra_intelligence']
            character.dexterity = character_class.dexterity + form.cleaned_data[
                'extra_dexterity']
            character.strength = character_class.strength + form.cleaned_data[
                'extra_strength']
            character.health = 100
            character.save()
            return redirect('start_scene')
    else:
        form = CharacterForm() # Если не ПОСТ запрос, просто отдаем пустую форму
    return render(request, 'create_character.html', {'form': form})


@login_required
def start_scene(request):
    character = Character.objects.filter(user=request.user,
                                         health__gt=0).first() # узнать
    # почему у перса с отрицательным хп нет редиректа на game_over
    # добавить меню выбора персонажей щас берет first(), такая же шляпа в сцене
    if not character:
        return redirect('create_character')
    scene = Scene.objects.first()
    if not scene:
        return render(request, 'no_scenes.html')
    return redirect('scene', scene_id=scene.id)


@login_required
def scene_view(request, scene_id):
    character = Character.objects.filter(user=request.user,
                                         health__gt=0).first()
    if not character:
        return redirect('create_character')
    scene = Scene.objects.get(id=scene_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        success = False
        if action == 'flee':
            success = random.random() > 0.5
        else:
            success = calculate_success(character, scene.enemy, action)
        if success:
            if scene.success_scene:
                return redirect('scene', scene_id=scene.success_scene.id)
            return render(request, 'victory.html')
        else:
            if character.health > 0:
                character.health = max(0, character.health - 20) # добавить
                # логику, чтобы хп убавлялось не на 20 а на размер атаки enemy
                character.save()
            if character.health <= 0:
                return redirect('create_character')
            if scene.failure_scene:
                return redirect('scene', scene_id=scene.failure_scene.id)
            return render(request, 'failure.html')
    return render(request, 'scene.html',
                  {'scene': scene, 'character': character})


def calculate_success(character, enemy, action):
    stat_map = {
        'fight': 'strength',
        'negotiate': 'intelligence',
        'flee': 'dexterity'
    }
    stat = getattr(character, stat_map[action])
    enemy_stat = getattr(enemy, stat_map[action]) if enemy else 10
    dice_roll = random.randint(1, 20)
    return (stat + dice_roll) > enemy_stat
