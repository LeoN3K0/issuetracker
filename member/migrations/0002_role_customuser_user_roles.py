# Generated by Django 4.1 on 2022-09-15 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Admin'), (2, 'Project Leaders'), (4, 'Employee')], default=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='user_roles',
            field=models.ManyToManyField(blank=True, to='member.role'),
        ),
    ]