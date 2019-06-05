from account.models import BonusSettings, BonusType, Bonus


def calculate_bonus_test():
    print('hello')


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
        parent.right_point = parent.right_point + (parent.package.percent * price_som)/100
    else:
        parent.left_point = parent.left_point + (parent.package.percent * price_som)/100
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
        Bonus.objects.create(node=parent, value=bonus, partner=node,
                             type=cycle_type.name)
    parent.save()
    return calculate_parent_bonus(cycle_type, parent, price_som)