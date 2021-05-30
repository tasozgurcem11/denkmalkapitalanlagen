import os

from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page

from denkmalgeschutztelofts.helpers import mail
from scheduler import forms
from django_project.settings import STATIC_URL, STATIC_DIR
from denkmalgeschutztelofts.models import Email, Kontakt


# Create your views here.
def check_newsletter_submission(request):
    # try:
    #     successful_submit = request.session["newsletter_success"]
    #     if successful_submit:
    #         request.session["newsletter_success"] = False
    # except KeyError:
    #     successful_submit = False
    #     request.session["newsletter_success"] = False
    successful_submit = False
    return successful_submit


# @cache_page(60 * 15)  # Cache the page for 15 minutes
# def index(request):
#     successful_submit = check_newsletter_submission(request)
#     return render(request, "denkmalgeschutztelofts/index.html",
#                   {"successful_submit": successful_submit})


# def index(request):
#     successful_submit = check_newsletter_submission(request)
#     return render(request, "denkmalgeschutztelofts/angebot.html")

# def index(request):
#     successful_submit = check_newsletter_submission(request)
#     return render(request, "denkmalgeschutztelofts/index.html",
#                   {"successful_submit": successful_submit})


# @cache_page(60 * 15)  # Cache the page for 15 minutes
# def kontakt(request, location=None):
#     form = forms.CustomerContactUs()
#     city_message = None
#     city_image = None
#     if location is not None:
#         locations = {
#             "dusseldorf": (
#                 "Dusseldorf message", "denkmalgeschutztelofts/images/cities/dusseldorf.jpg"),
#             "berlin": ("Berlin message", "denkmalgeschutztelofts/images/cities/berlin.jpg"),
#             "stuttgart": (
#                 "Stuttgart message", "denkmalgeschutztelofts/images/cities/stuttgart.jpg"),
#             "hamburg": ("Hamburg message", "denkmalgeschutztelofts/images/cities/hamburg.jpg"),
#         }
#         if location not in locations.keys():
#             return redirect("denkmalgeschutztelofts:kontakt")
#         else:
#             city_message = locations[location][0]
#             city_image = locations[location][1]

#     if request.method == "POST":
#         form = forms.CustomerContactUs(request.POST)
#         if form.is_valid():
#             form.save()
#         context = {"STATIC_URL": STATIC_URL, "form": form, "city_message": city_message,
#                    "city_image": city_image, "successful_submit": True}
#         return render(request, "denkmalgeschutztelofts/kontakt_2.html", context)
#     else:
#         context = {"STATIC_URL": STATIC_URL, "form": form, "city_message": city_message,
#                    "city_image": city_image, "successful_submit": False}

#     return render(request, "denkmalgeschutztelofts/kontakt_2.html", context)


def impressum(request):
    successful_submit = check_newsletter_submission(request)
    return render(request, "denkmalgeschutztelofts/impressum.html",
                  {"successful_submit": successful_submit})


def datenschutz(request):
    successful_submit = check_newsletter_submission(request)
    return render(request, "denkmalgeschutztelofts/datenschutz.html",
                  {"successful_submit": successful_submit})


def uberuns(request):
    successful_submit = check_newsletter_submission(request)
    return render(request, "denkmalgeschutztelofts/uber-uns.html",
                  {"successful_submit": successful_submit})

def FAQ(request):
    return render(request, "denkmalgeschutztelofts/FAQ.html")

def covid(request):
    return render(request, "denkmalgeschutztelofts/covid.html")


def kaiserdicke(request):
    successful_submit = check_newsletter_submission(request)
    if request.method == "POST":
        email = "not given"
        vorname = "not given"
        nachname = "not given"
        nachricht = "not given"
        vorname = request.POST.get("vorname")
        nachname = request.POST.get("nachname")
        email = request.POST.get("email")
        telefon = request.POST.get("full_id_phone_number")
        nachricht = request.POST.get("nachricht")
        o_ref = Kontakt(email=email, vorname=vorname, nachname=nachname, telefon=telefon, nachricht=nachricht,
                        quelle="KD")
        o_ref.save()
        # pdf_file = os.path.join(STATIC_DIR, "pdf", "KDB_INNEN_240x288_200710.pdf")
        # mail.send_pdf(request.POST['email'], pdf_file)
        successful_submit = True
    return render(request, "denkmalgeschutztelofts/kaiserdicke.html",
                  {"successful_submit": successful_submit})

