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
                node, user, user_profile = save_registration(address, city, country, username, email, first_name,
                                                             last_name,
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
    desc_count = parent_node.get_descendant_count()
    if desc_count > 1:
        raise ValueError("Children count > 1")

    user = User(username=username, email=email, first_name=first_name, last_name=last_name, is_staff=1)
    user.set_password(password)
    user.save()
    package = packages.get(pk=package_id)
    user_profile = UserProfile.objects.create(user=user, first_name=first_name, last_name=last_name,
                                              middle_name=middle_name, phone=phone, email=email, city=city,
                                              country=country, address=address, package=package)
    is_right = False
    if desc_count == 1:
        is_right = True
    node = Node.objects.create(user=user, name=user.first_name + " " + user.last_name, parent=parent_node,
                               user_parent=user_parent, is_right=is_right)

    calculate_bonus(user, user_parent)

    return node, user, user_profile


def calculate_bonus(user, user_parent):
    # bonus
    if user_parent:
        bonus_settings = BonusSettings.objects.all()
        bonus_types = BonusType.objects.all()
        recommendation_type = bonus_types.get(code=1)
        step_type = bonus_types.get(code=2)
        cycle_type = bonus_types.get(code=3)

        inviter_node = Node.objects.get(user=user_parent)

        # bonus for recommendation
        recommendation_bonus_value = bonus_settings.get(bonus_type=recommendation_type, level=1).bonus_value
        Bonus.objects.create(user=user_parent, value=recommendation_bonus_value, partner=user,
                             type=recommendation_type.name)

        if inviter_node.bonus is None:
            inviter_node.bonus = recommendation_bonus_value
        else:
            inviter_node.bonus = inviter_node.bonus + recommendation_bonus_value

        # bonus for step
        left_count = 0
        right_count = 0

        try:
            right_child = Node.objects.get(parent=inviter_node, is_right=True)
            right_count = right_child.get_descendant_count() + 1
        except Node.DoesNotExist:
            right_child = None

        try:
            left_child = Node.objects.get(parent=inviter_node, is_right=False)
            left_count = left_child.get_descendant_count() + 1
        except Node.DoesNotExist:
            left_child = None

        if left_child and right_child:
            try:
                step_settings = bonus_settings.get(bonus_type=step_type, level=inviter_node.step + 1)
                summ_boolean = left_count + right_count >= step_settings.left + step_settings.right
                diff_boolean = abs(left_count - right_count) <= step_settings.diff
                if summ_boolean and diff_boolean:
                    Bonus.objects.create(user=user_parent, value=step_settings.bonus_value,
                                         partner=user, type=step_type.name)
                    inviter_node.bonus = inviter_node.bonus + step_settings.bonus_value
                    inviter_node.step = inviter_node.step + 1
                    # bonus for cycle
                    last_level_exist = bonus_settings.filter(bonus_type=step_type, level=inviter_node.step + 1).exists()
                    if not last_level_exist:
                        try:
                            cycle_settings = bonus_settings.get(bonus_type=cycle_type, level=inviter_node.cycle + 1)
                            Bonus.objects.create(user=user_parent, value=cycle_settings.bonus_value,
                                                 partner=user, type=cycle_type.name)
                            inviter_node.bonus = inviter_node.bonus + cycle_settings.bonus_value
                            inviter_node.cycle = inviter_node.cycle + 1
                        except BonusSettings.DoesNotExist:
                            pass
            except BonusSettings.DoesNotExist:
                pass
        inviter_node.save()


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
    level = int(request.GET.get('level'))
    s = 1
    ids = Node.objects.filter(user_parent=user).values_list('user_id', flat=True)
    while s < level:
        s = s + 1
        ids = Node.objects.filter(user_parent__pk__in=ids).values_list('user_id', flat=True)
    nodes = Node.objects.filter(user__pk__in=ids)
    return render(request, 'account/invited_ajax.html', {'nodes': nodes})


@login_required
def bonus_history(request):
    user = request.user
    node = user.node
    history = Bonus.objects.filter(user=user).order_by('-created_date')
    total_sum = Bonus.objects.all().aggregate(Sum('value'))['value__sum'] or 0.00
    return render(request, 'account/bonus_history.html', {'node': node, 'total_sum': total_sum, 'history': history})


@login_required
def documentation(request):
    user = request.user
    return render(request, 'account/documentation.html', {'node': user.node})


@login_required
def notifications(request):
    user = request.user
    return render(request, 'account/notifications.html', {'node': user.node})
