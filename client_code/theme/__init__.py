from ._anvil_designer import themeTemplate
from anvil import *
import anvil.server
from ..link import link

class theme(themeTemplate):
  def __init__(self, data=None, **properties):
      # Set Form properties and Data Bindings.
      self.init_components(**properties)
      self.main_heading_id = None
      self.section_heading_id = None
      self.back_link.visible = False
      self.link_form = None
    
      if isinstance(data, int):         #section_heading_id搜索
          self.data = data
          self.update_display()
      elif isinstance(data, dict):     #确定的theme
          self.link_other_themes.set_event_handler('click', self.link_other_themes_click)
          self.link_other_themes.visible = True
          self.load_main_heading(data)
      elif isinstance(data, list):      #搜索theme的列表
          self.link_other_themes.visible = False
          self.main_heading_list(data)


  def link_other_themes_click(self, **event_args):
      if not self.link_form:
          self.link_form = link(data=None)
          self.link_panel.add_component(self.link_form)
          theme_data = {
            'main_heading_id': self.main_heading_id,
              'main_heading': self.main_heading.text
        }
          self.link_form.data = theme_data
          self.link_form.update_display()

      self.link_panel.visible = True
      self.list_panel.visible = False
      self.link_other_themes.visible = False
      self.back_link.visible = True

    
  def update_display(self):
      if self.data:
        main_heading_data, section_heading_data = anvil.server.call('get_main_heading_data', self.data)
        self.main_heading.text = main_heading_data['main_heading']
        self.main_heading_id = main_heading_data['main_heading_id']
        self.category_source.text, self.category_target.text = anvil.server.call('get_category_descriptions', main_heading_data['category_source_id'], main_heading_data['category_target_id'])
        section_heading_data = anvil.server.call('get_section_heading', main_heading_data['main_heading_id'])
        if section_heading_data:
            self.link_other_themes.set_event_handler('click', self.link_other_themes_click)
            self.link_other_themes.visible = True
            self.init_list(section_heading_data)
          
        
  def init_list(self, section_heading_data):
      for item in section_heading_data:
        # 假设 item 是一个字典，包含 'section_heading_id' 和 'section_heading' 键
        header_link = Link(text=item.get('section_heading', 'No Title'), role='title', icon='fa:chevron-right')
        header_link.tag.section_heading_id = item.get('section_heading_id')
        content_panel = ColumnPanel(visible=False)
        content_panel.tag.loaded = False
        
        # 将 content_panel 存储在 header_link 的 tag 中
        header_link.tag.content_panel = content_panel
        
        header_link.set_event_handler('click', self.header_click)
        self.list_panel.add_component(header_link)
        self.list_panel.add_component(content_panel)

  
  def header_click(self, sender, **event_args):
      # 切换内容的可见性
      content_panel = sender.tag.content_panel
      content_panel.visible = not content_panel.visible
      # 如果内容尚未加载，则加载内容
      if not content_panel.tag.loaded:
          section_heading_id = sender.tag.section_heading_id
          lexical_items = anvil.server.call('get_lexical_items', section_heading_id)

          def create_link_click_handler(headword):
            def link_click_handler(**event_args):
               self.open_lexical_item(headword)
            return link_click_handler
            
          for index, item in enumerate(lexical_items, start=1):
              content_link = Link(text=f"{index}. {item}", role='body')
              content_link.set_event_handler('click', create_link_click_handler(item))
              content_panel.add_component(content_link)
          content_panel.tag.loaded = True

  def open_lexical_item(self, user_input):
      results = anvil.server.call('search_lexical_items', user_input)
      open_form('LexicalItem', item_panel_role='elevated-card', item_panel_visibility=True, data=results)

  def main_heading_list(self, data_list):
      self.column_panel_1.visible = False
      self.list_panel.visible = True
      for index, item in enumerate(data_list, start=1):
          link = Link(text=f"{index}. {item}", role='title')
          link.tag.main_heading = item
          link.set_event_handler('click', self.main_heading_click)
          self.list_panel.add_component(link)

  def main_heading_click(self, sender, **event_args):
        main_heading = sender.tag.main_heading
        self.link_other_themes.set_event_handler('click', self.link_other_themes_click)
        self.link_other_themes.visible = True
        self.subtitle_panel.visible = True
        # Call the server function to get the main heading data
        main_heading_data = anvil.server.call('get_main_heading_data_by_heading', main_heading)
        if main_heading_data:
            self.load_main_heading(main_heading_data)
  

  def load_main_heading(self, data):
        self.column_panel_1.visible = True
        self.list_panel.clear() 
        self.data = data
        self.main_heading.text = data['main_heading']
        self.main_heading_id = data['main_heading_id']
        self.category_source.text, self.category_target.text = anvil.server.call('get_category_descriptions', data['category_source_id'], data['category_target_id'])
        section_heading_data = anvil.server.call('get_section_heading', data['main_heading_id'])
        if section_heading_data:
            self.init_list(section_heading_data)

  def back_link_click(self, **event_args):
      if self.link_form and self.link_panel.visible:
          self.link_panel.visible = False
          self.list_panel.visible = True
          self.back_link.visible = False
          self.link_other_themes.visible = True
            
        
