from ._anvil_designer import wordTemplate
from anvil import *
import anvil.server

class word(wordTemplate):
  def __init__(self, data=None, add_mode=False, **properties):
      self.init_components(**properties)
      self.data_list = data
      self.current_index = 0
      self.main_heading_data = None
      self.edit_mode = False
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
        
      elif self.add_mode:
            self.button_1.visible = False
            self.button_2.visible = False
            self.button_save.text = "Add Item"  # 更改保存按钮的文本     
            self.button_edit.visible = False  
            self.label_main_heading.visible = False
            self.label_section_heading.visible = False

            self.textbox_item.placeholder = 'Enter English headword'
            self.textbox_literal_meaning.placeholder = 'Enter literal meaning'
            self.textbox_word_class.placeholder = 'Enter word class'
            self.textbox_metaphor_meaning.placeholder = 'Enter metaphor meaning'
            self.textbox_english_example_sentence.placeholder = 'Enter English example sentence'

  def button_1_click(self, **event_args):
      self.current_index -= 1
      self.update_display()
          
  def button_2_click(self, **event_args):
      self.current_index += 1
      self.update_display()
  
  def button_edit_click(self, **event_args):
      password_box = TextBox(placeholder="Enter password", hide_text=True)
      result = alert(
          content=password_box,
          title="Password Required",
          buttons=[("OK", True), ("Cancel", False)],
      )
      
      if result:
          entered_password = password_box.text
          if entered_password == "123":  # 替换为您的实际密码
              self.edit_mode = True
              self.update_display()
          else:
              alert("Incorrect password. Edit mode not activated.")
          
  def button_save_click(self, **event_args):
      new_data = {
          'english_headword': self.textbox_item.text,
          'literal_meaning': self.textbox_literal_meaning.text,
          'word_class': self.textbox_word_class.text,
          'metaphor_meaning': self.textbox_metaphor_meaning.text,
          'english_example_sentence': self.textbox_english_example_sentence.text
      }
      if self.add_mode:
        # 调用添加到数据库的方法
          result = anvil.server.call('add_new_lexical_item', new_data)
          if result['status'] == 'success':
              alert("New item added successfully")
              open_form('main')
          else:
              alert(result['message'])
      else:
          data = self.data_list[self.current_index]
          new_data['lexical_item_id'] = data['lexical_item_id']
          new_data['section_heading_id'] = data['section_heading_id']
          self.data_list[self.current_index] = new_data
          result = anvil.server.call('update_data_in_database', data['lexical_item_id'], new_data)
          
          if result['status'] == 'success':
              self.edit_mode = False
              self.update_display()
              alert("Changes saved successfully")
          else:
              alert("Failed to save changes")

  def button_cancel_click(self, **event_args):
      if self.add_mode:
          open_form('main')
      else:
          self.edit_mode = False
          self.update_display()

  def get_data(self):
      if self.data_list and 0 <= self.current_index < len(self.data_list):
          return self.data_list[self.current_index].get('section_heading_id')
      return None