from ._anvil_designer import LexicalItem_ListTemplate
from anvil import *
import anvil.server
from ..utils import populate_content_panel, open_lexical_item, filter_by_word_class

class LexicalItem_List(LexicalItem_ListTemplate):
    def __init__(self, lexis=True, theme=False, source=False, **properties):
        self.init_components(**properties)
        self.data_lexis = None
        self.lexis = lexis
        self.theme = theme
        self.source = source
        if not lexis:
            self.drop_down.visible = False

    def explore_letter_list(self, letter):
        headwords = anvil.server.call('get_lexical_items_by_letter', letter)
        self.data_lexis = headwords
        populate_content_panel(self.grid_panel, headwords, open_lexical_item, word_class=True, is_grid=True)

    def explore_theme_list(self, letter):
        theme = anvil.server.call('get_theme_by_letter', letter)
        self.data_lexis = theme
        populate_content_panel(self.grid_panel, theme, open_lexical_item, theme=True, is_grid=True, num_columns=2, width_xs=6)

    def explore_source_list(self, letter):
        sources = anvil.server.call('explore_source_by_letter', letter)
        self.data_lexis = sources
        populate_content_panel(self.grid_panel, sources, open_lexical_item, theme=True, source=True, is_grid=True, num_columns=2, width_xs=6)

    def search_list(self, data):
        headwords = data
        self.headwords = headwords
        self.data_lexis = headwords
        populate_content_panel(self.grid_panel, headwords, open_lexical_item, word_class=True, is_grid=True)

    def link_1_click(self, **event_args):
      open_form('main')

    def search_lexical_item_button_click(self, **event_args):
        user_input = self.outlined_1.text.strip()
        user_input = user_input.upper() if self.theme or self.source else user_input.lower()

        if not user_input:
            alert("Please input the search field")
            return
        if user_input:
            results = anvil.server.call('search_in_lexical_list', self.data_lexis, user_input, self.lexis)
            if results:
                if self.lexis:
                  populate_content_panel(self.grid_panel, results, open_lexical_item, word_class=True, is_grid=True)
                elif self.theme:
                  populate_content_panel(self.grid_panel, results, open_lexical_item, theme=True, is_grid=True, num_columns=2, width_xs=6)
                elif self.source:
                  populate_content_panel(self.grid_panel, results, open_lexical_item, theme=True, source=True, is_grid=True, num_columns=2, width_xs=6)
            else:
                alert(
                    f"No results found for '{user_input}'",
                    title="Search Result"
                )


    def drop_down_change(self, **event_args):
        self.drop_down_literal.selected_value = 'All'
        filter_by_word_class(self, self.grid_panel, is_metaphor=True)

    def drop_down_literal_change(self, **event_args):
        self.drop_down.selected_value = 'All'
        filter_by_word_class(self, self.grid_panel, is_metaphor=False)




    


