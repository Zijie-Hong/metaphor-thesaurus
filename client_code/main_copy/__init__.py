from ._anvil_designer import main_copyTemplate
from anvil import *
import plotly.graph_objects as go
from ..homepage import homepage


class main_copy(main_copyTemplate):
  def __init__(self, **properties):
    # 初始化组件
    self.init_components(**properties)
 
