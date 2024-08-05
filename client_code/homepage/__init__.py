from ._anvil_designer import homepageTemplate
from anvil import *
import anvil.server
from ..utils import search_lexical_item

class homepage(homepageTemplate):
  def __init__(self, **properties):
      self.init_components(**properties)
      

  def search_lexical_item_button_click(self, **event_args):
    user_input = self.outlined_1.text.strip().lower()
    search_lexical_item(user_input)
  
      
  def search_theme_button_click(self, **event_args):
      result = None
      if self.radio_theme.selected:
          input1 = self.input_box_1.text.strip().upper()
          input2 = self.input_box_2.text.strip().upper()
          if input1 and input2:
            result = anvil.server.call('search_by_theme', input1, input2)
          else:
            alert("Please input both fields")
            return
      elif self.radio_target.selected:
          input = self.input_box_1.text.strip().upper()
          if input:
            result = anvil.server.call('search_themes_by_target', input)
          else:
            alert("Please input a target")
            return
      elif self.radio_source.selected:
          input = self.input_box_2.text.strip().upper()
          if input:
            result = anvil.server.call('search_themes_by_source', input)
          else:
            alert("Please input a source.")
            return
        
      if result:
          open_form('LexicalItem', theme_panel_role='elevated-card', item_panel_visibility=False, data=result)
      else:
          alert("No results found.")
          

  def radio_target_clicked(self, **event_args):
    self.label_2.visible = False
    self.column_panel_2.clear()
    self.column_panel_2.add_component(self.input_box_1)

  def radio_source_clicked(self, **event_args):
    self.label_2.visible = False
    self.column_panel_2.clear()
    self.column_panel_2.add_component(self.input_box_2)

  def radio_theme_clicked(self, **event_args):
    self.label_2.visible = True
    self.column_panel_2.clear()
    self.column_panel_2.add_component(self.input_box_1)
    self.column_panel_2.add_component(self.label_2)
    self.column_panel_2.add_component(self.input_box_2)




      
      





        
            
