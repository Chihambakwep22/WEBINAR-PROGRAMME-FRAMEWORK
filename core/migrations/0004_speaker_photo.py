from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_paymentmethod_and_registration_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='speaker',
            name='speaker_photo',
            field=models.ImageField(blank=True, null=True, upload_to='speakers/'),
        ),
    ]
