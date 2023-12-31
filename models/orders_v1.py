from typing import List, Optional
import datetime

from pydantic import BaseModel


order_json = {
    "item_id": "123",
    "created_date": "2002-11-24 12:22",
    "pages_visited": [1, 2, "3"],
    "price": 17.22,
}


class Order(BaseModel):
    item_id: int
    created_date: Optional[datetime.datetime]
    pages_visited: List[int] = []
    price: float


# class Order:
#     def __init__(
#         self,
#         item_id: int,
#         created_date: datetime.datetime,
#         pages_visited: List[int],
#         price: float,
#     ):
#         self.item_id = item_id
#         self.created_date = created_date
#         self.pages_visited = pages_visited
#         self.price = price

#     def __str__(self):
#         return str(self.__dict__)


o = Order(**order_json)
print(o)


# Default for JSON post
# Can be done for others with mods.
def order_api(order: Order):
    pass
