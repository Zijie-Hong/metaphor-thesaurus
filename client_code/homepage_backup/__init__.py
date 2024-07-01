from ._anvil_designer import homepage_backupTemplate
from anvil import *
import plotly.graph_objects as go


class homepage_backup(homepage_backupTemplate):
  def __init__(self, **properties):
    # 初始化组件
    self.init_components(**properties)
    self.add_letter_links()

  def add_letter_links(self):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for letter in alphabet:
      link = Link(text=letter, url=f"#{letter}", role="letter-nav")
      link.tag.letter = letter
      self.column_panel_1.add_component(link)
      print(f"Added link for letter: {letter}")  # 调试输出

      print(f"Total links added: {len(self.column_panel_1.get_components())}")
