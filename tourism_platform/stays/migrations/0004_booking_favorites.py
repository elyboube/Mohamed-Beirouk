# Generated migration for stays - add bookings and favorites

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('stays', '0003_staymedia_kind_staymedia_url_alter_staymedia_file'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='stay',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.CreateModel(
            name='StayFavorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('stay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stays.stay')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_stays', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'stay')},
            },
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_in', models.DateField()),
                ('check_out', models.DateField()),
                ('guests', models.IntegerField(default=1)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('pending', 'En attente'), ('confirmed', 'Confirmé'), ('cancelled', 'Annulé')], default='pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('stay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='stays.stay')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
