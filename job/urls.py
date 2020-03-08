from django.urls import path, include
from . import views


app_name = 'job'


urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('index', views.home, name='home'),
    path('home1', views.home1, name='home1'),
    path('companies', views.companies, name='companies'),
        path('companydetails/<int:id>', views.companydetails, name='companydetails'),

    path('cover', views.cover, name='cover'),
    path('applied', views.applied, name='applied'),

    path('reg', views.reg, name='reg'),
    
    path('register', views.newcompany, name='register'),
    path('register2', views.newseeker, name='register2'),
    path('cvpri', views.cvpri, name='cvpri'),

    path('cvedu', views.cvedu, name='cvedu'),
    path('cvlan', views.cvlan, name='cvlan'),
    path('cvwork', views.cvwork, name='cvwork'),
    path('cvpro', views.cvpro, name='cvpro'),
    path('cvref', views.cvref, name='cvref'),

    path('getOpenPositions/<slug:company>', views.getOpenPositions, name='getOpenPositions'),


    path('cv', views.cv, name='cv'),
    path('cv2', views.cv2, name='cv2'),

    path('job', views.job, name='job'),
    path('managejob', views.managejob, name='managejob'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('newjob', views.newjob, name='newjob'),
    path('profile2', views.profile2, name='profile2'),
    path('profile', views.profile, name='profile'),
    
        path('seekers', views.seekers, name='seekers'),
        path('seekerdetail/<int:id>', views.seekerdetail, name='seekerdetail'),
        path('appl/<int:id>/<int:id2>', views.appl, name='appl'),
        path('appliedlist/<int:id>', views.appliedlist, name='appliedlist'),

    path('approve/<int:id>/<int:id2>', views.approve, name='approve'),    

        path('appliedjobdetail/<int:job>', views.appliedjobdetail, name='appliedjobdetail'),


        path('jobdetail/<int:job>', views.jobdetail, name='jobdetail'),
        path('jobdetail2/<int:job>', views.jobdetail2, name='jobdetail2'),
        path('apply/<str:job>', views.apply, name='apply'),
        path('jobstatus/<int:job>', views.jobstatus, name='jobstatus'),
        path('jobstatus2/<int:job>', views.jobstatus2, name='jobstatus2'),

        



    path('about1', views.about1, name='about1'),
    path('contact1', views.contact1, name='contact1'),

    path('deletejob/<int:title>', views.deletejob, name='deletejob'),

    path('deleteedu/<int:title>', views.deleteedu, name='deleteedu'),
    path('deletelan/<int:title>', views.deletelan, name='deletelan'),
    path('deletepro/<int:title>', views.deletepro, name='deletepro'),
    path('deletework/<int:title>', views.deletework, name='deletework'),
    path('deleteref/<int:title>', views.deleteref, name='deleteref'),

    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('help', views.help, name='help'),
    path('updatedetails', views.updatedetails, name='updatedetails'),

    path('home2', views.home2, name='home2')
]