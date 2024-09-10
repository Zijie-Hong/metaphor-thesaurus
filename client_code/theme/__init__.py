from ._anvil_designer import themeTemplate
from anvil import *
import anvil.server
from ..link import link
from ..utils import populate_content_panel, open_lexical_item, drop_down_change

class theme(themeTemplate):
  def __init__(self, data=None, **properties):
      # Set Form properties and Data Bindings.
      self.init_components(**properties)
      self.main_heading_id = None
      self.section_heading_id = None
      self.back_link.visible = False
      self.link_form = None
      self.data_lexis = None
      self.expanded_content_panels = []
    
      if isinstance(data, int):        
          self.data = data
          self.update_display()
      elif isinstance(data, dict):     
          self.link_other_themes.set_event_handler('click', self.link_other_themes_click)
          self.link_other_themes.visible = True
          self.load_main_heading(data)
      elif isinstance(data, list):      
          self.link_other_themes.visible = False
          self.main_heading_list(data)


  def link_other_themes_click(self, **event_args):
      if not self.link_form:
          theme_data = {
                'main_heading_id': self.main_heading_id,
                  'main_heading': self.main_heading.text
            }
          relationships = anvil.server.call('get_relationships_by_main_heading_id', theme_data['main_heading_id'])
          if relationships:
              self.link_form = link(data=relationships) 
              self.link_form.update_display()
              self.link_panel.add_component(self.link_form)
              
          else:
              alert('No relationships for this theme')
              return
      self.link_panel.visible = True
      self.list_panel.visible = False
      self.link_other_themes.visible = False
      self.back_link.visible = True
      self.drop_down.visible = False
                
    
  def update_display(self):
      if self.data:
        main_heading_data, section_heading_data = anvil.server.call('get_main_heading_data', self.data)[:2]
        self.main_heading.text = main_heading_data['main_heading']
        self.main_heading_id = main_heading_data['main_heading_id']
        self.category_source.text, self.category_target.text = main_heading_data['category_source'], main_heading_data['category_target']
        if section_heading_data:
            self.link_other_themes.set_event_handler('click', self.link_other_themes_click)
            self.link_other_themes.visible = True
            self.init_list(section_heading_data)
          
        
  def init_list(self, section_heading_data):      
      for item in section_heading_data:
        section_heading = item['section_heading']
        section_heading_id = item['section_heading_id']
    
        header_link = Link(text=section_heading, role='section-title', icon='fa:chevron-right')
        header_link.tag.section_heading_id = section_heading_id
        content_panel = ColumnPanel(visible=False)
        content_panel.tag.loaded = False
        
        header_link.tag.content_panel = content_panel
        
        header_link.set_event_handler('click', self.section_header_click)
        self.list_panel.add_component(header_link)
        self.list_panel.add_component(content_panel)

  
  def section_header_click(self, sender, **event_args):
      content_panel = sender.tag.content_panel
      content_panel.visible = not content_panel.visible

      if content_panel.visible:
            sender.icon = 'fa:chevron-down'
            self.expanded_content_panels.append(content_panel)
      else:
            sender.icon = 'fa:chevron-right'
            self.expanded_content_panels.remove(content_panel)
        
      if not content_panel.tag.loaded:
          section_heading_id = sender.tag.section_heading_id
          lexical_items = anvil.server.call('get_lexical_items', section_heading_id)
          self.data_lexis = lexical_items
          populate_content_panel(content_panel, lexical_items, open_lexical_item, word_class=True)
 

  def main_heading_list(self, data_list):
      self.column_panel_1.visible = False
      self.list_panel.visible = True
      for index, item in enumerate(data_list, start=1):
          link = Link(text=f"{index}. {item}", role='section-title')
          link.tag.main_heading = item
          link.set_event_handler('click', self.main_heading_click)
          self.list_panel.add_component(link)

  def main_heading_click(self, sender, **event_args):
        main_heading = sender.tag.main_heading
        self.link_other_themes.set_event_handler('click', self.link_other_themes_click)
        self.link_other_themes.visible = True
        self.subtitle_panel.visible = True
        main_heading_data = anvil.server.call('get_main_heading_data_by_heading', main_heading)
        if main_heading_data:
            self.load_main_heading(main_heading_data)
  
  def load_main_heading(self, data):
        self.column_panel_1.visible = True
        self.list_panel.clear() 
        self.data = data
        self.main_heading.text = data['main_heading']
        self.main_heading_id = data['main_heading_id']
        self.category_source.text, self.category_target.text = data['category_source'], data['category_target']
        section_heading_data = data['section_headings']
        if section_heading_data:
            self.init_list(section_heading_data)

  def back_link_click(self, **event_args):
      if self.link_form and self.link_panel.visible:
          self.link_panel.visible = False
          self.list_panel.visible = True
          self.back_link.visible = False
          self.link_other_themes.visible = True
          self.drop_down.visible = False

  def drop_down_change(self, **event_args):
      if self.expanded_content_panels:
        for panel in self.expanded_content_panels:
            drop_down_change(self, panel)
      else:
        alert("Please expand a section before filtering.")
            
        
