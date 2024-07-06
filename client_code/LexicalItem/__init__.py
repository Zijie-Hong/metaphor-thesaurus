from ._anvil_designer import LexicalItemTemplate
from anvil import *
import plotly.graph_objects as go
from ..homepage import homepage
from ..theme import theme
from ..word import word

class LexicalItem(LexicalItemTemplate):
  def __init__(self, data=None, column_panel_2_role='default', column_panel_3_role='default', panel_2_visibility=True, **properties):
    self.init_components(**properties)
    self.column_panel_2.role = column_panel_2_role
    self.column_panel_3.role = column_panel_3_role
    self.column_panel_2.visible = panel_2_visibility
    if data and len(data) > 0:
      self.column_panel_4.clear()
      self.column_panel_4.add_component(word(data=data), full_width_row=True)

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

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass




