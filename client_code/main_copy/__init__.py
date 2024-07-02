from ._anvil_designer import main_copyTemplate
from anvil import *
import plotly.graph_objects as go
from ..homepage import homepage

class main_copy(main_copyTemplate):
  def __init__(self, **properties):
    # 初始化组件
    self.init_components(**properties)

  def reset_button_styles(self):
    self.column_panel_2.role = 'default'
    self.column_panel_3.role = 'default'

  def button_1_click(self, **event_args):
    self.reset_button_styles()
    self.column_panel_2.role = 'elevated-card'

  def button_2_click(self, **event_args):
    self.reset_button_styles()
    self.column_panel_3.role = 'elevated-card'

  def link_3_click(self, **event_args):
      self.content_panel.clear()
      self.update_sidebar("homepage")
      self.content_panel.add_component(homepage(), full_width_row=True)
      


