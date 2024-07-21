from ._anvil_designer import mainTemplate
from anvil import *
import plotly.graph_objects as go
from ..homepage import homepage
from ..map import map
import anvil.server
from ..LexicalItem_List import LexicalItem_List
from ..word import word
from ..suggestion_list import suggestion_list

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
        self.content_panel.clear()
        word_form = word(add_mode=True)
        self.content_panel.add_component(word_form, full_width_row=True)

    def link_1_click(self, **event_args):
        self.content_panel.clear()
        suggestion_list_form = suggestion_list()
        self.content_panel.add_component(suggestion_list_form, full_width_row=True)

    
        
