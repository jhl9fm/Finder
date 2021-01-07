from django.urls import path
from finder import views

app_name = 'finder'

urlpatterns = [
    path("", views.home, name="home"),
    path('events/', views.eventlist, name="eventlist"),
    path('<int:id>/', views.map, name="map"),
    path('detail/<int:id>/', views.detail, name="detail"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("logout/", views.logout, name="logout"),
    path("search/", views.search, name="search"),
    path("add_event/", views.add_event, name="add_event"),
    path("add_event/<int:id>", views.add_event, name="update_event"),
    path("event_delete/<int:id>", views.event_delete, name="event_delete"),
    path("event_list/", views.event_list, name="event_list"),
    path('registration/<int:id>/', views.reg_event, name="reg_event"),
    path("reg_list/", views.reg_list, name="reg_list"),
    path("reg_delete/<int:id>", views.reg_delete, name="reg_delete"),
]