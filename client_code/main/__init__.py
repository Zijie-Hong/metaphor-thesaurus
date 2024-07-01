from ._anvil_designer import mainTemplate
from anvil import *
import plotly.graph_objects as go
from ..homepage import homepage
from ..main_copy import main_copy

class main(mainTemplate):
    def __init__(self, **properties):
        # 初始化组件
        self.init_components(**properties)
        #self.content_panel.add_component(homepage(), full_width_row=True)
        self.content_panel.add_component(main_copy(), full_width_row=True)
       




