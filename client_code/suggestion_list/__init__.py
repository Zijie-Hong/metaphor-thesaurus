from ._anvil_designer import suggestion_listTemplate
from anvil import *
import anvil.server
from ..entry_edit import entry_edit

class suggestion_list(suggestion_listTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.refresh_entries()
    self.entries_panel.set_event_handler('x-delete-entry', self.delete_entry)
    
  def refresh_entries(self):
     # Load existing entries from the Data Table, 
     # and display them in the RepeatingPanel
     entries = anvil.server.call('get_suggestion_entries')
     self.entries_panel.items = entries
     if len(entries) == 0:
          self.label_no_suggestion.visible = True
     else:
          self.label_no_suggestion.visible = False

  def delete_entry(self, entry, **event_args):
      # Delete the entry
      anvil.server.call('delete_entry', entry)
      # Refresh entry to remove the deleted entry from the Homepage
      self.refresh_entries()

  def link_suggest_click(self, **event_args):
        new_entry = {}
  
        while True:
            entry_form = entry_edit(item=new_entry)
            save_clicked = alert(
                content=entry_form,
                title="Add Entry",
                large=True,
                buttons=[("Submit", True), ("Cancel", False)]
            )
            
            if save_clicked:
                if entry_form.theme_box.selected_value:
                    entry_form.item['theme'] = anvil.server.call('get_main_heading_data_by_id', entry_form.theme_box.selected_value)
                if entry_form.section_heading_box.selected_value:
                    entry_form.item['section_heading'] = anvil.server.call('get_section_heading_data', entry_form.section_heading_box.selected_value)
                required_fields = ['english_headword', 'literal_meaning', 'metaphor_meaning', 'literal_word_class', 'metaphorical_word_class','english_example_sentence','dictionary', 'theme', 'section_heading']  # 添加所有必填字段
                empty_fields = [field for field in required_fields if not new_entry.get(field)]
                
                if empty_fields:
                    error_message = f"Please fill in these required fields: {', '.join(empty_fields)}"
                    alert(error_message)
                    continue 
                else:
                    result = anvil.server.call('add_new_lexical_item', new_entry)
                    if result['status'] == 'success':
                        alert('Suggestion submitted successfully!')                  
                        break  
                    else:
                        alert(f"Error adding entry: {result['message']}")
            else:
                break
