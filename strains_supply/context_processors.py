from strains_supply import services


def load_unreceived_supply_num(request):
    unreceived = services.count_unreceived_supply(request.user)
    return {'unreceived_supply_num': unreceived}
