# Generated by Django 5.1.7 on 2025-07-10 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0004_rename_escolha_imagem_tipo_conta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagem',
            name='boleto_valor',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
    ]
