from ._anvil_designer import LexicalItemTemplate
from anvil import *
import plotly.graph_objects as go
from ..homepage import homepage


class LexicalItem(LexicalItemTemplate):
  def __init__(self, column_panel_2_role='default', column_panel_3_role='default', panel_2_visibility=True, **properties):
    self.init_components(**properties)
    self.column_panel_2.role = column_panel_2_role
    self.column_panel_3.role = column_panel_3_role

    self.column_panel_2.visible = panel_2_visibility

  def reset_button_styles(self):
    self.column_panel_2.role = "default"
    self.column_panel_3.role = "default"

  def button_1_click(self, **event_args):
    self.reset_button_styles()
    self.column_panel_2.role = "elevated-card"

  def button_2_click(self, **event_args):
    self.reset_button_styles()
    self.column_panel_3.role = "elevated-card"

  def link_3_click(self, **event_args):
      open_form('main')



