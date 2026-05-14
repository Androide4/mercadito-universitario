from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import redirect
from .forms import RegistroForm
from .models import Usuario


def usuario_autenticado(request):

    return request.session.get('usuario_id')

def register(request):

    if request.method == 'POST':

        form = RegistroForm(request.POST)

        if form.is_valid():

            usuario = form.save(commit=False)

            usuario.password = make_password(
                form.cleaned_data['password']
            )

            usuario.save()

            return redirect('login')

    else:

        form = RegistroForm()

    return render(request, 'accounts/register.html', {
        'form': form
    })


def login_view(request):

    if request.method == 'POST':

        correo = request.POST.get('correo')
        password = request.POST.get('password')

        try:
            usuario = Usuario.objects.get(correo=correo)

            if check_password(password, usuario.password):

                request.session['usuario_id'] = str(usuario.id)

                return redirect('interacciones:home')

            else:

                return render(request, 'accounts/login.html', {
                'error': 'Correo o contraseña incorrectos'
            })

        except Usuario.DoesNotExist:

            return render(request, 'accounts/login.html', {
                'error': 'Correo o contraseña incorrectos'
            })

    return render(request, 'accounts/login.html')


def profile(request):

    if not usuario_autenticado(request):
        return redirect('login')

    usuario_id = request.session.get('usuario_id')

    usuario = Usuario.objects.get(id=usuario_id)

    return render(request, 'accounts/profile.html', {
        'usuario': usuario
    })

def logout_view(request):

    request.session.flush()

    return redirect('login')