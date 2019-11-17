from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate



def login_request(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = username
        user = authenticate(username=username, password=password)
        return redirect('/evaluation/')
    form = AuthenticationForm()
    return render(request=request,
                  template_name="registration/login.html",
                  context={"form": form})


