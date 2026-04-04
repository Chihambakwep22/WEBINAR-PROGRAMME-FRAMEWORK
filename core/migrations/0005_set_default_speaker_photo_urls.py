from django.db import migrations


BASSEY_URL = 'https://images.unsplash.com/photo-1562788869-4ed32648eb72?auto=format&fit=crop&w=600&q=80'
ZHOU_URL = 'https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=600&q=80'


def set_default_speaker_photo_urls(apps, schema_editor):
    Speaker = apps.get_model('core', 'Speaker')

    Speaker.objects.filter(name='George Bassey').update(photo_url=BASSEY_URL)
    Speaker.objects.filter(name='Dr Helper Zhou').update(photo_url=ZHOU_URL)


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_speaker_photo'),
    ]

    operations = [
        migrations.RunPython(set_default_speaker_photo_urls, noop_reverse),
    ]
