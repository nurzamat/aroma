from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from .models import Node, UserProfile, Package
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail


def index(request):
    return render(request, 'account/login.html')


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('account:home')
        else:
            return render(request, 'account/login.html', {'alert': "Неверный логин или пароль"})
    else:
        return render(request, 'account/login.html')


def signup(request):
    if request.method == "POST":
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        parent_id = request.POST.get('parent_id')
        package_id = request.POST.get('package_id')
        password = 'kymdan2019'
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        middle_name = request.POST.get('middle_name')
        city = request.POST.get('city')
        country = request.POST.get('country')
        address = request.POST.get('address')

        user = User(username=email, email=email, first_name=first_name, last_name=last_name, is_staff=1)
        user.set_password(password)
        user.save()
        package = get_object_or_404(Package, pk=package_id)
        user_profile = UserProfile.objects.create(user=user, first_name=first_name, last_name=last_name,
                                                  middle_name=middle_name, phone=phone, email=email, city=city,
                                                  country=country, address=address, package=package)
        parent_node = get_object_or_404(Node, user__pk=int(parent_id))
        node = Node.objects.create(user=user, name=user.pk + " "+user.first_name + " " + user.username, parent=parent_node)

        if user and user_profile and node:
            login(request, user)
            send_mail(
                'Subject here',
                'Here is the message.',
                'nurzamat@gmail.com',
                ['nnr86@mail.ru'],
                fail_silently=False,
            )
            return redirect('account:home')
        else:
            packages = Package.objects.all()
            return render(request, 'account/signup.html', {'alert': "Ошибка регистрации", 'packages': packages})
    else:
        packages = Package.objects.all()
        return render(request, 'account/signup.html', {'packages': packages})


@login_required
def user_logout(request):
    logout(request)
    return redirect('account:user_login')


@login_required
def home(request):
    user = request.user
    node = get_object_or_404(Node, user=user)
    profile = get_object_or_404(UserProfile, user=user)
    return render(request, 'account/home.html', {'node': node, 'user': user, 'profile': profile})


@login_required
def structure(request):
    user = request.user
    node = user.node
    nodes = node.get_descendants(include_self=True)
    return render(request, 'account/structure.html', {'node': node, 'nodes': nodes})


@login_required
def invited(request):
    user = request.user
    node = get_object_or_404(Node, user=user)
    nodes = Node.objects.filter(user_parent=user)
    return render(request, 'account/invited.html', {'node': node, 'nodes': nodes})


@login_required
def invited_ajax(request):
    user = request.user
    level = request.GET.get('level')
    s = 1
    ids = Node.objects.filter(user_parent=user).values_list('user_id', flat=True)
    while s < int(level):
        s = s + 1
        ids = Node.objects.filter(user_parent__pk__in=ids).values_list('user_id', flat=True)
    nodes = Node.objects.filter(user__pk__in=ids)
    return render(request, 'account/invited_ajax.html', {'nodes': nodes})


@login_required
def documentation(request):
    user = request.user
    return render(request, 'account/documentation.html', {'node': user.node})


@login_required
def notifications(request):
    user = request.user
    return render(request, 'account/notifications.html', {'node': user.node})
