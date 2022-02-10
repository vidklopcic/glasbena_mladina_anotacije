from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Revija(models.Model):
    class Type(models.IntegerChoices):
        glasbena_mladina = 0, 'Glasbena Mladina'
        muska = 1, 'Muska'
        glasna = 2, 'Glasna'

    from_fn = models.CharField(editable=False, null=True, blank=True, max_length=255)
    revija = models.IntegerField(choices=Type.choices, default=Type.glasbena_mladina)
    datum_izdaje = models.DateField()
    letnik = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)], null=True, blank=True)
    stevilka = models.IntegerField(null=True, blank=True, verbose_name='Številka')
    html = models.FileField(upload_to='revije/html', blank=True, verbose_name='HTML datoteka')
    pdf = models.FileField(upload_to='revije/pdf', blank=True, verbose_name='PDF datoteka')
    txt = models.FileField(upload_to='revije/txt', blank=True, verbose_name='TXT datoteka')
    zakljuceno = models.BooleanField(default=False, verbose_name='Zaključeno')

    def __str__(self):
        return f'{self.Type.choices[self.revija][1]} ({self.datum_izdaje.year}, {self.stevilka}.)'

    class Meta:
        verbose_name = 'Revija'
        verbose_name_plural = 'Revije'


class Avtor(models.Model):
    ime_in_priimek = models.CharField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.ime_in_priimek

    class Meta:
        verbose_name = 'Avtor'
        verbose_name_plural = 'Avtorji'


class Clanek(models.Model):
    class Kategorija(models.IntegerChoices):
        clanek = 0, 'Članek'
        intervju = 1, 'Intervju'

    revija = models.ForeignKey(Revija, on_delete=models.CASCADE)
    naslov = models.CharField(max_length=255)
    podnaslov = models.CharField(max_length=255, null=True, blank=True)
    stran_v_reviji = models.IntegerField()
    stran_v_pdf_dokumentu = models.IntegerField()
    kategorija = models.IntegerField(choices=Kategorija.choices, default=Kategorija.clanek)
    avtorji = models.ManyToManyField(Avtor, blank=True)
    vsebina = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.naslov

    class Meta:
        verbose_name = 'Članek'
        verbose_name_plural = 'Članki'