from ._anvil_designer import LexicalItem_ListTemplate
from anvil import *
import anvil.server

class LexicalItem_List(LexicalItem_ListTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
 
    def explore_list(self, letter):
        headwords = anvil.server.call('get_lexical_items_by_letter', letter)
        self._populate_grid(headwords)

    def search_list(self, data):
        self._populate_grid(data)

    def _populate_grid(self, items):
        self.grid_panel.clear()
        num_columns = 4
        
        for index, item in enumerate(sorted(items)):
            row = f"row_{index // num_columns}"
            col_xs = index % num_columns
            content_link = Link(text=f"{index+1}. {item}", role='text-link')
            content_link.set_event_handler('click', self._create_link_click_handler(item))
            self.grid_panel.add_component(content_link, row=row, col_xs=col_xs, width_xs=3)

    def _create_link_click_handler(self, item):
        def link_click_handler(**event_args):
            self.open_lexical_item(item)
        return link_click_handler

    def open_lexical_item(self, user_input):
        results = anvil.server.call('get_lexical_item_details', user_input)
        open_form('LexicalItem', item_panel_role='elevated-card', item_panel_visibility=True, data=results)
