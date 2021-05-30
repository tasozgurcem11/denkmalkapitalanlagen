from django.urls import path
from denkmalgeschutztelofts import views

app_name = "denkmalgeschutztelofts"
urlpatterns = [
    path('', views.index, name="index"),
    path('angebot-anfordern/', views.angebot, name="angebot"),
    path('angebot-anfordern/kaiser-und-dicke/', views.angebot_kaiser, name="angebot_kaiser"),
    path('kaiser-dicke/', views.kaiserdicke, name="kaiserdicke"),
    # path('angebot-anfordern/<slug:location>/', views.kontakt, name="kontakt"),
    path('datenschutz/', views.datenschutz, name="datenschutz"),
    path('impressum/', views.impressum, name="impressum"),
    path('uber-uns/', views.uberuns, name="uberuns"),
    path('projekte/', views.projekter, name="projekte"),
    path('FAQ/', views.FAQ, name="faq"),
    path('kontakt/', views.kontakt, name="kontakt"),
    path('Covid-19/', views.covid, name="covid"),
    path('denkmal-afa/', views.afa, name="afa"),
    path("newsletter-abonnieren/", views.newsletter_abonnieren, name="newsletter_abonnieren"),
    path('virtual-tour-chapter-1/', views.virtual_tour1, name="virtual_tour1"),
    path('virtual-tour-chapter-2/', views.virtual_tour2, name="virtual_tour2"),
    path('virtual-tour-chapter-3/', views.virtual_tour3, name="virtual_tour3"),
    path('Rübenstraße/', views.rubenstrasse, name="rubenstrasse"),
    path('teschemacher-hof/', views.hof, name="hof"),
    path('angebot-anfordern/teschemacher-hof/', views.angebot_hof, name="angebot_hof"),
    path('angebot-anfordern/Rübenstraße/', views.angebot_rb, name="angebot_rb"),
    path('Käthe-Kollwitz-Str/', views.turm, name="turm"),
    path('angebot-anfordern/Käthe-Kollwitz-Str/', views.angebot_turm, name="angebot_turm"),

]
