from ._anvil_designer import NewLexicalItemTemplate
from anvil import *
import anvil.server



class NewLexicalItem(NewLexicalItemTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.add_component(Label(text='New Lexical Item Submission'))
        self.lexical_item = TextBox(placeholder="Enter lexical item")
        self.definition = TextBox(placeholder="Enter definition")
        self.example_sentence = TextBox(placeholder="Enter example sentence")
        self.submit_button = Button(text="Submit")
        self.submit_button.set_event_handler('click', self.submit_click)
        self.review_button = Button(text="Review", visible=False)  
        self.review_button.set_event_handler('click', self.review_click)
        self.status_label = Label(text='')

        self.add_component(self.lexical_item)
        self.add_component(self.definition)
        self.add_component(self.example_sentence)
        self.add_component(self.submit_button)
        self.add_component(self.review_button)
        self.add_component(self.status_label)

    def submit_click(self, **event_args):
        result = anvil.server.call('submit_lexical_item', self.lexical_item.text, self.definition.text, self.example_sentence.text)
        if result:
            self.status_label.text = "Submitted for review."
        else:
            self.status_label.text = "Submission failed."

    def review_click(self, **event_args):
        success = anvil.server.call('review_lexical_item')
        if success:
            self.status_label.text = "Item reviewed and accepted."
        else:
            self.status_label.text = "Review failed."
