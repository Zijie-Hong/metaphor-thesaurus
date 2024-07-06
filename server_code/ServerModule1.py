import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def search_lexical_items(headword):
    headword = headword.strip() 
    matching_rows = app_tables.lexical_items.search(english_headword=headword)
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


@anvil.server.callable
def get_main_heading_data(section_heading_id):
    # 查询 section_headings 表，获取 main_heading_id
    section_heading_row = app_tables.section_headings.get(section_heading_id=section_heading_id)
    if not section_heading_row:
        return None
      
    section_heading = section_heading_row['section_heading']
    main_heading_id = section_heading_row['main_heading_id']
    
    main_heading_row = app_tables.main_headings.get(main_heading_id=main_heading_id)
    if not main_heading_row:
        return None
    
    main_heading_data = {
        "main_heading_id": main_heading_row['main_heading_id'],
        "main_heading": main_heading_row['main_heading'],
        "target_id": main_heading_row['target_id'],
        "source_id": main_heading_row['source_id'],
        "category_source_id": main_heading_row['category_source_id'],
        "category_target_id": main_heading_row['category_target_id']
    }
    
    return main_heading_data, section_heading