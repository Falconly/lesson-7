from django import template


register = template.Library()


@register.simple_tag()
def get_menu():
    menu = [{'title': 'Главная страница', 'url_name': 'home'},
            {'title': 'Список продуктов', 'url_name': 'list_products'},
            {'title': 'Добавить продукт', 'url_name': 'add_product'},
            {'title': 'Список покупателей', 'url_name': 'list_buyers'},
            {'title': 'Добавить покупателя', 'url_name': 'add_buyer'},
            ]
    return menu
