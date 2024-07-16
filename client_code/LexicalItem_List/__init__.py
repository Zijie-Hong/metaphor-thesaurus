from ._anvil_designer import LexicalItem_ListTemplate
from anvil import *
import anvil.server

class LexicalItem_List(LexicalItem_ListTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
 
  def setup_list(self, letter):
    headwords = anvil.server.call('get_lexical_items_by_letter', letter)
    self.grid_panel.clear()
    
    def create_link_click_handler(headword):
      def link_click_handler(**event_args):
        self.open_lexical_item(headword)
      return link_click_handler
    
    num_columns = 4 
    for index, headword in enumerate(sorted(headwords)):
      row = f"row_{index // num_columns}"
      col_xs = index % num_columns
      content_link = Link(text=f"{index+1}. {headword}", role='body')
      content_link.set_event_handler('click', create_link_click_handler(headword))
      self.grid_panel.add_component(content_link, row=row, col_xs=col_xs, width_xs=3)

  def open_lexical_item(self, user_input):
      results = anvil.server.call('search_lexical_items', user_input)
      open_form('LexicalItem', item_panel_role='elevated-card', item_panel_visibility=True, data=results)