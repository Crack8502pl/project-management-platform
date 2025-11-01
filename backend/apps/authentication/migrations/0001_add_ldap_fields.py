# Generated migration for LDAP/AD fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        # This will be updated based on the actual initial migration
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='auth_source',
            field=models.CharField(
                choices=[('LOCAL', 'Lokalna baza danych'), ('AD', 'Active Directory')],
                default='LOCAL',
                help_text='Źródło autentykacji użytkownika',
                max_length=20
            ),
        ),
        migrations.AddField(
            model_name='user',
            name='ldap_dn',
            field=models.CharField(
                blank=True,
                help_text='DN użytkownika w Active Directory',
                max_length=500,
                null=True,
                verbose_name='LDAP Distinguished Name'
            ),
        ),
        migrations.AddField(
            model_name='user',
            name='ad_synced_at',
            field=models.DateTimeField(
                blank=True,
                null=True,
                verbose_name='Ostatnia synchronizacja z AD'
            ),
        ),
    ]
