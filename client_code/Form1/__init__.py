from ._anvil_designer import Form1Template
from anvil import *

class Form1(Form1Template):

    def __init__(self, **properties):
        # 初始化组件
        self.init_components(**properties)

