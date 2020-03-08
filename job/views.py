from django.shortcuts import render,HttpResponseRedirect,reverse,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

import PyPDF2 as p2 
from django.conf import settings
import substring
import re
# import schedule
# Create your views here.



def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return HttpResponseRedirect(reverse('Hospital:login'))


def login(request):
    if request.method == 'post':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            
            return HttpResponseRedirect(reverse('job:home'))
        else:
            context = {
                'errors':user.errors
            }
            return render(request, 'job/registration/login.html')
    else:
        return render(request, 'job/registration/login.html')




@login_required
def home(request):
    if request.user.is_authenticated:
        if request.user.is_seeker:
            return HttpResponseRedirect(reverse('job:dashboard'))
        else:
            return HttpResponseRedirect(reverse('job:managejob'))
        #     return render(request, 'job/employer/managejob.html')

@login_required
def dashboard(request):
    return render(request, 'job/seeker/dashboard.html')

@login_required
def home1(request):
    return render(request, 'job/seeker/index.html')

def welcome(request):
    if request.user.is_authenticated:
        if request.user.is_seeker:
            return HttpResponseRedirect(reverse('job:dashboard'))
        elif request.user.is_company:
            return HttpResponseRedirect(reverse('job:managejob'))
        #     return render(request, 'job/employer/managejob.html')
    else:
        return render(request, 'job/welcome.html')  

@login_required
def companies(request):
    companies = Company.objects.all()
    
    context = {
            "companies":companies
    }
    return render(request, 'job/seeker/companies.html',context)

def getOpenPositions(request,company):
    open_positions = Job.objects.filter(company=company,status="True").count()
    return open_positions

@login_required
def companydetails(request, id):
    # print(request.GET.get('company'))
    
    u = CustomUser.objects.get(pk=id)
    c = Company.objects.get(user=u)
    jobs = Job.objects.filter(company=c,status="True")
    context = {
            "c":c,
            "jobs":jobs 
               }
    return render(request, 'job/seeker/companydetail.html',context)

@login_required
def cv(request):
#     edu = CVEdu.objects.filter() where user is currently logged in
    
    if request.POST:
        a = CVEdu.objects.create(
            title = request.POST.get("title"),
            from_date = request.POST.get("from_date"),
            end_date = request.POST.get("end_date"),
            level = request.POST.get("level"),
            user = request.user
        )
        a.save()
        return HttpResponseRedirect(reverse('job:cv'))
    
    seeker = Seeker.objects.get(user=request.user)
    try:
        cvpri = CVPri.objects.get(user=request.user)
    except CVPri.DoesNotExist:
        cvpri = None

    try:
        cvedu = CVEdu.objects.filter(user=request.user)
    except CVEdu.DoesNotExist:
        cvedu = None

    try:
        cvwork = CVWork.objects.filter(user=request.user)
    except CVWork.DoesNotExist:
        cvwork = None

    try:
        cvlan = CVLan.objects.filter(user=request.user)
    except CVLan.DoesNotExist:
        cvlan = None
    try:
        cvskills = CVPro.objects.filter(user=request.user)
    except CVPro.DoesNotExist:
        cvskills = None
    try:
        cvrefs = CVRef.objects.filter(user=request.user)
    except CVRef.DoesNotExist:
        cvrefs = None


   
    context = {
            "seeker":seeker,
            "cvpri":cvpri,
            "edu":cvedu,
            "work":cvwork,
            "lan":cvlan,
            "pro":cvskills,
            "ref":cvrefs
            
    }
    return render(request, 'job/seeker/cv.html',context)

    
