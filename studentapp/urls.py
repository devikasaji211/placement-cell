from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_page, name='student_page'),
    path('student-login', views.student_login, name='student_login'),
    path('student-logout', views.student_logout, name='student_logout'),
    path('student-register', views.student_register, name='student_register'),
    path('referral-request/<int:vacancy_id>/', views.referral_request, name='referral_request'),
    path('student-referrals/', views.student_referrals, name='student_referrals'),
    path('student-notifications/', views.notifications_page, name='notifications_page'),
    path('student-notifications/read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('edit-student-profile/', views.edit_student_profile, name='edit_student_profile'),
    path('bookmark/<int:vacancy_id>/', views.toggle_bookmark, name='toggle_bookmark'),
    path('bookmarks/', views.bookmarked_vacancies, name='bookmarked_vacancies'),
    path('check-username/', views.check_username_availability, name='check_username'),
    # path('notification/open/<int:notification_id>/', views.open_notification_redirect, name='open_notification_redirect'),
]

