from ._anvil_designer import LexicalItem_ListTemplate
from anvil import *
import anvil.server
from ..utils import populate_content_panel, open_lexical_item

class LexicalItem_List(LexicalItem_ListTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
 
    def explore_list(self, letter):
        headwords = anvil.server.call('get_lexical_items_by_letter', letter)
        populate_content_panel(self.grid_panel, headwords, open_lexical_item, is_grid=True)

    def search_list(self, data):
        populate_content_panel(self.grid_panel, data, open_lexical_item, is_grid=True)

