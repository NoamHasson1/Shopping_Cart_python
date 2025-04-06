from errors import ItemAlreadyExistsError, ItemNotExistError
from item import Item


class ShoppingCart:
    def __init__(self):

        self.products = []


    def add_item(self, item: Item):
        if item in self.products:
            raise ItemAlreadyExistsError
        else:
            self.products.append(item)

    def remove_item(self, item_name: str):
        matching_items = [item for item in self.products if item.name == item_name]
        if not matching_items:
            raise ItemNotExistError
        self.products.remove(matching_items[0])

    def get_subtotal(self) -> int:
        sum = 0
        for item in self.products:
            sum += item.price
        return sum

    def check_presence(self, item_name: str) -> bool:
        return any(item.name == item_name for item in self.products)

    def make_hashtags_list(self) -> list:
        final_hashtags = []
        for item in self.products:
            final_hashtags.append(item.hashtags)
        return final_hashtags

