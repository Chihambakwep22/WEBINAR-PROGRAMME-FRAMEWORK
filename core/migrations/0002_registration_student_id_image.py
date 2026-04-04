from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='student_id_image',
            field=models.ImageField(blank=True, null=True, upload_to='student_ids/'),
        ),
    ]
