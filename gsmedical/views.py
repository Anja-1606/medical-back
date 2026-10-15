from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email', '')
    
    if not username or not password:
        return Response({'error': 'Nom d’utilisateur et mot de passe requis.'}, status=status.HTTP_400_BAD_REQUEST)
        
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Ce nom d’utilisateur existe déjà.'}, status=status.HTTP_400_BAD_REQUEST)
        
    user = User.objects.create_user(username=username, password=password, email=email)
    return Response({'message': 'Utilisateur créé avec succès !'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({'message': 'Connexion réussie', 'username': user.username}, status=status.HTTP_200_OK)
    return Response({'error': 'Identifiants invalides.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout_user(request):
    logout(request)
    return Response({'message': 'Déconnexion réussie'}, status=status.HTTP_200_OK)

class PatientListCreateView(generics.ListCreateAPIView):
    queryset = patient.objects.all()
    serializer_class = PatientSerializers

class PatientRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = patient.objects.all()
    serializer_class = PatientSerializers
    lookup_field = "codeP"

class MedecinListCreateView(generics.ListCreateAPIView):
    queryset = medecin.objects.all()
    serializer_class = MedecinSerializers

class MedecinRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = medecin.objects.all()
    serializer_class = MedecinSerializers
    lookup_field = "matriculeM"

class ConsultationListCreateView(generics.ListCreateAPIView):
    queryset = consultation.objects.all()
    serializer_class = ConsultationSerializers

class ConsultationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = consultation.objects.all()
    serializer_class = ConsultationSerializers
    lookup_field = "id"

class OrdonnanceListCreateView(generics.ListCreateAPIView):
    queryset = ordonnance.objects.all()
    serializer_class = OrdonnanceSerializers

    def create(self, request, *args, **kwargs):
        data = request.data
        lignes = data.get('lignes', [])

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        ordonnance_instance = serializer.save()

        for ligne in lignes:
            ref_med = ligne.get('medicament')
            quantite = int(ligne.get('quantite', 1))

            try:
                med_obj = medicament.objects.get(pk=ref_med)
                
                contenir.objects.create(
                    ordonnance=ordonnance_instance,
                    medicament=med_obj,
                    quantite=quantite
                )

                if med_obj.quantiteMed >= quantite:
                    med_obj.quantiteMed -= quantite
                    med_obj.save()
                else:
                    pass
            except medicament.DoesNotExist:
                pass

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class OrdonnanceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ordonnance.objects.all()
    serializer_class = OrdonnanceSerializers
    lookup_field = "id"

class MedicamentListCreateView(generics.ListCreateAPIView):
    queryset = medicament.objects.all()
    serializer_class = MedicamentSerializers

class MedicamentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = medicament.objects.all()
    serializer_class = MedicamentSerializers
    lookup_field = "refMed"

class ContenirListCreateView(generics.ListCreateAPIView):
    queryset = contenir.objects.all()
    serializer_class = ContenirSerializers

class ContenirRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = contenir.objects.all()
    serializer_class = ContenirSerializers
    lookup_field = "quantite"

