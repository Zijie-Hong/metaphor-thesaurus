from ._anvil_designer import wordTemplate
from anvil import *
import anvil.server

class word(wordTemplate):
  def __init__(self, data=None, **properties):
    self.init_components(**properties)
    self.data_list = data
    self.current_index = 0
    self.update_display()

    if len(self.data_list) <= 1:
        self.button_1.visible = False
        self.button_2.visible = False
    else:
        self.button_1.visible = False
        self.button_2.visible = True
    
  def update_display(self):
      if self.data_list and 0 <= self.current_index < len(self.data_list):
          data = self.data_list[self.current_index]
          self.label_item.text = data.get('english_headword', 'No data found')
          self.label_literal_meaning.text = data.get('literal_meaning', '')
          self.label_word_class.text = data.get('word_class', '')
          self.label_metaphor_meaning.text = data.get('metaphor_meaning', '')
          self.label_english_example_sentence.text = data.get('english_example_sentence', '')

          section_heading_id = data.get('section_heading_id')
          if section_heading_id:
            main_heading_data, section_heading_data = anvil.server.call('get_main_heading_data', section_heading_id)
            self.label_main_heading.text = main_heading_data['main_heading']
            self.label_section_heading.text = section_heading_data

      self.button_1.visible = self.current_index > 0
      self.button_2.visible = self.current_index < len(self.data_list) - 1
   
  def button_1_click(self, **event_args):
      self.current_index -= 1
      self.update_display()
          
  def button_2_click(self, **event_args):
      self.current_index += 1
      self.update_display()
 