def deleteedu(request,title):
    seeker = Seeker.objects.get(user=request.user)
    to_delete = get_object_or_404(CVEdu, pk=title)
    if to_delete.level == "P.L.E":
        seeker.rating = seeker.rating - 1
        seeker.save()

    if to_delete.level == "U.C.E":
        seeker.rating = seeker.rating - 2
        seeker.save()

    if to_delete.level == "U.A.C.E":
        seeker.rating = seeker.rating - 2
        seeker.save()

    if to_delete.level == "Certificate":
        seeker.rating = seeker.rating - 4
        seeker.save()

    if to_delete.level == "Diploma":
        seeker.rating = seeker.rating - 4
        seeker.save()

    if to_delete.level == "Degree":
        seeker.rating = seeker.rating - 8
        seeker.save()

    if to_delete.level == "Masters":
        seeker.rating = seeker.rating - 8
        seeker.save()

    if to_delete.level == "PHd":
        seeker.rating = seeker.rating - 11
        seeker.save()
    
    to_delete.delete()
    return HttpResponseRedirect(reverse('job:cv'))

def deletelan(request,title):
    get_object_or_404(CVLan, title=title).delete()
    return HttpResponseRedirect(reverse('job:cv'))

def deletepro(request,title):
    get_object_or_404(CVPro, title=title).delete()
    
    return HttpResponseRedirect(reverse('job:cv'))

def deletework(request,title):
    a = get_object_or_404(CVWork, pk=title)
    seeker = Seeker.objects.get(user=request.user)

    try:
        cvwork = CVWork.objects.filter(user=request.user)
    except CVWork.DoesNotExist:
        cvwork = None

    if a.companytype == "International":
        cunt = 0
        for b in cvwork:
            if b.companytype == "International":
                cunt = cunt + 1
           
        if cunt==1:
            seeker.rating = seeker.rating - 23
            seeker.save()
        

    if a.companytype == "Private Company":
        seeker.rating = seeker.rating - 18
        seeker.save()

    if a.companytype == "Non-Government Organization":
        seeker.rating = seeker.rating - 23
        seeker.save()

    if a.companytype == "Government":
        seeker.rating = seeker.rating - 14
        seeker.save()

    if a.companytype == "Freelance":
        seeker.rating = seeker.rating - 5
        seeker.save()
    
    a.delete()
    return HttpResponseRedirect(reverse('job:cv'))

def deleteref(request,title):
    get_object_or_404(CVRef, name=title).delete()
    return HttpResponseRedirect(reverse('job:cv'))

def deletejob(request,title):
    
    job = Job.objects.get(pk=title)
    a = AppliedJobs.objects.filter(job=job)
    for b in a:
        if b.job == job:
            get_object_or_404(Job, pk=title).delete()

    get_object_or_404(Job, pk=title).delete()
    return HttpResponseRedirect(reverse('job:managejob'))

def cvpri(request):
    if request.POST:
        cvpri = CVPri.objects.get(user=request.user)
        cvpri.full_name = request.POST.get("full_name")
        cvpri.age = request.POST.get("age")
        cvpri.marital_status = request.POST.get("marital_status")
        cvpri.nationality = request.POST.get("nationality")
        cvpri.save()
        return HttpResponseRedirect(reverse('job:cv'))

    return render(request, 'job/seeker/cv.html')

def cvedu(request):
    edu = CVEdu.objects.filter(user=request.user)
    seeker = Seeker.objects.get(user=request.user)

    if request.POST:
        a = CVEdu.objects.create(
            title = request.POST.get("title"),
            from_date = request.POST.get("from_date"),
            end_date = request.POST.get("end_date"),
            level = request.POST.get("level"),
            user = request.user
        )
        a.save()



        if a.level == "P.L.E":
            print("Ple level")
            seeker.rating = seeker.rating + 1
            seeker.save()

        if a.level == "U.C.E":
            seeker.rating = seeker.rating + 2
            seeker.save()

        if a.level == "U.A.C.E":
            seeker.rating = seeker.rating + 2
            seeker.save()
            
        if a.level == "Certificate":
            seeker.rating = seeker.rating + 4
            seeker.save()

        if a.level == "Diploma":
            seeker.rating = seeker.rating + 4
            seeker.save()

        if a.level == "Degree":
            seeker.rating = seeker.rating + 8
            seeker.save()

        if a.level == "Masters":
            seeker.rating = seeker.rating + 8
            seeker.save()

        if a.level == "PHd":
            seeker.rating = seeker.rating + 11
            seeker.save()

      
        
        return HttpResponseRedirect(reverse('job:cv'))
    context = {
        "edu":edu
    }
    return render(request, 'job/seeker/cv.html',context)

