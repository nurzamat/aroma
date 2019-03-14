from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from .models import Node, UserProfile, Package
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db import IntegrityError, transaction


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
    packages = Package.objects.all()
    if request.method == "POST":
        parent = request.POST.get('parent')
        email_phone = request.POST.get('email_phone')
        tree_parent = request.POST.get('parent_id')
        package_id = request.POST.get('package_id')
        username = request.POST.get('username')
        password = request.POST.get('user_password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        middle_name = request.POST.get('middle_name')
        city = request.POST.get('city')
        country = request.POST.get('country')
        address = request.POST.get('address')

        if '@' in email_phone:
            email = email_phone
            phone = ''
        else:
            email = ''
            phone = email_phone

        if parent == '':
            return render(request, 'account/signup.html', {'alert': "Регистрируйтесь по реферальной ссылке",
                                                           'packages': packages, 'parent': parent})

        username_exists = User.objects.filter(username__iexact=username).exists()
        if username_exists:
            return render(request, 'account/signup.html', {'alert': "Такой логин существует в системе",
                                                           'packages': packages, 'parent': parent})

        user_parent = get_object_or_404(User, pk=int(parent))
        if tree_parent == '':
            # auto define node
            node = get_object_or_404(Node, user=user_parent)
            left_node, left_count = get_tree_parent_node(node, False, 0)
            right_node, right_count = get_tree_parent_node(node, True, 0)
            if left_count > right_count:
                parent_node = right_node
            else:
                parent_node = left_node
        else:
            parent_node = get_object_or_404(Node, pk=int(tree_parent))
            children = Node.objects.filter(parent=parent_node)
            if children and children.count() > 1:
                return render(request, 'account/signup.html',
                              {'alert': "Данный tree parent занят", 'packages': packages, 'parent': parent})

        try:
            with transaction.atomic():
                node, user, user_profile = save_registration(address, city, country, username, email, first_name, last_name,
                                                             middle_name, package_id, packages, parent_node, password,
                                                             phone, user_parent)
        except IntegrityError:
            return render(request, 'account/signup.html', {'alert': "Ошибка при регистрации", 'packages': packages,
                                                           'parent': parent})

        if user and user_profile and node:
            login(request, user)
            return redirect('account:home')
        else:
            return render(request, 'account/signup.html', {'alert': "Ошибка регистрации", 'packages': packages,
                                                           'parent': parent})
    else:
        parent = ''
        if request.GET.get('parent'):
            parent = request.GET.get('parent')
        return render(request, 'account/signup.html', {'packages': packages, 'parent': parent})


def get_tree_parent_node(node, is_right, count):
    try:
        child = Node.objects.get(parent=node, is_right=is_right)
    except Node.DoesNotExist:
        return node, count
    count = count + 1
    return get_tree_parent_node(child, is_right, count)


def save_registration(address, city, country, username, email, first_name, last_name, middle_name, package_id, packages,
                      parent_node, password, phone, user_parent):
    if parent_node.get_descendant_count() > 1:
        raise ValueError("Children count > 1")
    user = User(username=username, email=email, first_name=first_name, last_name=last_name, is_staff=1)
    user.set_password(password)
    user.save()
    package = packages.get(pk=package_id)
    user_profile = UserProfile.objects.create(user=user, first_name=first_name, last_name=last_name,
                                              middle_name=middle_name, phone=phone, email=email, city=city,
                                              country=country, address=address, package=package)
    is_right = False
    if parent_node.get_descendant_count() == 1:
        is_right = True
    node = Node.objects.create(user=user, name=user.first_name + " " + user.last_name, parent=parent_node,
                               user_parent=user_parent, is_right=is_right)
    return node, user, user_profile


def validate_username_ajax(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'Такой логин существует в системе'
    return JsonResponse(data)


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
