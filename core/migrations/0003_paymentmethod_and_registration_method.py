from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_registration_student_id_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=40, unique=True)),
                ('name', models.CharField(max_length=80)),
                ('method_type', models.CharField(choices=[('mobile', 'Mobile Payment'), ('card', 'Card Payment'), ('wallet', 'Digital Wallet'), ('bank', 'Bank Transfer'), ('other', 'Other')], default='other', max_length=20)),
                ('account_label', models.CharField(blank=True, help_text='Label like wallet number, merchant ID, or email.', max_length=80)),
                ('account_value', models.CharField(blank=True, help_text='Fill this later with your real account details.', max_length=120)),
                ('instructions', models.TextField(blank=True, help_text='Optional payment instructions to show users.')),
                ('active', models.BooleanField(default=True)),
                ('display_order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ['display_order', 'name'],
            },
        ),
        migrations.AddField(
            model_name='registration',
            name='payment_method',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.SET_NULL, to='core.paymentmethod'),
        ),
    ]
