from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
import os
from home.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing, name = "landing_page"), 
    path('register/', register, name= "register"),
    path('login1/', login1, name = "login"),
    path('logout/', log_out, name = "log_out"),
    #patient pages
    path('pdash/', patient_dashboard, name = 'patient_dashboard'),
    path('pappointment/', appointment, name = 'patient_appointment'),
    path('pmeds/', pmeds, name = 'patient_meds'),
    path('delete-med/<int:id>/', delete_med, name='delete_med'),
    path('pvitals/', vitals, name = 'patient_vitals'),
    path('presc-upload/', presc, name = 'patient_presc_upload'),
    path('pprofile/', profile_p, name = 'patient_profile'),
    #doctor pages
    path('ddash/', doctor_dashboard, name = 'doctor_dashboard'),
    path('dcheck/', check, name = 'check_requests'),
    path('dprofile/', dprofile, name = 'doctor_profile'),
    path('dpresc/', prescribe, name = 'doctor_prescribe'),
    path('dview/', view_patients, name = 'view_patients'),
    path('dviewreport/', view_reports, name = 'view_report'),
    #new adds
    path('pcard/', card, name = 'card'),
    path('api/medicine_status/<str:uid>/', get_meds_api, name='api'),
]

# Add this only in development mode
urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR, "static"))
