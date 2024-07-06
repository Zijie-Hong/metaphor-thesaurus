from ._anvil_designer import Form1Template
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

class Form1(Form1Template):

    def __init__(self, **properties):
        # 初始化组件
        self.init_components(**properties)