def rubenstrasse(request):
    if request.method == "POST":
        email = "not given"
        vorname = "not given"
        nachname = "not given"
        vorname = request.POST.get("vorname")
        nachname = request.POST.get("nachname")
        email = request.POST.get("email")
        telefon = request.POST.get("full_id_phone_number")
        nachricht = request.POST.get("nachricht")
        o_ref = Kontakt(email=email, vorname=vorname, nachname=nachname, nachricht=nachricht, telefon=telefon,
                        quelle="RB")
        o_ref.save()
        return render(request, "denkmalgeschutztelofts/rubenstrasse.html",
                      {'successful_submit': True})
    else:
        return render(request, "denkmalgeschutztelofts/rubenstrasse.html")

def turm(request):
    if request.method == "POST":
        email = "not given"
        vorname = "not given"
        nachname = "not given"
        vorname = request.POST.get("vorname")
        nachname = request.POST.get("nachname")
        email = request.POST.get("email")
        telefon = request.POST.get("full_id_phone_number")
        nachricht = request.POST.get("nachricht")
        o_ref = Kontakt(email=email, vorname=vorname, nachname=nachname, nachricht=nachricht, telefon=telefon,
                        quelle="TU")
        o_ref.save()
        return render(request, "denkmalgeschutztelofts/turm.html",
                      {'successful_submit': True})
    else:
        return render(request, "denkmalgeschutztelofts/turm.html")

def hof(request):
    if request.method == "POST":
        email = "not given"
        vorname = "not given"
        nachname = "not given"
        vorname = request.POST.get("vorname")
        nachname = request.POST.get("nachname")
        email = request.POST.get("email")
        telefon = request.POST.get("full_id_phone_number")
        nachricht = request.POST.get("nachricht")
        o_ref = Kontakt(email=email, vorname=vorname, nachname=nachname, nachricht=nachricht, telefon=telefon,
                        quelle="TH")
        o_ref.save()
        return render(request, "denkmalgeschutztelofts/hof.html",
                      {'successful_submit': True})
    else:
        return render(request, "denkmalgeschutztelofts/hof.html")


def afa(request):
    successful_submit = check_newsletter_submission(request)
    return render(request, "denkmalgeschutztelofts/afa.html",
                  {"successful_submit": successful_submit})


def projekter(request):
    successful_submit = check_newsletter_submission(request)
    return render(request, "denkmalgeschutztelofts/projekter.html",
                  {"successful_submit": successful_submit})

def virtual_tour1(request):
    successful_submit = check_newsletter_submission(request)
    return render(request, "denkmalgeschutztelofts/virtual_tour1.html",
                  {"successful_submit": successful_submit})
def virtual_tour2(request):
    successful_submit = check_newsletter_submission(request)
    return render(request, "denkmalgeschutztelofts/virtual_tour2.html",
                  {"successful_submit": successful_submit})
def virtual_tour3(request):
    successful_submit = check_newsletter_submission(request)
    return render(request, "denkmalgeschutztelofts/virtual_tour3.html",
                  {"successful_submit": successful_submit})


# functions with forms below:

def newsletter_abonnieren(request):
    if request.method == "POST":
        email = "not given"
        email = request.POST["email"]
        try:
            vorname = request.POST["vorname"]
            nachname = request.POST["nachname"]
            o_ref = Kontakt(email=email, vorname=vorname, nachname=nachname, quelle="NS")
            o_ref.save()
            successful_submit = True
        except KeyError:
            vorname = "not given"
            nachname = "not given"
            successful_submit = False
        context = {"email": email, "submit": True, "successful_submit": successful_submit}
        return render(request, "denkmalgeschutztelofts/newsletter.html", context)
    else:
        return render(request, "denkmalgeschutztelofts/newsletter.html")


def kontakt(request):
    if request.method == "POST":
        email = "not given"
        vorname = "not given"
        nachname = "not given"
        vorname = request.POST.get("vorname")
        nachname = request.POST.get("nachname")
        email = request.POST.get("email")
        telefon = request.POST.get("full_id_phone_number")
        nachricht = request.POST.get("nachricht")
        o_ref = Kontakt(email=email, vorname=vorname, nachname=nachname, telefon=telefon,
                        nachricht=nachricht, quelle="KT")
        o_ref.save()
        return render(request, "denkmalgeschutztelofts/kontakt_2.html", {'successful_submit': True})
    else:
        return render(request, "denkmalgeschutztelofts/kontakt_2.html")

