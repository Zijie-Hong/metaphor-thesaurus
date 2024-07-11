from ._anvil_designer import LexicalItemTemplate
from anvil import *
import plotly.graph_objects as go
from ..homepage import homepage
from ..theme import theme
from ..word import word

class LexicalItem(LexicalItemTemplate):
  def __init__(self, data=None, item_panel_role='default', theme_panel_role='default', item_panel_visibility=True, **properties):
    self.init_components(**properties)
    self.item_panel.role = item_panel_role
    self.theme_panel.role = theme_panel_role
    self.item_panel.visible = item_panel_visibility
    
    if data and len(data) > 0:
      self.column_panel_4.clear()
      # 初始化并添加不同的表单
      self.word_form = word(data=data)
      saved_data = self.word_form.main_heading_data
      self.theme_form = theme(data=saved_data)

      self.column_panel_4.add_component(self.word_form, full_width_row=True)
      self.column_panel_4.add_component(self.theme_form, full_width_row=True)

      # 默认显示 word_form
      self.show_form(self.word_form)

  def show_form(self, form):
      # 隐藏所有表单
      for component in self.column_panel_4.get_components():
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
    self.show_form(self.theme_form)
    

    
  def link_3_click(self, **event_args):
      open_form('main')

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass




