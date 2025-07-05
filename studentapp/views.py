from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .models import StudentProfile, Notification
from articleapp.models import VacancyPost
from .models import ReferralRequest
from ca_articleship_placement.supabase_client import SUPABASE_URL, supabase, SUPABASE_BUCKET
import uuid





# Create your views here.

@login_required
def student_page(request):
    try:
        profile = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        profile = None

    vacancies = VacancyPost.objects.filter()
    unread_count = Notification.objects.filter(user=request.user, is_read=False).count()

    return render(request, 'student_page.html', {'profile': profile, 'vacancies': vacancies, 'unread_count': unread_count})
def student_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            try:
                user.studentprofile  # role check
                login(request, user)
                return redirect('student_page')
            except:
                return render(request, 'student_login.html', {'error': 'Not a student account'})
        else:
            return render(request, 'student_login.html', {'error': 'Invalid credentials'})
    return render(request, 'student_login.html')


def student_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, 'student_register.html')

        name = request.POST['name']
        dob = request.POST['dob']
        sro = request.POST['sro']
        state = request.POST['state']
        district = request.POST['district']
        phone = request.POST['phone']
        email = request.POST['email']
        linkedin = request.POST.get('linkedin', '')
        orientation = request.POST.get('orientation', '') == 'on'
        itt = request.POST.get('itt', '') == 'on'

        try:
            user = User.objects.create_user(username=username, password=password)
        except IntegrityError:
            messages.error(request, "Username already exists. Please choose a different one.")
            return redirect('student_register')

        
        profile = StudentProfile.objects.create(
            user=user,
            name=name,
            dob=dob,
            sro=sro,
            state=state,
            district=district,
            phone=phone,
            email=email,
            linkedin=linkedin,
            orientation_completed=orientation,
            itt_completed=itt,
        )
        messages.success(request, "Registration successful! Please log in.")
        return redirect('student_login')

    return render(request, 'student_register.html')


def student_logout(request):
    logout(request)
    return redirect('student_login')

@login_required
def referral_request(request, vacancy_id):
    vacancy = get_object_or_404(VacancyPost, id=vacancy_id)

    if request.method == 'POST':
        message = request.POST['message']
        resume = request.FILES['resume']
        file_name = f"{request.user.username}_{uuid.uuid4().hex}_{resume.name}"

        try:
            # Read uploaded file as bytes
            file_data = resume.read()

            # Upload to Supabase
            supabase.storage.from_(SUPABASE_BUCKET).upload(
                path=file_name,
                file=file_data,
                file_options={"content-type": resume.content_type}
            )

            # Get public URL
            resume_url = f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{file_name}"

            # Save to DB
            ReferralRequest.objects.create(
                student=request.user,
                vacancy=vacancy,
                message=message,
                resume=resume_url
            )

            Notification.objects.create(
                user=vacancy.article,
                message=f"{request.user.username} requested a referral for {vacancy.firm_name} - {vacancy.branch}"
            )

            messages.success(request, "Referral request submitted successfully.")
            return redirect('student_page')

        except Exception as e:
            print("Supabase upload failed:", e)
            messages.error(request, "There was an error uploading your resume.")
            return redirect('referral_request', vacancy_id=vacancy_id)

    return render(request, 'referral_request.html', {'vacancy': vacancy})


@login_required
def student_referrals(request):
    referrals = ReferralRequest.objects.filter(student=request.user)
    return render(request, 'student_referrals.html', {'referrals': referrals})


@login_required
def notifications_page(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notifications_page.html', {'notifications': notifications})

@login_required
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()



    return redirect('notifications_page')


@login_required
def edit_student_profile(request):
    try:
        profile = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        return redirect('student_dashboard')

    if request.method == 'POST':
        profile.name = request.POST.get('name')
        profile.dob = request.POST.get('dob')
        profile.sro = request.POST.get('sro')
        profile.state = request.POST.get('state')
        profile.district = request.POST.get('district')
        profile.phone = request.POST.get('phone')
        profile.email = request.POST.get('email')
        profile.linkedin = request.POST.get('linkedin')
        profile.orientation_completed = 'orientation_completed' in request.POST
        profile.itt_completed = 'itt_completed' in request.POST
        profile.save()
        return redirect('student_dashboard')

    return render(request, 'edit_student_profile.html', {'profile': profile})