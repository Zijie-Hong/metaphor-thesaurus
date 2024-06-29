from ._anvil_designer import Form1Template
from anvil import *

class Form1(Form1Template):

    def __init__(self, **properties):
        # 初始化组件
        self.init_components(**properties)
        # 初始化时未选中任何按钮
        self.selected_button = None

        # 确保所有按钮有点击事件处理程序
        self.button_1.set_event_handler('click', self.button_click)
        self.button_2.set_event_handler('click', self.button_click)

    def select_button(self, button):
        # 如果有按钮被选中，将其状态重置
        if self.selected_button:
            self.selected_button.role = 'sidebar-button'
        
        # 设置当前按钮为选中状态
        self.selected_button = button
        self.selected_button.role = 'sidebar-button selected'

    def button_click(self, **event_args):
        # 处理按钮点击事件
        button = event_args['sender']
        print(f"Button {button.text} clicked")  # 添加调试信息
        self.select_button(button)
