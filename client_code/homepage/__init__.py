from ._anvil_designer import homepageTemplate
from anvil import *
import anvil.server


class homepage(homepageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def outlined_button_1_click(self, **event_args):
    user_input = self.outlined_1.text
    result = anvil.server.call('search_lexical_items', user_input)
    open_form('LexicalItem', column_panel_2_role='elevated-card', panel_2_visibility=True, data =result)
    
  def outlined_button_2_click(self, **event_args):
    open_form('LexicalItem', column_panel_3_role='elevated-card', panel_2_visibility=False)
