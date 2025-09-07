from app.schemas.item import SItemFilter
from app.crud.item import ItemDAO


def find_many_item(filters: SItemFilter):
    items = ItemDAO.find_many(filters=filters)
    return items
