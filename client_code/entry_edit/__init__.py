from ._anvil_designer import entry_editTemplate
from anvil import *
import anvil.server


class entry_edit(entry_editTemplate):
  def __init__(self, edit_item=False, **properties):
    self.init_components(**properties)
    self.source_category = None
    self.target_category = None
    self.theme_box.items = []
    self.section_heading_box.items = []
    if edit_item:
            self.label_source_category.visible = False
            self.label_target_category.visible = False
            self.label_select_theme.visible = False
            self.source_category_box.visible = False
            self.target_category_box.visible = False
            self.theme_box.visible = False
            self.section_heading_box.visible = False
            self.textbox_dictionary.visible = False
            self.label_dictionary.visible = False
    else:
            self.textbox_dictionary.text = self.item.get('dictionary', ' ') 


  def source_category_box_change(self, **event_args):
      self.source_category = self.source_category_box.selected_value
      self.check_selection()
      
  def target_category_box_change(self, **event_args):
      self.target_category = self.target_category_box.selected_value
      self.check_selection()

  def check_selection(self):
      if self.source_category and self.target_category:
          self.theme_box.items = []
          self.section_heading_box.items = []
          results = anvil.server.call('get_matching_headings', self.source_category, self.target_category)
          
          self.theme_box.items = [(f"{index}. {d['main_heading']}", d['main_heading_id']) 
                                for index, d in enumerate(results, start=1)]
          self.theme_box.items = self.theme_box.items
          if not self.section_heading_box.items:
              self.theme_box_change()

  def theme_box_change(self, **event_args):
      selected_id = self.theme_box.selected_value
      if selected_id:
        section_heading_data = anvil.server.call('get_section_heading', selected_id)
        self.section_heading_box.items = [(item['section_heading'], item['section_heading_id']) 
                                  for item in section_heading_data]


  def get_data(self):
    return self.item, self.section_heading_box.selected_value

  def are_fields_filled(self):
        if not self.source_category_box.selected_value or not self.target_category_box.selected_value:
            return False
        return True

    
