from django.urls import path
from . import views

urlpatterns =[
    path('', views.article_page, name='article_page'),
    path('article-login', views.article_login, name='article_login'),
    path('article-logout', views.article_logout, name='article_logout'),
    path('article-register', views.article_register, name='article_register'),
    path('add-vacancy', views.add_vacancy, name='add_vacancy'),
    path('edit-vacancy/<int:id>/', views.edit_vacancy, name='edit_vacancy'),
    path('delete-vacancy/<int:id>/', views.delete_vacancy, name='delete_vacancy'),
    path('view-referrals/<int:vacancy_id>/', views.view_referrals, name='view_referrals'),
    path('update-referral-status/<int:referral_id>/', views.update_referral_status, name='update_referral_status'),
    path('article-notification/', views.notification_page, name='notification_page'),
    path('notifications/read/<int:notification_id>/', views.mark_notification_readarticle, name='mark_notification_readarticle'),

]