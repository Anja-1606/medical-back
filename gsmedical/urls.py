from django.urls import path
from . import views
from .views import register_user, login_user, logout_user

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('patients/', views.PatientListCreateView.as_view()),
    path('patients/<str:codeP>/', views.PatientRetrieveUpdateDestroyView.as_view()),
    path('medecins/', views.MedecinListCreateView.as_view()),
    path('medecins/<str:matriculeM>/', views.MedecinRetrieveUpdateDestroyView.as_view()),
    path('medicaments/', views.MedicamentListCreateView.as_view()),
    path('medicaments/<str:refMed>/', views.MedicamentRetrieveUpdateDestroyView.as_view()),
    path('consultations/', views.ConsultationListCreateView.as_view()),
    path('consultations/<int:id>/', views.ConsultationRetrieveUpdateDestroyView.as_view()),
    path('ordonnances/', views.OrdonnanceListCreateView.as_view()),
    path('ordonnances/<int:id>/', views.OrdonnanceRetrieveUpdateDestroyView.as_view()),
    path('contenir/', views.ContenirListCreateView.as_view()),
    path('contenir/<int:id>/', views.ContenirRetrieveUpdateDestroyView.as_view()),
]
