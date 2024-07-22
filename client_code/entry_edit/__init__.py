from ._anvil_designer import entry_editTemplate
from anvil import *
import anvil.server


class entry_edit(entry_editTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.source_category = None
    self.target_category = None

    # Any code you write here will run before the form opens.

  

  def source_category_box_change(self, **event_args):
      self.source_category = self.source_category_box.selected_value
      self.check_selection()
      
  def target_category_box_change(self, **event_args):
      self.target_category = self.target_category_box.selected_value
      self.check_selection()

  def check_selection(self):
      if self.source_category and self.target_category:
          results = anvil.server.call('get_matching_headings', self.source_category, self.target_category)
          self.theme_box.items = [(f"{index}. {d['main_heading']}", d['main_heading_id']) 
                                for index, d in enumerate(results, start=1)]
          self.theme_box.items = self.theme_box.items
          selected_id = self.theme_box.selected_value 
          if selected_id:
            section_heading_data = anvil.server.call('get_section_heading', data['main_heading_id'])
            for item in section_heading_data:
              self.section_heading_box.items = [(item['section_heading'], item['section_heading_id']) for item in section_heading_data]

    
