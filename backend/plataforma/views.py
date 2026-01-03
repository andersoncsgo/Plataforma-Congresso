from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import CadastroForm

def cadastro(request):
    if request.method == "POST":
        form = CadastroForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
                first_name=form.cleaned_data["first_name"]
            )
            return redirect("login")
    else:
        form = CadastroForm()
    return render(request, "cadastro.html", {"form": form})
