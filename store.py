import yaml

from errors import ItemNotExistError, TooManyMatchesError, ItemAlreadyExistsError
from item import Item
from shopping_cart import ShoppingCart

class Store:
    def __init__(self, path):
        with open(path) as inventory:
            items_raw = yaml.load(inventory, Loader=yaml.FullLoader)['items']
        self._items = self._convert_to_item_objects(items_raw)
        self._shopping_cart = ShoppingCart()

    @staticmethod
    def _convert_to_item_objects(items_raw):
        return [Item(item['name'],
                     int(item['price']),
                     item['hashtags'],
                     item['description'])
                for item in items_raw]

    def get_items(self) -> list:
        return self._items


    def sorting_ResList(self, resList1: list) -> list:
        tagList1 = [tag for item in self._shopping_cart.products for tag in item.hashtags]
        final_resList = sorted(resList1, key=lambda item: (-sum(tagList1.count(hashtag) for hashtag in item.hashtags), item.name))
        return final_resList

    def check_availability(self, item_name: str):
        check = 0
        if not item_name:
            raise TooManyMatchesError
        for item in self._items:
            if item.name == item_name:
                check += 1
        if check == 0:
            raise ItemNotExistError
        if check > 1:
            raise TooManyMatchesError


    def search_by_name(self, item_name: str) -> list:
        resList1 = []
        if not item_name:
            resList1 = [item for item in self._items if item not in self._shopping_cart.products]
        else:
            resList1 = [item for item in self._items if item_name in item.name and not self._shopping_cart.check_presence(item.name)]

        final_list = self.sorting_ResList(resList1)
        return final_list

    def search_by_hashtag(self, hashtag: str) -> list:
        resList2 = []
        resList3 = []
        for item in self._items:
            if hashtag in item.hashtags and not self._shopping_cart.check_presence(item.name):
                resList2.append(item)
        for item in resList2:
            if hashtag in item.hashtags:
                resList3.append(item)
        final_list = self.sorting_ResList(resList3)
        return final_list

    def add_item(self, item_name: str):
        if not item_name:
            raise TooManyMatchesError
        self.check_availability(item_name)
        if self._shopping_cart.check_presence(item_name):
            raise ItemAlreadyExistsError
        matching_items = [item for item in self._items if item_name in item.name]
        if len(matching_items) > 1:
            raise TooManyMatchesError
        self._shopping_cart.add_item(matching_items[0])

    def remove_item(self, item_name: str):
        matching_items = [item for item in self._shopping_cart.products if item_name in item.name]
        if not matching_items:
            raise ItemNotExistError
        if len(matching_items) > 1:
            raise TooManyMatchesError
        self._shopping_cart.remove_item(matching_items[0].name)

    def checkout(self) -> int:
        sum_total = 0
        for item in self._shopping_cart.products:
            sum_total += item.price
        return sum_total
