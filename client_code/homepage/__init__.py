from ._anvil_designer import homepageTemplate
from anvil import *
import anvil.server
from ..utils import search_lexical_item

class homepage(homepageTemplate):
  def __init__(self, **properties):
      self.init_components(**properties)
      
  def search_lexical_item_button_click(self, **event_args):
    user_input = self.outlined_1.text.strip()
    search_lexical_item(user_input)
     
  def search_theme_button_click(self, **event_args):
      result = None
      input1 = self.input_box_1.text.strip().upper()
      input2 = self.input_box_2.text.strip().upper()
      if input1 and input2:
        result = anvil.server.call('search_by_theme', input1, input2)
      else:
        alert("Please input both fields")
        return
              
      if result:
          open_form('LexicalItem', theme_panel_role='elevated-card', item_panel_visibility=False, data=result)
      else:
          alert("No results found.")
          
  def search_target_button_click(self, **event_args):
    result = None
    input = self.target_input_box.text.strip().upper()
    if input:
        result = anvil.server.call('search_themes_by_target', input)
    else:
        alert("Please input a target")
        return
    if result:
        open_form('LexicalItem', theme_panel_role='elevated-card', item_panel_visibility=False, data=result)
    else:
        alert("No results found.")

  def search_source_button_click(self, **event_args):
    result = None
    input = self.source_input_box.text.strip().upper()
    if input:
      result = anvil.server.call('search_themes_by_source', input)
    else:
      alert("Please input a source.")
      return
    if result:
        open_form('LexicalItem', theme_panel_role='elevated-card', item_panel_visibility=False, data=result)
    else:
        alert("No results found.")




      
      





        
            
