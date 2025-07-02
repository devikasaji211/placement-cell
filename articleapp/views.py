from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import ArticleProfile, VacancyPost
from studentapp.models import ReferralRequest

from studentapp.models import Notification


# Create your views here.

@login_required
def article_page(request):
    try:
        profile = ArticleProfile.objects.get(user=request.user)
    except ArticleProfile.DoesNotExist:
        profile = None

    vacancies = VacancyPost.objects.filter(article=request.user)
    unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
    return render(request, 'article_page.html', {'profile': profile, 'vacancies': vacancies, 'unread_count': unread_count})

def article_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            try:
                user.articleprofile  # Validate it's an article user
                login(request, user)
                return redirect('article_page')
            except:
                messages.error(request, "This account is not an article profile.")
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, 'article_login.html')


def article_logout(request):
    logout(request)
    return redirect('article_login')


def article_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, 'article_register.html')

        name = request.POST['name']
        firm_name = request.POST['firm_name']
        dob = request.POST['dob']
        sro = request.POST['sro']
        state = request.POST['state']
        district = request.POST['district']
        year_of_commencement = request.POST['year_of_commencement']
        phone = request.POST['phone']
        email = request.POST['email']
        linkedin = request.POST.get('linkedin', '')

        try:
            user = User.objects.create_user(username=username, password=password)
        except IntegrityError:
            messages.error(request, "Username already exists. Please choose a different one.")
            return redirect('article_register')

        
        ArticleProfile.objects.create(
            user=user,
            name=name,
            firm_name=firm_name,
            dob=dob,
            sro=sro,
            state=state,
            district=district,
            year_of_commencement=year_of_commencement,
            phone=phone,
            email=email,
            linkedin=linkedin
        )
        return redirect('article_login')

    return render(request, 'article_register.html')

@login_required
def add_vacancy(request):
    if request.method == 'POST':
        firm_name = request.POST['firm_name']
        branch = request.POST['branch']
        other_branches = request.POST.get('other_branches', '')
        vacancies = request.POST['vacancies']
        phone = request.POST['phone']
        email = request.POST['email']
        description = request.POST['description']
        stipend = request.POST['stipend']
        website = request.POST.get('website', '')
        linkedin = request.POST.get('linkedin', '')
        share_contact = request.POST.get('share_contact') == 'on'

        # Safely get rating fields with defaults
        def get_rating(field):
            value = request.POST.get(field)
            return int(value) if value and value.isdigit() else 0

        statutory_audit_rating = get_rating('statutory_audit_rating')
        internal_audit_rating = get_rating('internal_audit_rating')
        direct_tax_rating = get_rating('direct_tax_rating')
        gst_rating = get_rating('gst_rating')
        compliance_rating = get_rating('compliance_rating')
        consultancy_rating = get_rating('consultancy_rating')
        other_specialisation = request.POST.get('other_specialisation', '')
        other_specialisation_rating = get_rating('other_specialisation_rating')

        # Duplicate check
        norm_firm = ''.join(firm_name.lower().split())
        norm_branch = ''.join(branch.lower().split())
        for v in VacancyPost.objects.all():
            if ''.join(v.firm_name.lower().split()) == norm_firm and ''.join(v.branch.lower().split()) == norm_branch:
                messages.error(request, "Vacancy for this firm and branch already exists!")
                return redirect('add_vacancy')

        # Save to DB
        VacancyPost.objects.create(
            article=request.user,
            firm_name=firm_name,
            branch=branch,
            other_branches=other_branches,
            vacancies=vacancies,
            phone=phone,
            email=email,
            description=description,
            stipend=stipend,
            website=website,
            linkedin=linkedin,
            share_contact=share_contact,
            statutory_audit_rating=statutory_audit_rating,
            internal_audit_rating=internal_audit_rating,
            direct_tax_rating=direct_tax_rating,
            gst_rating=gst_rating,
            compliance_rating=compliance_rating,
            consultancy_rating=consultancy_rating,
            other_specialisation=other_specialisation,
            other_specialisation_rating=other_specialisation_rating,
        )

        messages.success(request, "Vacancy posted successfully!")
        return redirect('article_page')

    return render(request, 'add_vacancy.html')


@login_required
def edit_vacancy(request, id):
    vacancy = get_object_or_404(VacancyPost, id=id, article=request.user)

    if request.method == 'POST':
        vacancy.firm_name = request.POST['firm_name']
        vacancy.branch = request.POST['branch']
        vacancy.other_branches = request.POST.get('other_branches', '')
        vacancy.vacancies = request.POST['vacancies']
        vacancy.phone = request.POST['phone']
        vacancy.email = request.POST['email']
        vacancy.description = request.POST['description']
        vacancy.stipend = request.POST['stipend']
        vacancy.website = request.POST.get('website', '')
        vacancy.linkedin = request.POST.get('linkedin', '')
        vacancy.share_contact = request.POST.get('share_contact') == 'on'

        def get_rating(field):
            value = request.POST.get(field)
            return int(value) if value and value.isdigit() else 0

        vacancy.statutory_audit_rating = get_rating('statutory_audit_rating')
        vacancy.internal_audit_rating = get_rating('internal_audit_rating')
        vacancy.direct_tax_rating = get_rating('direct_tax_rating')
        vacancy.gst_rating = get_rating('gst_rating')
        vacancy.compliance_rating = get_rating('compliance_rating')
        vacancy.consultancy_rating = get_rating('consultancy_rating')
        vacancy.other_specialisation = request.POST.get('other_specialisation', '')
        vacancy.other_specialisation_rating = get_rating('other_specialisation_rating')

        vacancy.save()
        messages.success(request, 'Vacancy updated successfully.')
        return redirect('article_page')

    return render(request, 'edit_vacancy.html', {'vacancy': vacancy})

@login_required
def delete_vacancy(request, id):
    vacancy = get_object_or_404(VacancyPost, id=id, article=request.user)
    vacancy.delete()
    messages.success(request, 'Vacancy deleted.')
    return redirect('article_page')


@login_required
def view_referrals(request, vacancy_id):
    vacancy = get_object_or_404(VacancyPost, id=vacancy_id, article=request.user)
    referrals = ReferralRequest.objects.filter(vacancy=vacancy)
    return render(request, 'view_referrals.html', {'vacancy': vacancy, 'referrals': referrals})

@require_POST
@login_required
def update_referral_status(request, referral_id):
    referral = get_object_or_404(ReferralRequest, id=referral_id, vacancy__article=request.user)
    new_status = request.POST.get('status')


    if new_status in dict(ReferralRequest.STATUS_CHOICES):
        referral.status = new_status
        referral.save()

        Notification.objects.create(
            user=referral.student,
            message=f"Your referral request for {referral.vacancy.firm_name} was {new_status}"
        )

        messages.success(request, "Referral status updated successfully.")
    else:
        messages.error(request, "Invalid status selected.")

    return redirect('view_referrals', vacancy_id=referral.vacancy.id)


@login_required
def notification_page(request):
    notification = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notification_page.html', {'notification': notification})

@login_required
def mark_notification_readarticle(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()


    return redirect('notification_page')