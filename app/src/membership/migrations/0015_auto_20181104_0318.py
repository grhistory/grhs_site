# Generated by Django 2.1.2 on 2018-11-04 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0014_merge_20181104_0306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='member_type',
            field=models.CharField(choices=[('I', 'Individual'), ('SE', 'Senior'), ('St', 'Student'), ('L', 'Legacy'), ('C', 'Complimentary'), ('B', 'Baxter')], default='I', max_length=25),
        ),
    ]