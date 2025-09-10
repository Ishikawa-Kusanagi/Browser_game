from django.db import migrations


def create_initial_data(apps, schema_editor):
    CharacterClass = apps.get_model('game', 'CharacterClass')
    CharacterClass.objects.create(
        name='Маг',
        primary_stat='intelligence',
        intelligence=10,
        dexterity=5,
        strength=5
    )
    CharacterClass.objects.create(
        name='Лучник',
        primary_stat='dexterity',
        intelligence=5,
        dexterity=10,
        strength=5
    )
    CharacterClass.objects.create(
        name='Воин',
        primary_stat='strength',
        intelligence=5,
        dexterity=5,
        strength=10
    )


class Migration(migrations.Migration):
    dependencies = [
        ('game', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(create_initial_data),
    ]
