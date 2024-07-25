from ._anvil_designer import homepageTemplate
from anvil import *
import anvil.server


class homepage(homepageTemplate):
  def __init__(self, **properties):
      self.init_components(**properties)
      

  def search_lexical_item_button_click(self, **event_args):
    user_input = self.outlined_1.text.strip().lower()
    if user_input:
        results = anvil.server.call('search_lexical_items', user_input)
        if results:
            open_form('main')
            main_form = get_open_form()
            main_form.search_lexical_item(results)
        else:
            alert(
                f"No results found for '{user_input}'",
                title="Search Result"
            )
    else:
        alert("Please input the search field")
  
      
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
      self.input_box_1.visible = True
      self.input_box_2.visible = False

  def radio_source_clicked(self, **event_args):
      self.label_2.visible = False
      self.input_box_1.visible = False
      self.input_box_2.visible = True

  def radio_theme_clicked(self, **event_args):
      self.label_2.visible = True
      self.input_box_1.visible = True
      self.input_box_2.visible = True




      
      





        
            
