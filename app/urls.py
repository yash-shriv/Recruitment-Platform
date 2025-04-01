from django.urls import path
from accounts.views import home
from . import views

urlpatterns = [
    path("search/", views.search, name="search"),
    # path("", home, name="home"),  # Homepage (handled and mapped in accounts)
    
    path("my-jobs/", views.my_jobs, name="my_jobs"),
    path("my-applications/", views.my_applications, name="my_applications"),
    
    path("create-advert/", views.create_advert, name="create_advert"),
    path("adverts/", views.list_adverts, name="list_adverts"),
    path("advert/<int:advert_id>/", views.get_advert, name="get_advert"),
    path("advert/<int:advert_id>/update/", views.update_advert, name="update_advert"),
    path("advert/<int:advert_id>/delete/", views.delete_advert, name="delete_advert"),
    path("advert/<int:advert_id>/apply/", views.apply, name="apply"),
    path("advert/<int:advert_id>/applications/", views.advert_applications, name="advert_applications"),
    path("application/<int:job_application_id>/decide/", views.decide, name="decide"),
]