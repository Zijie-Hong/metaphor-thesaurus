from ._anvil_designer import LexicalItem_ListTemplate
from anvil import *
import anvil.server
from ..utils import populate_content_panel, open_lexical_item, drop_down_change

class LexicalItem_List(LexicalItem_ListTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.headwords = None
        self.theme = None
   
 
    def explore_letter_list(self, letter):
        headwords = anvil.server.call('get_lexical_items_by_letter', letter)
        self.headwords = headwords
        populate_content_panel(self.grid_panel, headwords, open_lexical_item, word_class=True, is_grid=True)

    def explore_theme_list(self, letter):
        theme = anvil.server.call('get_theme_by_letter', letter)
        print(theme)
        self.theme = theme
        populate_content_panel(self.grid_panel, theme, open_lexical_item, word_class=True, is_grid=True)

    def search_list(self, data):
        headwords = data
        self.headwords = headwords
        populate_content_panel(self.grid_panel, headwords, open_lexical_item, word_class=True, is_grid=True)

    def link_1_click(self, **event_args):
      open_form('main')

    def search_lexical_item_button_click(self, **event_args):
        user_input = self.outlined_1.text.strip().lower()
        if user_input:
            results = anvil.server.call('search_in_lexical_list', self.headwords, user_input)
            if results:
                populate_content_panel(self.grid_panel, results, open_lexical_item, word_class=True, is_grid=True)
            else:
                alert(
                    f"No results found for '{user_input}'",
                    title="Search Result"
                )
        else:
            alert("Please input the search field")

    def drop_down_change(self, **event_args):
        drop_down_change(self, self.grid_panel)




    


