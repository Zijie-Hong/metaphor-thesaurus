from ._anvil_designer import wordTemplate
from anvil import *


class word(wordTemplate):
  def __init__(self, data=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    if data:
            self.label_1.text = data.get('english_headword', 'No data found')
    # Any code you write here will run before the form opens.
