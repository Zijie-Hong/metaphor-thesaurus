from ._anvil_designer import mapTemplate
from anvil import *
import anvil.server
from ..utils import populate_content_panel

class map(mapTemplate):
  def __init__(self, **properties):
      # Set Form properties and Data Bindings.
      self.init_components(**properties)
  
      self.source_buttons = [self.source_button_1, self.source_button_2, self.source_button_3, self.source_button_4]
      self.target_buttons = [self.target_button_1, self.target_button_2, self.target_button_3, self.target_button_4, self.target_button_5, self.target_button_6]
  
      self.selected_source = None
      self.selected_target = None
      
      for idx, button in enumerate(self.source_buttons):
          button.set_event_handler('click', self.source_button_click)
    
      for idx, button in enumerate(self.target_buttons):
          button.set_event_handler('click', self.target_button_click)

  def reset_buttons(self, buttons):
        for button in buttons:
            button.role = 'elevated-button'

  def select_button(self, button, buttons, button_type):
    if button.role == 'selected-button':
        button.role = 'elevated-button' 
        if button_type == 'source':
            self.selected_source = None
        elif button_type == 'target':
            self.selected_target = None
    else:
        self.reset_buttons(buttons)
        button.role = 'selected-button'
        if button_type == 'source':
            self.selected_source = button.text
        elif button_type == 'target':
            self.selected_target = button.text

    self.check_selection()

  def source_button_click(self, **event_args):
      clicked_button = event_args['sender']
      self.select_button(clicked_button, self.source_buttons, 'source')
  
  def target_button_click(self, **event_args):
      clicked_button = event_args['sender']
      self.select_button(clicked_button, self.target_buttons, 'target')
  
  def check_selection(self):
      if self.selected_source or self.selected_target:
          self.result_panel.clear()
          results = anvil.server.call('get_matching_headings', self.selected_source, self.selected_target)
          results_heading = [d['main_heading'] for d in results]
          if results_heading:
            populate_content_panel(self.result_panel, results_heading, self.main_heading_click)
          else:
                self.result_panel.add_component(Label(text="No matching rows found."), row=0, col_xs=0)

            
  def main_heading_click(self, sender, **event_args):
      main_heading = sender.tag.main_heading
      main_heading_data = anvil.server.call('get_main_heading_data_by_heading', main_heading)
      open_form('LexicalItem', theme_panel_role='elevated-card', item_panel_visibility=False, data =main_heading_data)
    