import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

def get_section_headings():
    rows = app_tables.section_headings.search()
    return [r.to_dict() for r in rows]
