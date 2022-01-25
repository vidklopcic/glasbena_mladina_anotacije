from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Revija(models.Model):
    class Type(models.IntegerChoices):
        glasbena_mladina = 0, 'Glasbena Mladina'
        muska = 1, 'Muska'
        glasna = 2, 'Glasna'

    revija = models.IntegerField(choices=Type.choices, default=Type.glasbena_mladina)
    datum_izdaje = models.DateField()
    stevilka = models.IntegerField()
    pdf = models.FileField(upload_to='revije/pdf', blank=True)
    txt = models.FileField(upload_to='revije/txt', blank=True)

    def __str__(self):
        return f'{self.Type.choices[self.revija][1]} ({self.datum_izdaje.year}, {self.stevilka}.)'


class Avtor(models.Model):
    ime_in_priimek = models.CharField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.ime_in_priimek


class Clanek(models.Model):
    class Kategorija(models.IntegerChoices):
        clanek = 0, 'Članek'
        interviju = 1, 'Interviju'

    revija = models.ForeignKey(Revija, on_delete=models.CASCADE)
    naslov = models.CharField(max_length=255)
    podnaslov = models.CharField(max_length=255, null=True, blank=True)
    stran_v_reviji = models.IntegerField()
    stran_v_pdf_dokumentu = models.IntegerField()
    kategorija = models.IntegerField(choices=Kategorija.choices, default=Kategorija.clanek)
    avtorji = models.ManyToManyField(Avtor, blank=True)
    vsebina = models.ForeignKey('ClanekVsebina', on_delete=models.CASCADE)

    def __str__(self):
        return self.naslov


class ClanekVsebina(models.Model):
    besedilo = models.TextField()

    def __str__(self):
        return str(self.clanek_set.first() or 'nova vsebina')


@receiver(post_delete, sender=Clanek)
def delete_clanek(sender, instance: Clanek, **kwargs):
    if instance.vsebina:
        instance.vsebina.delete()
