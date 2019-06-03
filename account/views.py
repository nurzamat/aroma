from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from .models import Node, UserProfile, Package, BonusSettings, BonusType, Bonus
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db import IntegrityError, transaction
from django.db.models import Sum


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
        inviter = request.POST.get('inviter')
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

        if inviter == '':
            return render(request, 'account/signup.html', {'alert': "Регистрируйтесь по реферальной ссылке",
                                                           'packages': packages, 'inviter': inviter})

        username_exists = User.objects.filter(username__iexact=username).exists()
        if username_exists:
            return render(request, 'account/signup.html', {'alert': "Такой логин существует в системе",
                                                           'packages': packages, 'inviter': inviter})

        inviter_node = get_object_or_404(Node, pk=int(inviter))
        is_right = False
        if tree_parent == '':
            # auto define node
            node = get_object_or_404(Node, inviter=inviter_node)
            left_node, left_count = get_tree_parent_node(node, False, 0)
            right_node, right_count = get_tree_parent_node(node, True, 0)
            if left_count > right_count:
                parent_node = right_node
                is_right = True
            else:
                parent_node = left_node
                is_right = False
        else:
            parent_node = get_object_or_404(Node, pk=int(tree_parent))
            if parent_node.children.count() > 1:
                return render(request, 'account/signup.html',
                              {'alert': "Данный tree parent занят", 'packages': packages, 'inviter': inviter})
            elif parent_node.children.count() == 1:
                child = parent_node.children.first()
                if child.is_right:
                    is_right = False
                else:
                    is_right = True

        try:
            with transaction.atomic():
                node, user, user_profile = save_registration(address, city, country, username, email, first_name,
                                                             last_name,
                                                             middle_name, package_id, packages, parent_node, password,
                                                             phone, inviter, is_right)
        except IntegrityError:
            return render(request, 'account/signup.html', {'alert': "Ошибка при регистрации", 'packages': packages,
                                                           'inviter': inviter})

        if user and user_profile and node:
            login(request, user)
            return redirect('account:home')
        else:
            return render(request, 'account/signup.html', {'alert': "Ошибка регистрации", 'packages': packages,
                                                           'inviter': inviter})
    else:
        inviter = ''
        if request.GET.get('inviter'):
            inviter = request.GET.get('inviter')
        return render(request, 'account/signup.html', {'packages': packages, 'inviter': inviter})


def get_tree_parent_node(node, is_right, count):
    try:
        child = Node.objects.get(parent=node, is_right=is_right)
    except Node.DoesNotExist:
        return node, count
    count = count + 1
    return get_tree_parent_node(child, is_right, count)


def save_registration(address, city, country, username, email, first_name, last_name, middle_name, package_id, packages,
                      parent_node, password, phone, inviter, is_right):

    user = User(username=username, email=email, first_name=first_name, last_name=last_name, is_staff=1)
    user.set_password(password)
    user.save()
    package = packages.get(pk=package_id)
    user_profile = UserProfile.objects.create(user=user, first_name=first_name, last_name=last_name,
                                              middle_name=middle_name, phone=phone, email=email, city=city,
                                              country=country, address=address, package=package)

    node = Node.objects.create(user=user, name=user.first_name + " " + user.last_name, parent=parent_node,
                               inviter=inviter, is_right=is_right)

    calculate_bonus(node, inviter)

    return node, user, user_profile


def calculate_bonus(node, inviter):
    # bonus
    if inviter:
        bonus_settings = BonusSettings.objects.all()
        bonus_types = BonusType.objects.all()
        recommendation_type = bonus_types.get(code=1)
        # step_type = bonus_types.get(code=2)
        cycle_type = bonus_types.get(code=3)

        # bonus for recommendation
        recommendation_bonus_value = bonus_settings.get(bonus_type=recommendation_type, level=1).bonus_value
        Bonus.objects.create(node=inviter, value=recommendation_bonus_value, partner=node,
                             type=recommendation_type.name)

        if inviter.bonus is None:
            inviter.bonus = recommendation_bonus_value
        else:
            inviter.bonus = inviter.bonus + recommendation_bonus_value
        inviter.save()

        # bonus for registration
        price_som = node.package.price_som
        calculate_parent_bonus(cycle_type, node, price_som)


def calculate_parent_bonus(cycle_type, node, price_som):
    is_right = node.is_right
    parent = node.parent
    if parent is None:
        return
    if is_right:
        parent.right_point = parent.right_point + parent.package.percent * price_som * 0.01
    else:
        parent.left_point = parent.left_point + parent.package.percent * price_som * 0.01
    bonus = 0
    if parent.right_point > parent.left_point:
        bonus = parent.left_point
    elif parent.right_point < parent.left_point:
        bonus = parent.right_point
    else:
        bonus = parent.right_point
    if bonus > 0:
        parent.right_point = parent.right_point - bonus
        parent.left_point = parent.left_point - bonus
        parent.bonus = parent.bonus + bonus
        parent.save()
        Bonus.objects.create(node=parent, value=bonus, partner=node,
                             type=cycle_type.name)

    return calculate_parent_bonus(cycle_type, parent, price_som)


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
    return render(request, 'account/home.html', {'node': user.node, 'user': user, 'profile': user.userprofile})


@login_required
def structure(request):
    user = request.user
    node = user.node
    nodes = node.get_descendants(include_self=True)
    return render(request, 'account/structure.html', {'node': node, 'nodes': nodes})


@login_required
def invited(request):
    user = request.user
    node = user.node
    nodes = Node.objects.filter(inviter=node)
    return render(request, 'account/invited.html', {'node': node, 'nodes': nodes})


@login_required
def invited_ajax(request):
    user = request.user
    level = int(request.GET.get('level'))
    s = 1
    ids = Node.objects.filter(inviter=user.node).values_list('inviter_id', flat=True)
    while s < level:
        s = s + 1
        ids = Node.objects.filter(inviter__pk__in=ids).values_list('inviter_id', flat=True)
    nodes = Node.objects.filter(inviter__pk__in=ids)
    return render(request, 'account/invited_ajax.html', {'nodes': nodes})


@login_required
def bonus_history(request):
    user = request.user
    node = user.node
    history = Bonus.objects.filter(node=node).order_by('-created_date')
    total_sum = Bonus.objects.filter(node=node).aggregate(Sum('value'))['value__sum'] or 0.00
    return render(request, 'account/bonus_history.html', {'node': node, 'total_sum': total_sum, 'history': history})


@login_required
def documentation(request):
    user = request.user
    return render(request, 'account/documentation.html', {'node': user.node})


@login_required
def notifications(request):
    user = request.user
    return render(request, 'account/notifications.html', {'node': user.node})
