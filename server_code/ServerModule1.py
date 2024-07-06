import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

def search_lexical_items(headword):
    row = app_tables.lexical_items.get(english_headword=headword)
    if row:
        return row.to_dict()
    else:
        return None
