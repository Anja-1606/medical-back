from django.db import models

class patient(models.Model):
    codeP = models.CharField(max_length=20,primary_key=True)
    nomP = models.CharField(max_length=100)
    prenomP = models.CharField(max_length=150)
    telP = models.CharField(max_length=13,unique=True)
    dateNais = models.DateField()
    adresseP = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.nomP} {self.prenomP}"

class medecin(models.Model):
    matriculeM = models.CharField(max_length=20,primary_key=True)
    nomM = models.CharField(max_length=100)
    prenomM = models.CharField(max_length=150)
    specM = models.CharField(max_length=150)
    telM = models.CharField(max_length=13,unique=True)
    def __str__(self):
        return f"{self.nomM} {self.prenomM}"

class consultation(models.Model):
    dateCons = models.DateField(auto_now_add=True)
    observation = models.TextField(blank=True)
    prixCons = models.DecimalField(max_digits=15,decimal_places=2)
    medecin = models.ForeignKey(medecin,to_field='matriculeM',on_delete=models.CASCADE)
    patient = models.ForeignKey(patient,to_field='codeP',on_delete=models.CASCADE, default=None)

class ordonnance(models.Model):
    dateOrd = models.DateField(auto_now_add=True)
    totalPrix = models.DecimalField(max_digits=15, decimal_places=2)
    Consultation = models.ForeignKey(consultation,on_delete=models.CASCADE)

class medicament(models.Model):
    refMed = models.CharField(max_length=20,primary_key=True)
    libelle = models.CharField(max_length=100)
    quantiteMed = models.PositiveIntegerField()
    uniteMed = models.CharField(max_length=50, default="1")
    prixMed = models.DecimalField(max_digits=15,decimal_places=2)
    ordonnances = models.ManyToManyField(ordonnance,through='contenir')
    def __str__(self):
        return f"{self.libelle} {self.quantiteMed} {self.prixMed}"

class contenir(models.Model):
    medicament = models.ForeignKey(medicament,to_field='refMed',on_delete=models.CASCADE)
    ordonnance = models.ForeignKey(ordonnance,on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
