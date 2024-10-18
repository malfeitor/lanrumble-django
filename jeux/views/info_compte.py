from django.shortcuts import render, redirect
from django.http import HttpResponse  # QueryDict,
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, password_validation

# from django.core.files.storage import FileSystemStorage
from django.utils.translation import gettext
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from os import path, remove
from datetime import timedelta
import re
import secrets
from ..models import Player, TokenResetPassword
from ..forms import ConfigColorsForm, PasswordResetForm
from .gestionnaire_erreur import gestionnaire_erreur
from .joueur_options import joueur_colors, joueur_background


validate_mail_regexp = re.compile(
    "^[0-9a-zA-Z.-_]{3,}@[0-9a-zA-Z-_]{2,}\.[a-zA-Z0-9]{2,}$"
)


@login_required(login_url="/")
@gestionnaire_erreur
def config(request):
    form_colors = ConfigColorsForm(
        instance=Player.objects.get(utilisateur=request.user.id)
    )
    password_validators = ""
    for p in password_validation.password_validators_help_texts():
        password_validators += gettext(p) + "\\n"
    return render(
        request,
        "jeux/config.html",
        {
            "colors": joueur_colors(request.user.id),
            "form_colors": form_colors,
            "background_image": joueur_background(request),
            "password_validators": re.sub(r"\'", "\\'", password_validators),
        },
    )


@gestionnaire_erreur
def change_info(request):
    if request.user.groups.filter(name="guest").exists():
        request.session["error_not_seen"] = True
        request.session[
            "error_message"
        ] += "Vous n'avez pas l'autorisation de modifier les informations.\\n"
    else:
        if (
            request.user.check_password(request.POST.get("password"))
            and request.method == "POST"
        ):
            if request.POST.get("password_new_1") != request.POST.get("password_new_1"):
                request.session[
                    "error_message"
                ] += "Les nouveaux mots de passe ne correspondent pas.\\n"
                request.session["error_not_seen"] = True
            elif (
                not request.POST.get("password_new_1") == ""
                and password_validation.validate_password(request.POST.get("password"))
                is None
            ):
                request.user.set_password(request.POST.get("password_new_1"))
                login(
                    request,
                    authenticate(
                        request,
                        username=request.user.username,
                        password=request.POST.get("password"),
                    ),
                )
                request.user.save()
                request.session["error_message"] += "Mot de passe changé.\\n"
                request.session["error_not_seen"] = True
                print("Mot de passe changé pour " + request.user.username)
            elif (
                request.POST.get("password_new_1") != ""
                and password_validation.validate_password(request.POST.get("password"))
                is not None
            ):
                request.session["error_message"] += "Nouveau mot de passe incorrect.\\n"
                request.session["error_not_seen"] = True
            if (
                validate_mail_regexp.match(request.POST.get("email"))
                and request.POST.get("email") != request.user.email
            ):
                request.user.email = request.POST.get("email")
                request.user.save()
                request.session["error_message"] += "Addresse email changée.\\n"
                request.session["error_not_seen"] = True
                print("Changement de mail pour " + request.user.username)
            elif request.POST.get("email") != request.user.email:
                request.session["error_message"] += "Addresse email incorrecte.\\n"
                request.session["error_not_seen"] = True

            form = ConfigColorsForm(
                request.POST,
                request.FILES,
                instance=Player.objects.get(utilisateur=request.user.id),
            )
            if form.is_valid():
                form.clean()
                # On supprimme le fond decran si upload d'un nouveau ou demande de le supprimmer !!
                try:
                    if not form.cleaned_data["background_file"] or not (
                        "user_" + str(request.user.id) + "/"
                    ) in str(form.cleaned_data["background_file"]):
                        remove(
                            path.join(
                                settings.MEDIA_ROOT,
                                Player.objects.get(
                                    utilisateur=request.user.id
                                ).background_file.name,
                            )
                        )
                except Exception as e:
                    print("Error : " + str(e))
                form.save()
        else:
            request.session["error_message"] += "Mot de passe actuel incorrect.\\n"
            request.session["error_not_seen"] = True
    return redirect("jeux:config")


