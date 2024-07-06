from ._anvil_designer import wordTemplate
from anvil import *


class word(wordTemplate):
  def __init__(self, data=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.data_list = data
    print(self.data_list)
    self.current_index = 0
    self.update_display()
    
  def update_display(self):
      if self.data_list and 0 <= self.current_index < len(self.data_list):
          data = self.data_list[self.current_index]
          self.label_item.text = data.get('english_headword', 'No data found')
          self.label_literal_meaning.text = data.get('literal_meaning', '')
          self.label_word_class.text = data.get('word_class', '')
          self.label_metaphor_meaning.text = data.get('metaphor_meaning', '')
          self.label_english_example_sentence.text = data.get('english_example_sentence', '')
      else:
          self.label_item.text = 'No data found'
          self.label_literal_meaning.text = ''
          self.label_word_class.text = ''
          self.label_metaphor_meaning.text = ''
          self.label_english_example_sentence.text = ''
          
  def button_1_click(self, **event_args):
      if self.current_index > 0:
          self.current_index -= 1
          self.update_display()
          
  def button_2_click(self, **event_args):
      if self.current_index < len(self.data_list) - 1:
          self.current_index += 1
          self.update_display()
 
