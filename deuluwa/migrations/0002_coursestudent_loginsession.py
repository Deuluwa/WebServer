# Generated by Django 2.1.1 on 2018-09-19 03:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('deuluwa', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coursestudent',
            fields=[
                ('couseid', models.ForeignKey(db_column='couseid', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='deuluwa.Course')),
            ],
            options={
                'db_table': 'coursestudent',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Loginsession',
            fields=[
                ('userid', models.ForeignKey(db_column='userid', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='deuluwa.User')),
                ('value', models.TextField()),
                ('lasttime', models.DateField()),
            ],
            options={
                'db_table': 'loginsession',
                'managed': False,
            },
        ),
    ]
