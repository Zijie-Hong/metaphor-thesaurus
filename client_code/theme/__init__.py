from ._anvil_designer import themeTemplate
from anvil import *
import anvil.server

class theme(themeTemplate):
  def __init__(self, data=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.main_heading_id = None
    self.section_heading_id = None

    if isinstance(data, int):
        self.data = data
        self.update_display()
    elif isinstance(data, dict):
        self.load_main_heading(data)
    elif isinstance(data, list):
        self.main_heading_list(data)

  def load_main_heading(self, data):
        self.column_panel_1.visible = True
        self.column_panel.clear() 
        self.data = data
        self.main_heading.text = data['main_heading']
        self.category_source.text, self.category_target.text = anvil.server.call('get_category_descriptions', data['category_source_id'], data['category_target_id'])
        section_heading_data = anvil.server.call('get_section_heading', data['main_heading_id'])
        if section_heading_data:
            self.init_list(section_heading_data)

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
        header_link = Link(text=item.get('section_heading', 'No Title'), role='title')
        header_link.tag.section_heading_id = item.get('section_heading_id')
        content_panel = ColumnPanel(visible=False)
        content_panel.tag.loaded = False
        
        # 将 content_panel 存储在 header_link 的 tag 中
        header_link.tag.content_panel = content_panel
        
        header_link.set_event_handler('click', self.header_click)
        self.column_panel.add_component(header_link)
        self.column_panel.add_component(content_panel)

  def header_click(self, sender, **event_args):
      # 切换内容的可见性
      content_panel = sender.tag.content_panel
      content_panel.visible = not content_panel.visible
      # 如果内容尚未加载，则加载内容
      if not content_panel.tag.loaded:
          section_heading_id = sender.tag.section_heading_id
          lexical_items = anvil.server.call('get_lexical_items', section_heading_id)
          for index, item in enumerate(lexical_items, start=1):
              content_link = Link(text=f"{index}. {item}", role='body')
              content_panel.add_component(content_link)
          content_panel.tag.loaded = True

  def main_heading_list(self, data_list):
      self.column_panel_1.visible = False
      for index, item in enumerate(data_list, start=1):
          link = Link(text=f"{index}. {item}", role='title')
          link.tag.main_heading = item
          link.set_event_handler('click', self.main_heading_click)
          self.column_panel.add_component(link)

  def main_heading_click(self, sender, **event_args):
        main_heading = sender.tag.main_heading
        # Call the server function to get the main heading data
        main_heading_data = anvil.server.call('get_main_heading_data_by_heading', main_heading)
        if main_heading_data:
            self.load_main_heading(main_heading_data)