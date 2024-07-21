from ._anvil_designer import ItemTemplate1Template
from anvil import *
import anvil.server
from ...entry_edit import entry_edit

class ItemTemplate1(ItemTemplate1Template):
  def __init__(self, **properties):
      # Set Form properties and Data Bindings.
      self.init_components(**properties)
      self.english_headword_label.visible = bool(self.item['english_headword'])
      self.literal_meaning_label.visible = bool(self.item['literal_meaning'])
      self.metaphor_meaning_label.visible = bool(self.item['metaphor_meaning'])
      self.english_example_sentence_label.visible = bool(self.item['english_example_sentence'])
      # Any code you write here will run before the form opens.

  def delete_entry_button_click(self, **event_args):
      if confirm(f"Are you sure you want to delete {self.item['english_headword']}?"):
          self.parent.raise_event('x-delete-entry', entry=self.item)

  def edit_entry_button_click(self, **event_args):
      entry_copy = dict(self.item)
      save_clicked = alert(
        content=entry_edit(item=entry_copy),
        title="Reiew Entry",
        large=True,
        buttons=[("Accept", True), ("Cancel", False)]
      )
      # Update the entry if the user clicks save
      if save_clicked:
        anvil.server.call('update_entry', self.item, entry_copy)
        # Now refresh the page
        self.refresh_data_bindings()
