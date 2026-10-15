from rest_framework import serializers
from .models import *

class PatientSerializers(serializers.ModelSerializer):
    class Meta:
        model = patient
        fields = ["codeP", "nomP", "prenomP", "telP", "dateNais", "adresseP"]

class MedecinSerializers(serializers.ModelSerializer):
    class Meta:
        model = medecin
        fields = ["matriculeM","nomM","prenomM","specM","telM"]

class ConsultationSerializers(serializers.ModelSerializer):
    class Meta:
        model = consultation
        fields = ["id", "dateCons", "observation", "prixCons", "medecin", "patient"]
        read_only_fields = ["id", "dateCons"]  


class MedicamentSerializers(serializers.ModelSerializer):
    class Meta:
        model = medicament
        fields = ["refMed", "libelle", "quantiteMed", "uniteMed", "prixMed", "ordonnances"]
        read_only_fields = ["ordonnances"]
        
class ContenirSerializers(serializers.ModelSerializer):
    medicament = MedicamentSerializers(read_only=True)
    class Meta:
        model = contenir
        fields = ["medicament", "quantite"]

class OrdonnanceSerializers(serializers.ModelSerializer):
    lignes = ContenirSerializers(source='contenir_set', many=True, read_only=True)

    class Meta:
        model = ordonnance
        fields = ["id", "dateOrd", "totalPrix", "Consultation", "lignes"]
        read_only_fields = ["id", "dateOrd"]



