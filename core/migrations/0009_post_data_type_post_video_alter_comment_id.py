# Generated by Django 4.2.6 on 2023-11-01 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_profile_coverimg'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='data_type',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='post',
            name='video',
            field=models.FileField(null=True, upload_to='post_videos'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
