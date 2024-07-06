import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def search_lexical_items(headword):
    headword = headword.strip() 
    matching_rows = app_tables.lexical_items.search(english_headword=q.ilike(f"%{headword}%"))
    results = []
    for row in matching_rows:
        results.append({
            "lexical_item_id": row['lexical_item_id'],
            "section_heading_id": row['section_heading_id'],
            "english_headword": row['english_headword'],
            "word_class": row['word_class'],
            "literal_meaning": row['literal_meaning'],
            "metaphor_meaning": row['matephor_meaning'],
            "english_example_sentence": row['english_example_sentence'],
        })
    if results:
        return results
    else:
        return None