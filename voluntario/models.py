from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


def is_voluntario(user):
    return DadosVoluntario.objects.filter(user=user).exists()

class Especialidades(models.Model):
    especialidade = models.CharField(max_length=50)
    
    class Meta:
        verbose_name = 'Especialidade'
        verbose_name_plural = 'Especialidades'
    
    def __str__(self):
        return self.especialidade
    

class DadosVoluntario(models.Model):
    nome = models.CharField(max_length=100)
    cep = models.CharField(max_length=15)
    rua = models.CharField(max_length=100)
    bairro = models.CharField(max_length=100)
    numero = models.IntegerField()
    anos_de_experiencia = models.IntegerField()
    rg = models.ImageField(upload_to='rgs')
    foto = models.ImageField(upload_to='foto_perfil')
    descricao = models.TextField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    especialidade = models.ForeignKey(Especialidades, models.DO_NOTHING)
    
    
    def __str__(self):
        return self.user.username
    
    @property
    def proxima_data(self):
        proxima_data = DatasAbertas.objects.filter(user=self.user).filter(data__gt=datetime.now()).filter(agendado=False).order_by('data').first()
        return proxima_data
    
class DatasAbertas(models.Model):
    data = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    agendado = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.data) 