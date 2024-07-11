from ._anvil_designer import themeTemplate
from anvil import *
import anvil.server

class theme(themeTemplate):
  def __init__(self, data=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.data = data
    self.update_display()
    
    
  def update_display(self):
      if self.data:
        main_heading_data, section_heading_data = anvil.server.call('get_main_heading_data', self.data)
        self.main_heading.text = main_heading_data['main_heading']
        self.category_source.text, self.category_target.text = anvil.server.call('get_category_descriptions', main_heading_data['category_source_id'], main_heading_data['category_target_id'])
        section_heading_data = anvil.server.call('get_section_heading', main_heading_data['main_heading_id'])
        if section_heading_data:
          self.init_list(section_heading_data)
        
  def init_list(self, section_heading_data):
      for item in section_heading_data:
            # 假设 item 是一个字典，包含 'section_heading_id' 和 'section_heading' 键
            header_link = Link(text=item.get('section_heading', 'No Title'))
            header_link.tag.section_heading_id = item.get('section_heading_id')
            header_link.set_event_handler('click', self.header_click)
            self.column_panel.add_component(header_link)
            
            content_panel = ColumnPanel(visible=False, role='content-panel')
            content_panel.tag.loaded = False  # 初始状态未加载内容
            self.column_panel.add_component(content_panel)

  def header_click(self, sender, **event_args):
      # 切换内容的可见性
        content_panel = sender.tag.content_panel
        content_panel.visible = not content_panel.visible

        # 如果内容尚未加载，则加载内容
        if not content_panel.tag.loaded:
            section_heading_id = sender.tag.section_heading_id
            lexical_items = anvil.server.call('get_lexical_items', section_heading_id)
            for item in lexical_items:
                content_link = Link(text=item)
                content_panel.add_component(content_link)
            content_panel.tag.loaded = True

