from ._anvil_designer import suggestion_listTemplate
from anvil import *
import anvil.server


class suggestion_list(suggestion_listTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.refresh_entries()
    self.entries_panel.set_event_handler('x-delete-entry', self.delete_entry)
    
  def refresh_entries(self):
     # Load existing entries from the Data Table, 
     # and display them in the RepeatingPanel
     self.entries_panel.items = anvil.server.call('get_entries')

  def delete_entry(self, entry, **event_args):
      # Delete the entry
      anvil.server.call('delete_entry', entry)
      # Refresh entry to remove the deleted entry from the Homepage
      self.refresh_entries()