def reset_password(request):
    if request.user.groups.filter(name="guest").exists():
        request.session["error_not_seen"] = True
        request.session[
            "error_message"
        ] += "Vous n'avez pas l'autorisation de modifier les informations.\\n"
    else:
        if request.method == "POST":
            if request.POST.get("email"):
                print("Email : " + request.POST.get("email"))
                try:
                    user_concerned = User.objects.get(email=request.POST.get("email"))
                except User.DoesNotExist:
                    return HttpResponse(200)
            else:
                print("Nom d'utilisateur : " + request.POST.get("username"))
                try:
                    user_concerned = User.objects.get(
                        username=request.POST.get("username")
                    )
                except User.DoesNotExist:
                    return HttpResponse(200)
            print("Utilisateur trouvé.")
            try:
                dt = TokenResetPassword.objects.get(utilisateur_id=user_concerned)
                if timezone.now() - dt.created > timedelta(minutes=15):
                    dt.delete()
                else:
                    return HttpResponse(200)
            except TokenResetPassword.DoesNotExist:
                pass
            token = secrets.token_urlsafe(32)
            database_line = TokenResetPassword(
                utilisateur_id=user_concerned, token=token
            )
            database_line.save()
            message_txt = f"Salut {user_concerned.username}, \nVoici le lien de reset de ton mot de passe : \n\
                            https://lanrumble.com/reset_page?token={token}\nSi tu n'a pas demandé ce mail merci de me le faire savoir.\nDes bisous, l'équipe de LANRumble."
            message_html = f"<h2>Salut {user_concerned.username},</h2></br><a href='https://lanrumble.com/reset_page?token={token}'>Voici le lien de reset de ton mot de passe</a>\
                            </br>Si tu n'a pas demandé ce mail merci de me le faire savoir.</br>Des bisous, l'équipe de LANRumble."
            send_mail(
                "[Lanrumble] Demande de réinitialisation de mot de passe.",
                message_txt,
                "root@lanrumble.com",
                [user_concerned.email],
                html_message=message_html,
            )
            return HttpResponse(200)
    return redirect("jeux:index")


@gestionnaire_erreur
def reset_page(request):
    if request.method == "GET":
        password_validators = ""
        for p in password_validation.password_validators_help_texts():
            password_validators += gettext(p) + "\\n"
        try:
            token = request.GET.get("token", False)
            token = TokenResetPassword.objects.get(token=token)
            if timezone.now() - token.created > timedelta(minutes=15):
                token.delete()
                request.session[
                    "error_message"
                ] += "Trop tard, token périmé, essaie encore.\\n"
                request.session["error_not_seen"] = True
                return redirect("jeux:index")
            else:
                form = PasswordResetForm()
                return render(
                    request,
                    "jeux/password_reset.html",
                    {
                        "form": form,
                        "password_validators": re.sub(
                            r"\'", "\\'", password_validators
                        ),
                        "token": token.token,
                    },
                )

        except TokenResetPassword.DoesNotExist:
            request.session["error_message"] += "Le token n'existe pas.\\n"
            request.session["error_not_seen"] = True
            return redirect("jeux:index")
    elif request.method == "POST":
        if request.user.groups.filter(name="guest").exists():
            request.session["error_not_seen"] = True
            request.session[
                "error_message"
            ] += "Vous n'avez pas l'autorisation de modifier les informations.\\n"
        else:
            password_validators = ""
            for p in password_validation.password_validators_help_texts():
                password_validators += gettext(p) + "\\n"
            token_post = request.POST.get("token")
            print(token_post)
            pass_1 = request.POST.get("new_password_1")
            pass_2 = request.POST.get("new_password_2")
            if pass_1 != pass_2:
                request.session[
                    "error_message"
                ] += "Les mots de passe sont différents.\\n"
                request.session["error_not_seen"] = True
                form = PasswordResetForm()
                return render(
                    request,
                    "jeux/password_reset.html",
                    {
                        "form": form,
                        "password_validators": re.sub(
                            r"\'", "\\'", password_validators
                        ),
                        "token": token_post,
                    },
                )
            try:
                if password_validation.validate_password(pass_1) is None:
                    try:
                        token = TokenResetPassword.objects.get(token=token_post)
                        if timezone.now() - token.created > timedelta(minutes=15):
                            token.delete()
                            return redirect("jeux:index")
                        user = token.utilisateur_id
                        user.set_password(pass_1)
                        user.save()
                        login(
                            request,
                            authenticate(
                                request,
                                username=token.utilisateur_id.username,
                                password=pass_1,
                            ),
                        )
                        token.delete()
                        print("Mdp de " + user.username + " changé.")
                        request.session["error_message"] += "Mot de passe changé.\\n"
                        request.session["error_not_seen"] = True
                        return redirect("jeux:index")
                    except TokenResetPassword.DoesNotExist:
                        return redirect("jeux:accueil")
            except password_validation.ValidationError as e:
                for message in e:
                    request.session["error_message"] += message + "\\n"
                request.session["error_not_seen"] = True
                form = PasswordResetForm()
                return render(
                    request,
                    "jeux/password_reset.html",
                    {
                        "form": form,
                        "password_validators": re.sub(
                            r"\'", "\\'", password_validators
                        ),
                        "token": token_post,
                    },
                )
    return render(request, "jeux/index.html")
