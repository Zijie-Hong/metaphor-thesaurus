from ._anvil_designer import wordTemplate
from ..entry_edit import entry_edit
from anvil import *
import anvil.server
import copy 
from ..utils import check_password
class word(wordTemplate):
  def __init__(self, data=None, add_mode=False, **properties):
      self.init_components(**properties)
      self.data_list = data
      self.current_index = 0
      self.add_mode = add_mode
      self.update_display()
      if self.data_list:
          if len(self.data_list) <= 1:
              self.button_1.visible = False
              self.button_2.visible = False
          else:
              self.button_1.visible = False
              self.button_2.visible = True
          
  def update_display(self):
      if self.data_list and 0 <= self.current_index < len(self.data_list):    
          data = self.data_list[self.current_index]
          data_with_subtitle = {}
          self.button_1.visible = self.current_index > 0
          self.button_2.visible = self.current_index < len(self.data_list) - 1
          main_heading_data, section_heading_data = anvil.server.call('get_main_heading_data', data['section_heading_id'])
          data_with_subtitle['main_heading'] = main_heading_data['main_heading']
          data_with_subtitle['section_heading'] = section_heading_data[0]
          data_copy = data_with_subtitle.copy()
          data_copy.update(data)
          self.item = data_copy

      elif self.add_mode:
            self.button_1.visible = False
            self.button_2.visible = False
            self.button_save.text = "Add Item"  # 更改保存按钮的文本     
            self.button_edit.visible = False  
            self.label_main_heading.visible = False
            self.label_section_heading.visible = False

  def button_1_click(self, **event_args):
      self.current_index -= 1
      self.update_display()
          
  def button_2_click(self, **event_args):
      self.current_index += 1
      self.update_display()
  
  def button_edit_click(self, **event_args):
          result = check_password()
          if result is True:
              data = self.data_list[self.current_index]
              entry_copy = data
              save_clicked = alert(
                  content=entry_edit(item=entry_copy, hide_components=True),
                  title="Update Entry",
                  large=True,
                  buttons=[("Save", True), ("Cancel", False)]
              )
              if save_clicked:
                  anvil.server.call('update_entry', self.item, entry_copy)
                  self.data_list[self.current_index] = entry_copy
                  self.item = entry_copy
                  self.update_display()
          elif result == 'wrong':
              alert("Incorrect password. Edit mode not activated.")


  def get_data(self):
      if self.data_list and 0 <= self.current_index < len(self.data_list):
          return self.data_list[self.current_index]['section_heading_id']
      return None

