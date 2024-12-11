from ._anvil_designer import LexicalItemTemplate
from anvil import *
import anvil.server
import plotly.graph_objects as go
from ..homepage import homepage
from ..theme import theme
from ..word import word
from ..map import map
from ..main import main
from ..suggestion_list import suggestion_list
from ..utils import search_lexical_item
from ..introduction import introduction
from ..homepage_new import homepage_new

class LexicalItem(LexicalItemTemplate):
  def __init__(self, data=None, item_panel_role='default', theme_panel_role='default', item_panel_visibility=True, **properties):
      self.init_components(**properties)
      self.item_panel.role = item_panel_role
      self.theme_panel.role = theme_panel_role
      self.item_panel.visible = item_panel_visibility
      self.current_section_heading_id = None
      
      # 初始化并添加不同的表单
      if item_panel_role == 'elevated-card':
          self.word_form = word(data=data)
          self.theme_form = theme(data=None)
          self.output_panel.add_component(self.word_form, full_width_row=True)
          self.output_panel.add_component(self.theme_form, full_width_row=True)
          # 默认显示 word_form
          self.show_form(self.word_form)

       
      elif theme_panel_role == 'elevated-card':
          self.theme_form = theme(data=data)
          self.output_panel.add_component(self.theme_form, full_width_row=True)
          self.show_form(self.theme_form)

  def show_form(self, form):
      # 隐藏所有表单
      for component in self.output_panel.get_components():
          component.visible = False
      # 显示指定的表单
      form.visible = True

  def reset_button_styles(self):
    self.item_panel.role = "default"
    self.theme_panel.role = "default"


  def button_1_click(self, **event_args):
    self.reset_button_styles()
    self.item_panel.role = "elevated-card"
    self.show_form(self.word_form)
    
  def button_2_click(self, **event_args):
      self.reset_button_styles()
      self.theme_panel.role = "elevated-card"

      if hasattr(self, 'word_form'):
            # 获取新的 section_heading_id
            new_section_heading_id = self.word_form.get_data()
            
            # 只有当 section_heading_id 发生变化时才更新数据
            if new_section_heading_id != self.current_section_heading_id:
                # 清理旧数据
                self.theme_form.clear_data()  # 需要在 theme 类中实现此方法
                
                # 更新当前 section_heading_id 和数据
                self.current_section_heading_id = new_section_heading_id
                self.theme_form.data = new_section_heading_id
                
                # 更新显示
                self.theme_form.update_display()
      self.show_form(self.theme_form)


  def link_3_click(self, **event_args):
      from ..main import main
      main_form = main()
      main_form.content_panel.clear()
      main_form.content_panel.add_component(homepage(), full_width_row=True)
      open_form(main_form)

  def link_2_click(self, **event_args):
      main_form = main()
      main_form.add_map_to_content_panel()
      open_form(main_form)
    

  def link_1_click(self, **event_args):
      main_form = main()
      main_form.content_panel.clear()
      suggestion_list_form = suggestion_list()
      main_form.content_panel.add_component(suggestion_list_form, full_width_row=True)
      open_form(main_form)


  def search_lexical_item_button_click(self, **event_args):
      user_input = self.outlined_1.text.strip().lower()
      search_lexical_item(user_input)

  def link_4_click(self, **event_args):
    open_form('introduction')

  def link_5_click(self, **event_args):
      from ..main import main
      main_form = main()
      open_form(main_form)





