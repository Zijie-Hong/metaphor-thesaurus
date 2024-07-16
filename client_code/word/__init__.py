from ._anvil_designer import wordTemplate
from anvil import *
import anvil.server

class word(wordTemplate):
  def __init__(self, data=None, **properties):
    self.init_components(**properties)
    self.data_list = data
    self.current_index = 0
    self.main_heading_data = None
    self.edit_mode = False
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
          
          if self.edit_mode:
              self.button_1.visible = False
              self.button_2.visible = False

              self.label_item.visible = False
              self.textbox_item.visible = True
              self.textbox_item.text = data.get('english_headword', '')
              
              self.label_literal_meaning.visible = False
              self.textbox_literal_meaning.visible = True
              self.textbox_literal_meaning.text = data.get('literal_meaning', '')

              self.label_word_class.visible = False
              self.textbox_word_class.visible = True
              self.textbox_word_class.text = data.get('word_class', '')

              self.label_metaphor_meaning.visible = False
              self.textbox_metaphor_meaning.visible = True
              self.textbox_metaphor_meaning.text = data.get('metaphor_meaning', '')

              self.label_english_example_sentence.visible = False
              self.textbox_english_example_sentence.visible = True
              self.textbox_english_example_sentence.text = data.get('english_example_sentence', '')
          else:
              self.label_item.visible = True
              self.label_item.text = data.get('english_headword', 'No data found')
              self.textbox_item.visible = False

              self.label_literal_meaning.visible = True
              self.label_literal_meaning.text = data.get('literal_meaning', '')
              self.textbox_literal_meaning.visible = False

              self.label_word_class.visible = True
              self.label_word_class.text = data.get('word_class', '')
              self.textbox_word_class.visible = False

              self.label_metaphor_meaning.visible = True
              self.label_metaphor_meaning.text = data.get('metaphor_meaning', '')
              self.textbox_metaphor_meaning.visible = False

              self.label_english_example_sentence.visible = True
              self.label_english_example_sentence.text = data.get('english_example_sentence', '')
              self.textbox_english_example_sentence.visible = False
            
              self.button_1.visible = self.current_index > 0
              self.button_2.visible = self.current_index < len(self.data_list) - 1
            
          if data['section_heading_id']:
              self.main_heading_data, section_heading_data = anvil.server.call('get_main_heading_data', data['section_heading_id'])
              self.label_main_heading.text = self.main_heading_data['main_heading']
              self.label_section_heading.text = section_heading_data

      self.button_save.visible = self.edit_mode
      self.button_cancel.visible = self.edit_mode 
      self.button_edit.visible = not self.edit_mode
      self.label_main_heading.visible = not self.edit_mode
      self.label_section_heading.visible = not self.edit_mode
      
   
  def button_1_click(self, **event_args):
      self.current_index -= 1
      self.update_display()
          
  def button_2_click(self, **event_args):
      self.current_index += 1
      self.update_display()
  
  def button_edit_click(self, **event_args):
      self.edit_mode = True
      self.update_display()
      
  def button_save_click(self, **event_args):
      data = self.data_list[self.current_index]
      new_data = {
          'lexical_item_id': data['lexical_item_id'],
          'section_heading_id': data['section_heading_id'], 
          'english_headword': self.textbox_item.text,
          'literal_meaning': self.textbox_literal_meaning.text,
          'word_class': self.textbox_word_class.text,
          'metaphor_meaning': self.textbox_metaphor_meaning.text,
          'english_example_sentence': self.textbox_english_example_sentence.text
      }

      self.data_list[self.current_index] = new_data
      result = anvil.server.call('update_data_in_database', data['lexical_item_id'], new_data)
      
      if result['status'] == 'success':
          self.edit_mode = False
          self.update_display()
          alert("Changes saved successfully")
      else:
          alert("Failed to save changes")

  def button_cancel_click(self, **event_args):
      self.edit_mode = False
      self.update_display()

  def get_data(self):
      if self.data_list and 0 <= self.current_index < len(self.data_list):
          return self.data_list[self.current_index].get('section_heading_id')
      return None