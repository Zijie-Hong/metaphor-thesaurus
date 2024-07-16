from ._anvil_designer import homepageTemplate
from anvil import *
import anvil.server


class homepage(homepageTemplate):
  def __init__(self, **properties):
      self.init_components(**properties)

  def outlined_button_1_click(self, **event_args):
    user_input = self.outlined_1.text
    result = anvil.server.call('search_lexical_items', user_input)
    if result:
      open_form('LexicalItem', item_panel_role='elevated-card', item_panel_visibility=True, data =result)
    else:
      results = anvil.server.call('search_lexical_items_vague', user_input)
      if results:
        open_form('LexicalItem', item_panel_role='elevated-card', item_panel_visibility=True, data =result)
      alert("No results found.")
      
  def outlined_button_2_click(self, **event_args):
      input1 = self.input_box_1.text.strip().upper()
      input2 = self.input_box_2.text.strip().upper()

      result = anvil.server.call('search_main_headings', input1, input2)
      if result:
          open_form('LexicalItem', theme_panel_role='elevated-card', item_panel_visibility=False, data =result)
      else:
          alert("No results found.")

        
            
