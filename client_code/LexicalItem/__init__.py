from ._anvil_designer import LexicalItemTemplate
from anvil import *
import plotly.graph_objects as go
from ..homepage import homepage
from ..theme import theme
from ..word import word
from ..map import map
from ..main import main


class LexicalItem(LexicalItemTemplate):
  def __init__(self, data=None, item_panel_role='default', theme_panel_role='default', item_panel_visibility=True, **properties):
      self.init_components(**properties)
      self.item_panel.role = item_panel_role
      self.theme_panel.role = theme_panel_role
      self.item_panel.visible = item_panel_visibility
      self.current_section_heading_id = None
      
      # 初始化并添加不同的表单
      if item_panel_role == 'elevated-card':
          print(data)
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

      # if isinstance(form, theme):
      #     if hasattr(self, 'word_form'):
      #       section_heading_id = self.word_form.get_current_section_heading_id()
      #       if section_heading_id != self.current_section_heading_id:  # 仅当 section_heading_id 发生变化时
      #           self.current_section_heading_id = section_heading_id  # 更新当前 section_heading_id
      #           form.data = section_heading_id
      #           form.update_display() 

      
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
          section_heading_id = self.word_form.get_data()
          if section_heading_id != self.current_section_heading_id: # 仅当 section_heading_id 发生变化时
                    self.current_section_heading_id = section_heading_id  # 更新当前 section_heading_id
                    self.theme_form.data = section_heading_id
            
      self.theme_form.update_display()
      self.show_form(self.theme_form)


  def link_3_click(self, **event_args):
      open_form('main')

  def link_2_click(self, **event_args):
      main_form = open_form('main')
      main_form.add_map_to_content_panel()





