from ._anvil_designer import entry_editTemplate
from anvil import *
import anvil.server


class entry_edit(entry_editTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
