from django import template


register = template.Library()


@register.simple_tag()
def get_menu():
    menu = [{'title': 'Главная страница', 'url_name': 'modelsapp:home'},
            {'title': 'Список продуктов', 'url_name': 'modelsapp:list_products'},
            {'title': 'Добавить продукт', 'url_name': 'modelsapp:add_product'},
            {'title': 'Список покупателей', 'url_name': 'modelsapp:list_buyers'},
            {'title': 'Добавить покупателя', 'url_name': 'modelsapp:add_buyer'},
            ]
    return menu