def cvlan(request):
    if request.POST:
        a = CVLan.objects.create(
            title = request.POST.get("title"),
            spoken = request.POST.get("spoken"),
            written = request.POST.get("written"),
            user = request.user

          
        )
        a.save()
        return HttpResponseRedirect(reverse('job:cv'))


def cvpro(request):
    if request.POST:
        a = CVPro.objects.create(
            title = request.POST.get("title"),
            percent = request.POST.get("percent"),
           
            user = request.user
        )
        a.save()
        return HttpResponseRedirect(reverse('job:cv'))
 
def cvwork(request):
    seeker = Seeker.objects.get(user=request.user)
    try:
        cvwork = CVWork.objects.filter(user=request.user)
    except CVWork.DoesNotExist:
        cvwork = None

    if request.POST:
        a = CVWork.objects.create(
            title = request.POST.get("title"),
            from_date = request.POST.get("from_date"),
            end_date = request.POST.get("end_date"),
            description = request.POST.get("description"),
            company = request.POST.get("company"),
            companytype = request.POST.get("companytype"),
            user = request.user

        )
        a.save()




        cunt1 = 0

        if a.companytype == "International":
            for b in cvwork:
                if b.companytype == "International":
                    cunt1 = cunt1 + 1
           
        if cunt1==1:
            seeker.rating = seeker.rating + 23
            seeker.save()

        if a.companytype == "Private Company":
            seeker.rating = seeker.rating + 18
            seeker.save()

        if a.companytype == "Non-Government Organization":
            seeker.rating = seeker.rating + 23
            seeker.save()

        if a.companytype == "Government":
            seeker.rating = seeker.rating + 14
            seeker.save()

        if a.companytype == "Freelance":
            seeker.rating = seeker.rating + 5
            seeker.save()

        return HttpResponseRedirect(reverse('job:cv'))
  

def cvref(request):
    if request.POST:
        a = CVRef.objects.create(
            title = request.POST.get("title"),
            name = request.POST.get("name"),
            email = request.POST.get("email"),
            phone = request.POST.get("phone"),
            user = request.user


        )
        a.save()
        return HttpResponseRedirect(reverse('job:cv'))


























def cv1(request):
#     edu = CVEdu.objects.filter()
    if request.POST:
        a = CVPri.objects.create(


        full_name = request.POST.get("full_name"),
        age = request.POST.get("age"),
        marital_status = request.POST.get("marital_status"),
        nationality = request.POST.get("nationality"),
        )
        a.save()
        return HttpResponseRedirect(reverse('job:job'))

    return render(request, 'job/seeker/cv.html')

   
def cover(request):
    return render(request, 'job/seeker/cover.html') 

def profile(request):
    seeker = Seeker.objects.get(user=request.user)
    jobs = AppliedJobs.objects.filter(seeker=seeker)

    approved = 0
    pending = 0
    declined = 0
    for b in jobs:
        if b.status:
            approved = approved + 1
        else:
            if b.limit_reached:
                declined = declined + 1
            else:
                pending = pending + 1

    context = {
            
            "s":seeker,
            "applied_jobs":jobs.count(),
            "approved":approved,
            "pending":pending,
            "declined":declined
    }
    return render(request, 'job/seeker/profile.html',context) 

def cv2(request):
    return render(request, 'job/seeker/cv2.html')

@login_required
def job(request):
    jobs = Job.objects.filter(status=True)

    context = {
        "jobs":jobs
    }
    return render(request, 'job/seeker/job.html',context)

