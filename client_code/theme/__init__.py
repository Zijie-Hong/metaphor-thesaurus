from ._anvil_designer import themeTemplate
from anvil import *


class theme(themeTemplate):
  def __init__(self, data=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.main_heading.text=data
    print(data)

    # Any code you write here will run before the form opens.

