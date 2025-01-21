import json
import products
from cart import dao
from products import Product


class Cart:
    def _init_(self, id: int, username: str, contents: list[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod
    def load(data):
        contents = [Product(**item) for item in data['contents']]
        return Cart(data['id'], data['username'], contents, data['cost'])


def get_cart(username: str) -> list[Product]:
    cart_details = dao.get_cart(username)
    if cart_details is None:
        return []

    # Using list comprehension and json.loads() instead of eval
    items = [json.loads(cart_detail['contents']) for cart_detail in cart_details]

    # Flattening the list of items and removing duplicates
    product_ids = {content for sublist in items for content in sublist}
    
    # Using map to get products by their ids
    products_map = {product_id: products.get_product(product_id) for product_id in product_ids}
    return [products_map[product_id] for product_id in product_ids]

def add_to_cart(username: str, product_id: int):
    dao.add_to_cart(username, product_id)

def remove_from_cart(username: str, product_id: int):
    dao.remove_from_cart(username, product_id)

def delete_cart(username: str):
    dao.delete_cart(username)