@login_required
def applied(request):
    seeker = Seeker.objects.get(user=request.user)
    jobs = AppliedJobs.objects.filter(seeker=seeker)
    context = {
            
            "s":seeker,
            "jobs":jobs
    }
    return render(request, 'job/seeker/applied.html',context)

@login_required
def jobdetail(request,job):
    job = Job.objects.get(pk=job)
    
    try:
        a = AppliedJobs.objects.get(job=job,seeker=Seeker.objects.get(user=request.user))
        #  a = None
    except AppliedJobs.DoesNotExist:
        a = None


    if a != None:
        is_applied = True
    else:
        is_applied = False


    context = {
            
            "job":job,
            "is_applied":is_applied
    }
    return render(request, 'job/seeker/jobdetail.html',context)

@login_required
def appliedjobdetail(request,job):
    job = AppliedJobs.objects.get(pk=job)
    
    try:
        a = AppliedJobs.objects.get(job=job.job,seeker=Seeker.objects.get(user=request.user))
        #  a = None
    except AppliedJobs.DoesNotExist:
        a = None


    if a != None:
        is_applied = True
    else:
        is_applied = False
 
    sa = substring.substringByChar(job.academic_extract, startChar="~", endChar="`")

    print(sa)

    context = {
            
            "job":job,
            "is_applied":is_applied
    }
    return render(request, 'job/seeker/appliedjobdetail.html',context)

@login_required
def jobdetail2(request,job):
    job = Job.objects.get(pk=job)
    
    context = {
            
            "job":job
    }
    return render(request, 'job/employer/jobdetail.html',context)

@login_required
def apply(request,job):
    job = Job.objects.get(title=job)
    if request.POST:
        a = AppliedJobs.objects.create(


        job = job,
        seeker = Seeker.objects.get(user=request.user)


        )
        a.save()
        if request.FILES:
            a.cover = request.FILES['cover']
            a.academic = request.FILES['academic']
            a.rec = request.FILES['rec']


            a.save()

# settings.BASE_DIR
            PDFfile = open(settings.BASE_DIR + a.academic.url,"rb")
            pdfReader = p2.PdfFileReader(PDFfile)
            print(pdfReader.numPages)
            pageObj = pdfReader.getPage(1)
            # print(pageObj.extractText())
            a.academic_extract = pageObj.extractText()
            a.save()
            PDFfile.close()


         
            
        
        return HttpResponseRedirect(reverse('job:applied'))

    context = {
            
            "job":job
    }
    return render(request, 'job/seeker/apply.html',context)


    


def about(request):
    return render(request, 'job/seeker/about.html')

def contact(request):
    return render(request, 'job/seeker/contact.html')

def help(request):
    return render(request, 'job/seeker/help.html')

def updatedetails(request):
    return render(request, 'job/seeker/updatedetails.html')



# def login(request):
    # user = auth.authenticate(username=username, password=password)

    #     if user is not None:
    #         auth.login(request, user)
    #         messages.add_message(request, messages.INFO,
    #                              'Your are now Logged in.')
    #         return HttpResponseRedirect(reverse('Hospital:home'))
    #     else:
    #         context = {
    #             'errors':user.errors
    #         }
    #         return render(request, 'job/registration/login.html',context)
#     if request.method == 'post':
#         return HttpResponseRedirect(reverse('job:home1'))
        

