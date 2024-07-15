from ._anvil_designer import LexicalItem_ListTemplate
from anvil import *
import anvil.server

class LexicalItem_List(LexicalItem_ListTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.grid_panel.columns = 10 

  def setup_list(self, letter):
    headwords = anvil.server.call('get_lexical_items_by_letter', letter)
    self.grid_panel.clear()
    
    def create_link_click_handler(headword):
      def link_click_handler(**event_args):
        self.open_lexical_item(headword)
      return link_click_handler
    
    num_columns = 10
    for index, headword in enumerate(sorted(headwords)):
      row = index // num_columns
      col = index % num_columns
      content_link = Link(text=f"{index+1}. {headword}", role='body')
      content_link.set_event_handler('click', create_link_click_handler(headword))
      self.grid_panel.add_component(content_link, row=row, col=col)

  def open_lexical_item(self, user_input):
    results = anvil.server.call('search_lexical_items', user_input)
    open_form('LexicalItem', item_panel_role='elevated-card', item_panel_visibility=True, data=results)