def index(request):
    if request.method == "POST":
        email = "not given"
        vorname = "not given"
        nachname = "not given"
        vorname = request.POST.get("vorname")
        nachname = request.POST.get("nachname")
        email = request.POST.get("email")
        telefon = request.POST.get("full_id_phone_number")
        nachricht = request.POST.get("nachricht")
        o_ref = Kontakt(email=email, vorname=vorname, nachname=nachname, telefon=telefon,
                        nachricht=nachricht, quelle="IN")
        o_ref.save()
        return render(request, "denkmalgeschutztelofts/index.html", {'successful_submit': True})
    else:
        return render(request, "denkmalgeschutztelofts/index.html")


def angebot_kaiser(request):
    if request.method == "POST":
        email = "not given"
        vorname = "not given"
        nachname = "not given"
        vorname = request.POST.get("vorname")
        nachname = request.POST.get("nachname")
        email = request.POST.get("email")
        telefon = request.POST.get("full_id_phone_number")
        nachricht = request.POST.get("nachricht")
        o_ref = Kontakt(email=email, vorname=vorname, nachname=nachname, nachricht=nachricht, telefon=telefon,
                        quelle="AK")
        o_ref.save()
        return render(request, "denkmalgeschutztelofts/angebot_kaiser.html",
                      {'successful_submit': True})
    else:
        return render(request, "denkmalgeschutztelofts/angebot_kaiser.html")

def angebot_rb(request):
    if request.method == "POST":
        email = "not given"
        vorname = "not given"
        nachname = "not given"
        vorname = request.POST.get("vorname")
        nachname = request.POST.get("nachname")
        email = request.POST.get("email")
        telefon = request.POST.get("full_id_phone_number")
        nachricht = request.POST.get("nachricht")
        o_ref = Kontakt(email=email, vorname=vorname, nachname=nachname, nachricht=nachricht, telefon=telefon,
                        quelle="AR")
        o_ref.save()
        return render(request, "denkmalgeschutztelofts/angebot_rb.html",
                      {'successful_submit': True})
    else:
        return render(request, "denkmalgeschutztelofts/angebot_rb.html")

def angebot_turm(request):
    if request.method == "POST":
        email = "not given"
        vorname = "not given"
        nachname = "not given"
        vorname = request.POST.get("vorname")
        nachname = request.POST.get("nachname")
        email = request.POST.get("email")
        telefon = request.POST.get("full_id_phone_number")
        nachricht = request.POST.get("nachricht")
        o_ref = Kontakt(email=email, vorname=vorname, nachname=nachname, nachricht=nachricht, telefon=telefon,
                        quelle="AM")
        o_ref.save()
        return render(request, "denkmalgeschutztelofts/angebot_turm.html",
                      {'successful_submit': True})
    else:
        return render(request, "denkmalgeschutztelofts/angebot_turm.html")

def angebot_hof(request):
    if request.method == "POST":
        email = "not given"
        vorname = "not given"
        nachname = "not given"
        vorname = request.POST.get("vorname")
        nachname = request.POST.get("nachname")
        email = request.POST.get("email")
        telefon = request.POST.get("full_id_phone_number")
        nachricht = request.POST.get("nachricht")
        o_ref = Kontakt(email=email, vorname=vorname, nachname=nachname, nachricht=nachricht, telefon=telefon,
                        quelle="AT")
        o_ref.save()
        return render(request, "denkmalgeschutztelofts/angebot_hof.html",
                      {'successful_submit': True})
    else:
        return render(request, "denkmalgeschutztelofts/angebot_hof.html")


def angebot(request):
    if request.method == "POST":
        email = "not given"
        vorname = "not given"
        nachname = "not given"
        vorname = request.POST.get("vorname")
        nachname = request.POST.get("nachname")
        email = request.POST.get("email")
        telefon = request.POST.get("full_id_phone_number")
        nachricht = request.POST.get("nachricht")
        o_ref = Kontakt(email=email, vorname=vorname, nachname=nachname, telefon=telefon, nachricht=nachricht,
                        quelle="AN")
        o_ref.save()
        return render(request, "denkmalgeschutztelofts/angebot.html", {'successful_submit': True})
    else:
        return render(request, "denkmalgeschutztelofts/angebot.html")


def projekte(request):
    if request.method == "POST":
        email = "not given"
        vorname = "not given"
        nachname = "not given"
        vorname = request.POST.get("vorname")
        nachname = request.POST.get("nachname")
        email = request.POST.get("email")
        o_ref = Kontakt(email=email, vorname=vorname, nachname=nachname)
        o_ref.save()
        return redirect("denkmalgeschutztelofts:index")
    else:
        return render(request, "denkmalgeschutztelofts/projekte.html")