def newcompany(request):
    form = CustomUserCreationFormCompany(request.POST or None , request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            company = form.save()
            company.title  = request.POST["title"]
            company.phone  = request.POST["phone"]
            company.email  = request.POST["email"]

            company.username  = request.POST["username"]
            company.save()
            if request.FILES:
                company.logo = request.FILES['logo']
                company.save()
                
            return HttpResponseRedirect(reverse('login'))

        else:
            context = { "form":form}
            return render(request, 'job/register.html',context)

    else:
        context = {'form': form}
        return render(request, 'job/register.html',context)

def newseeker(request):
    form = CustomUserCreationFormSeeker(request.POST or None , request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            seeker = form.save()
            seeker.age  = request.POST["age"]
            seeker.email  = request.POST["email"]
            seeker.phone  = request.POST["phone"]
            seeker.gender  = request.POST["gender"]
            seeker.save()
            if request.FILES:
                seeker.usericon = request.FILES['usericon']
                seeker.save()
           
            cv = CVPri.objects.create(user=seeker.user)
            cv.save()
            return HttpResponseRedirect(reverse('job:dashboard'))

        else:
            context = { "form":form}
            return render(request, 'job/register2.html',context)
    else:
        context = { "form":form}
        return render(request, 'job/register2.html',context)



def reg(request):
    return render(request, 'job/reg.html')

def home2(request):
    company = Company.objects.get(user=request.user)
    jobs = Job.objects.filter(company=company)
    a = AppliedJobs.objects.all()

    total_applied = 0
    approved = 0
    pending = 0
    declined = 0

   
    for cc in a:
        if cc.job.company.user == request.user:
            total_applied = total_applied + 1


    for b in a:
        if b.job.company.user == request.user:
            if b.status:
                approved = approved + 1
            else:
                if b.limit_reached:
                    declined = declined + 1
                else:
                    pending = pending + 1

    context = {
            
            "posted_jobs":jobs.count(),
            "total_applied":total_applied,
            "approved":approved,
            "pending":pending,
            "declined":declined
    }
    return render(request, 'job/employer/index.html',context)

def profile2(request):
    company = Company.objects.get(user=request.user)
    context = {
            "company":company
    }
    if request.POST:

 
       
        company.title = request.POST.get("title")
        company.since  = request.POST.get("since")
        company.team  = request.POST.get("team")
        company.phone = request.POST.get("phone")
        company.email  = request.POST.get("email")
        company.website  = request.POST.get("website")
        company.address  = request.POST.get("address")
        company.description  = request.POST.get("description")

        if request.FILES:
            company.logo = request.FILES.get("logo"),
      
    
        company.save()
        return HttpResponseRedirect(reverse('job:profile2'))
    return render(request, 'job/employer/profile.html',context)

def about1(request):
    return render(request, 'job/employer/about.html')

def contact1(request):
    return render(request, 'job/employer/contact.html')

def newjob(request):
    if request.POST:                    
        a = Job.objects.create(
            title = request.POST.get("title"),
            jobtype = request.POST.get("jobtype"),
            offered_salary = request.POST.get("offered_salary"),
            exp = request.POST.get("exp"),
            email = request.POST.get("email"),
            phone = request.POST.get("phone"),
            description = request.POST.get("description"),
            jobindustry = request.POST.get("jobindustry"),
            deadline = request.POST.get("deadline"),
            qualification = request.POST.get("qualification"),
            city = request.POST.get("city"),
            address = request.POST.get("address"),
            skills2 = request.POST.get("skills2"),
            exp2 = request.POST.get("exp2"),
            gender = request.POST.get("gender"),
            people = request.POST.get("people"),
            company = Company.objects.get(user=request.user)
        )
        a.save()
        return HttpResponseRedirect(reverse('job:managejob'))


    return render(request, 'job/employer/newjob.html')

def seekers(request):
    seekers = Seeker.objects.all()
    context = {
            "seekers":seekers
    }
    return render(request, 'job/employer/seekers.html',context)

def seekerdetail(request,id):

    u = CustomUser.objects.get(pk=id)
    s = Seeker.objects.get(user=u)


    
    try:
        cvpri = CVPri.objects.get(user=u)
    except CVPri.DoesNotExist:
        cvpri = None

    try:
        cvedu = CVEdu.objects.filter(user=u)
    except CVEdu.DoesNotExist:
        cvedu = None

    try:
        cvwork = CVWork.objects.filter(user=u)
    except CVWork.DoesNotExist:
        cvwork = None

    try:
        cvlan = CVLan.objects.filter(user=u)
    except CVLan.DoesNotExist:
        cvlan = None
    try:
        cvskills = CVPro.objects.filter(user=u)
    except CVPro.DoesNotExist:
        cvskills = None
    try:
        cvrefs = CVRef.objects.filter(user=u)
    except CVRef.DoesNotExist:
        cvrefs = None


   
    context = {
          
            "cvpri":cvpri,
            "edu":cvedu,
            "work":cvwork,
            "lan":cvlan,
            "pro":cvskills,
            "ref":cvrefs,
             "s":s
            
    }



    return render(request, 'job/employer/seekerdetail.html',context)


def appl(request,id,id2):
    j = Job.objects.get(pk=id2)
    u = CustomUser.objects.get(pk=id)
    s = Seeker.objects.get(user=u)
    a = AppliedJobs.objects.get(seeker=s,job=j)

    sa = substring.substringByChar(a.academic_extract, startChar="~", endChar="`")

   
    
    try:
        cvpri = CVPri.objects.get(user=u)
    except CVPri.DoesNotExist:
        cvpri = None

    try:
        cvedu = CVEdu.objects.filter(user=u)
    except CVEdu.DoesNotExist:
        cvedu = None

    try:
        cvwork = CVWork.objects.filter(user=u)
    except CVWork.DoesNotExist:
        cvwork = None

    try:
        cvlan = CVLan.objects.filter(user=u)
    except CVLan.DoesNotExist:
        cvlan = None
    try:
        cvskills = CVPro.objects.filter(user=u)
    except CVPro.DoesNotExist:
        cvskills = None
    try:
        cvrefs = CVRef.objects.filter(user=u)
    except CVRef.DoesNotExist:
        cvrefs = None


   
    context = {
          
            "cvpri":cvpri,
            "edu":cvedu,
            "work":cvwork,
            "lan":cvlan,
            "pro":cvskills,
            "ref":cvrefs,
             "s":s,
            "a":a,
            "cgpa":sa.replace("~","").replace("`",""),
            "j":j
    }



    return render(request, 'job/employer/appl.html',context)


    

def appliedlist(request,id):

    j = Job.objects.get(pk=id)
    s = AppliedJobs.objects.filter(job=j)
    # jobs = Job.objects.filter(company=c)
    
    context = {
            "ss":s,
            "j":j
    }
    return render(request, 'job/employer/appliedlist.html',context)






@login_required
def managejob(request):
    applied = 0
    appliedspecific = 0
    company = Company.objects.get(user=request.user)
    myjobs = Job.objects.filter(company=company)
    active = myjobs.filter(status=True).count()
    a = AppliedJobs.objects.all()
    for b in a:
        if b.job.company.user == request.user:
            applied = applied + 1



    context = {
            "company":company,
            "myjobs":myjobs,
            "posted":myjobs.count(),
            "applied":applied,
            "active":active
    }
    return render(request, 'job/employer/managejob.html',context)





def jobstatus(request,job):
    job = Job.objects.get(pk=job)
    job.status = False
    job.save()
    return HttpResponseRedirect(reverse('job:managejob'))

def jobstatus2(request,job):
    job = Job.objects.get(pk=job)
    job.status = True
    job.save()
    return HttpResponseRedirect(reverse('job:managejob'))


def approve(request,id,id2):
    j = Job.objects.get(pk=id2)
    u = CustomUser.objects.get(pk=id)
    s = Seeker.objects.get(user=u)
    a = AppliedJobs.objects.get(seeker=s,job=j)
    

    a.status = True
    a.save()

    aa = AppliedJobs.objects.filter(job=j,status=True).count()
    aaa = AppliedJobs.objects.filter(job=j,status=False)
    if j.people == aa:
        j.status = False
        j.save()
    for bb in aaa:
        bb.limit_reached = True
        bb.save()

        
    return HttpResponseRedirect(reverse('job:appl', kwargs={'id': id,"id2":id2}))  
