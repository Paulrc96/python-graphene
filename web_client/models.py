from django.db import models

class Test(models.Model):   
    id = models.AutoField(primary_key=True)
    firstUsers = models.IntegerField()     
    time = models.DecimalField(decimal_places=3,max_digits=15)
    serverType = models.CharField(max_length=255)
    serverName = models.CharField(max_length=255)
    caseId = models.CharField(max_length=255)
    caseName = models.CharField(max_length=255)

    class Meta:
        managed = False

    def __str__(self):
        return self.id

class TestMutation(models.Model):   
    id = models.AutoField(primary_key=True)
    clientsTotal = models.IntegerField()     
    time = models.DecimalField(decimal_places=3,max_digits=15)
    serverType = models.CharField(max_length=255)
    serverName = models.CharField(max_length=255)

    class Meta:
        managed = False

    def __str__(self):
        return self.id