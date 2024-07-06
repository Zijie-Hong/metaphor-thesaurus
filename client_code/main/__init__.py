from ._anvil_designer import mainTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import plotly.graph_objects as go
from ..homepage import homepage
from ..LexicalItem import LexicalItem

class main(mainTemplate):
    def __init__(self, **properties):
        # 初始化组件
        self.init_components(**properties)
        self.content_panel.add_component(homepage(), full_width_row=True)
       

    def link_3_click(self, **event_args):
      open_form('main')

      


       




