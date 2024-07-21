from ._anvil_designer import mainTemplate
from anvil import *
import plotly.graph_objects as go
from ..homepage import homepage
from ..map import map
import anvil.server
from ..LexicalItem_List import LexicalItem_List
from ..word import word
from ..suggestion_list import suggestion_list
from ..entry_edit import entry_edit

class main(mainTemplate):
    def __init__(self, **properties):
        # 初始化组件
        self.init_components(**properties)
        self.content_panel.add_component(homepage(), full_width_row=True)
        self.add_letter_links()

      
    def link_3_click(self, **event_args):
      open_form('main')

    def link_2_click(self, **event_args):
      self.content_panel.clear()
      self.content_panel.add_component(map(), full_width_row=True)

    def add_letter_links(self):
        self.letter_links = {}
      
        # Add links for each letter
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for index, letter in enumerate(letters):
            link = Link(text=letter, align="center")
            link.set_event_handler('click', self.on_letter_click)
            self.letter_links[letter] = link
            
            # Alternate links between the two columns
            if index % 2 == 0:
                self.column_1.add_component(link)
            else:
                self.column_2.add_component(link)
        
    def on_letter_click(self, sender, **event_args):
        letter = sender.text
        self.content_panel.clear()
        lexical_item_list = LexicalItem_List()
        self.content_panel.add_component(lexical_item_list, full_width_row=True)
        lexical_item_list.explore_list(letter)

    def add_map_to_content_panel(self):
        self.content_panel.clear()
        self.content_panel.add_component(map(), full_width_row=True)
      
    def search_lexical_item(self, data):
        self.content_panel.clear()
        lexical_item_list = LexicalItem_List()
        self.content_panel.add_component(lexical_item_list, full_width_row=True)
        lexical_item_list.search_list(data)

    def link_suggest_click(self, **event_args):
        new_entry = {}
  
        while True:
        # Open an alert displaying the 'EntryEdit' Form
            entry_form = entry_edit(item=new_entry)
            save_clicked = alert(
                content=entry_form,
                title="Add Entry",
                large=True,
                buttons=[("Save", True), ("Cancel", False)]
            )
            
            # If the alert returned 'True', the save button was clicked.
            if save_clicked:
                # 检查所有必填字段
                required_fields = ['english_headword', 'literal_meaning', 'metaphor_meaning', 'word_class', 'english_example_sentence']  # 添加所有必填字段
                empty_fields = [field for field in required_fields if not new_entry.get(field)]
                
                if empty_fields:
                    # 如果有空字段，显示错误消息并重新打开表单
                    error_message = f"Please fill in all required fields: {', '.join(empty_fields)}"
                    alert(error_message)
                    continue  # 继续循环，重新显示表单
                else:
                    # 所有字段都已填写，保存条目
                    result = anvil.server.call('add_new_lexical_item', new_entry)
                    if result['status'] == 'success':
                        alert("Entry added successfully!")
                        break  # 退出循环
                    else:
                        alert(f"Error adding entry: {result['message']}")
                        # 可以选择是否继续循环或退出
            else:
                # 用户点击了取消
                break
    def link_1_click(self, **event_args):
        self.content_panel.clear()
        suggestion_list_form = suggestion_list()
        self.content_panel.add_component(suggestion_list_form, full_width_row=True)

    
        
