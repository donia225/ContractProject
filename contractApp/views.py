
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.views import LoginView

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Redirect to the index page
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    else:
               form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'login.html'

    def form_invalid(self, form):
        messages.error(self.request, "Nom d'utilisateur ou mot de passe incorrect.")
        return super().form_invalid(form)
