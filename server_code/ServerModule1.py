import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime
from functools import lru_cache
import itertools

@lru_cache(maxsize=128)
@anvil.server.callable
def search_lexical_items(input_original):
    input = input_original.lower()
    input_capitalized = input_original.capitalize()
    def create_queries(word):
        return [
            f'% {word} %',    # 单词在中间
            f'{word} %',      # 单词在开头
            f'% {word}',      # 单词在结尾
            f'{word}',        # 精确匹配
            f'%-{word}-%',    # 词在连字符之间
            f'%-{word} %',    # 词在连字符之后，句子中间
            f'%-{word}',      # 词在连字符之后，句尾
            f'{word}-%'       # 词在连字符之前
        ]
    
    # 生成所有可能的查询（小写和首字母大写）
    queries = create_queries(input) + create_queries(input_capitalized)
    
    # 进行首次搜索
    matching_rows = app_tables.lexical_items.search(
        english_headword=q.any_of(
            *[q.like(query) for query in queries]
        )
    )
   
    results = list(set((row['english_headword'], row['metaphorical_word_class']) for row in matching_rows)) or None
    if not results:
      query1 = f'%{input_original}%'  # 模糊匹配
      query2 = f'{input_original}'    # 精确匹配
      
      matching_rows = app_tables.lexical_items.search(
          english_headword=q.any_of(
              q.like(query1),
              q.like(query2)
          )
      )
      results = list(set((row['english_headword'], row['metaphorical_word_class']) 
                          for row in matching_rows))
    
    return results or None
      

def search_with_connectors(input1: str, input2: str, connectors: list) -> list:
    results = []
    for connector in connectors:
        query = f'%{input1}% {connector} %{input2}%'
        matching_rows = app_tables.main_headings.search(main_heading=q.like(query))
        if matching_rows is not None:
            results.extend(row['main_heading'] for row in matching_rows)
    return list(set(results)) or None

@anvil.server.callable
def search_by_theme(input1: str, input2: str) -> list:
    return search_with_connectors(input1, input2, ['IS', 'ARE'])

@anvil.server.callable
def search_themes_by_target(input: str) -> list:
    return search_with_connectors(input, '', ['IS', 'ARE'])

@anvil.server.callable
def search_themes_by_source(input: str) -> list:
    return search_with_connectors('', input, ['IS', 'ARE'])

@anvil.server.callable
def get_theme_by_letter(letter):
    results = app_tables.main_headings.search(
        main_heading=q.ilike(letter + '%')
    )

    sorted_results = sorted(results, key=lambda x: x['main_heading'])
    return [theme['main_heading'] for theme in sorted_results]

@anvil.server.callable
def explore_source_by_letter(letter):
    results = app_tables.sources.search(
        source=q.ilike(letter + '%')
    )
    combinations = []

    for item in results:
        source_identifier = str(item['source']) 
        matching_rows = app_tables.main_headings.search(source_id=item)

        target_ids = set()
        for row in matching_rows:
            target_identifier = row['target_id']['target'] 
            target_ids.add(str(target_identifier)) 
        
        for target_id in target_ids:
            combinations.append((source_identifier, target_id))
    combinations = sorted(combinations, key=lambda x: (x[0], x[1]))
    return combinations

  
@anvil.server.callable
def get_main_heading_data(section_heading_id):
    section_heading_row = app_tables.section_headings.get(section_heading_id=section_heading_id)
    if section_heading_row is None:
        raise ValueError("Section heading not found")

    main_heading_rows = app_tables.main_headings.search(main_heading_id=section_heading_row['main_heading_id'])

    if not main_heading_rows:
        raise ValueError("Main heading not found")
    main_heading_row = main_heading_rows[0] 
    main_heading_data = {
        "main_heading_id": main_heading_row['main_heading_id'],
        "main_heading": main_heading_row['main_heading'],
        "category_source": main_heading_row['category_source_id']['category_source'],
        "category_target": main_heading_row['category_target_id']['category_target'],
        "section_headings": main_heading_row['section_heading_ids']
    }
    return main_heading_data, main_heading_data["section_headings"], dict(section_heading_row)


@anvil.server.callable
def get_main_heading_data_by_heading(main_heading):
    row = next(iter(app_tables.main_headings.search(main_heading=main_heading)), None)
    if row:
        return {
            "main_heading_id": row['main_heading_id'],
            "main_heading": row['main_heading'],
            "category_source": row['category_source_id']['category_source'],
            "category_target": row['category_target_id']['category_target'],
            "section_headings": row['section_heading_ids']
        }
    return None
  
@lru_cache(maxsize=128)
@anvil.server.callable
def get_main_heading_data_by_vague_source(parts):
    part1, part2 = parts[0], parts[1]
    source_row = app_tables.sources.get(source=part1)
    target_row = app_tables.targets.get(target=part2)
    row = next(iter(app_tables.main_headings.search(
        source_id=source_row,
        target_id=target_row
    )), None)
    if row:
            return {
                "main_heading_id": row['main_heading_id'],
                "main_heading": row['main_heading'],
                "category_source": row['category_source_id']['category_source'],
                "category_target": row['category_target_id']['category_target'],
                "section_headings": row['section_heading_ids']
            }
    return None
  
@anvil.server.callable
def get_category_descriptions(source_row, target_row):
    # 直接从行对象获取描述信息
    source_description = source_row['category_source'] if source_row else "Source not found"
    target_description = target_row['category_target'] if target_row else "Target not found"
    return source_description, target_description

@anvil.server.callable
def get_lexical_items(section_heading_id):
    rows = app_tables.lexical_items.search(section_heading_id=section_heading_id)
    return [(row['english_headword'], row['metaphorical_word_class']) for row in rows]
  
@anvil.server.callable
def get_section_heading(main_heading_id):
    main_rows = app_tables.main_headings.search(main_heading_id=main_heading_id)
    section_heading_ids = []
    
    for main_row in main_rows:
        section_heading_ids.extend(main_row['section_heading_ids'])
    
    section_heading_rows = list(set(section_heading_ids))
    return [{'section_heading': row['section_heading'], 'section_heading_id': row['section_heading_id']} 
            for row in section_heading_rows]

@anvil.server.callable
def update_data_in_database(record_id, new_data):
    record = app_tables.lexical_items.get(lexical_item_id=record_id)
    if record:
        # Update the record with the new data
        record['english_headword'] = new_data['english_headword']
        record['literal_meaning'] = new_data['literal_meaning']
        record["literal_word_class"]= new_data['literal_word_class']
        record["metaphorical_word_class"]= new_data['metaphorical_word_class']
        record['metaphor_meaning'] = new_data['metaphor_meaning']
        record['english_example_sentence'] = new_data['english_example_sentence']
        
        # Optionally return a success message or updated record
        return {"status": "success", "message": "Record updated successfully"}
    else:
        return None


@anvil.server.callable
def get_lexical_items_by_letter(letter):
    items = app_tables.lexical_items.search(english_headword=q.like(letter.lower() + '%'))
    unique_headwords = []
    seen = set()
    for item in items:
        headword = item['english_headword']
        metaphorical_word_class = item['metaphorical_word_class']
        if headword not in seen:
            seen.add((headword,metaphorical_word_class))
    unique_headwords = sorted(seen)
    return unique_headwords

@anvil.server.callable
def search_in_lexical_list(input_list, search_target, lexis):
    results = []
    if lexis:
        for item in input_list:
          if search_target in item[0]:
              results.append(item) 
    else:
        for item in input_list:
          if search_target in item:
              results.append(item) 
    return results if results else None



@anvil.server.callable
def get_matching_headings(source_text, target_text):
    source_row = app_tables.category_sources.get(category_source=source_text)
    target_row = app_tables.category_targets.get(category_target=target_text)

    # if source_row and target_row:
    #     matching_rows = app_tables.main_headings.search(
    #         category_source_id=source_row, category_target_id=target_row
    #     )
    if source_row:
        matching_rows = app_tables.main_headings.search(
            category_source_id=source_row
        )
    elif target_row:
        matching_rows = app_tables.main_headings.search(
            category_target_id=target_row
        )
    else:
        return []
    seen = set()
    result = []
    for row in matching_rows:
        if row['main_heading_id'] not in seen:
            seen.add(row['main_heading_id'])
            result.append({'main_heading_id': row['main_heading_id'], 'main_heading': row['main_heading']})
    return result
 

@anvil.server.callable
def get_relationships_by_main_heading_id(main_heading_id):
    matching_rows = app_tables.relationships.search(main_heading_id=main_heading_id)
    return [{'relationship': row['relationship'], 'related_heading': row['related_heading']} for row in matching_rows]


@anvil.server.callable
def add_new_lexical_item(entry_dict):
    max_id_entry = app_tables.suggestion.search(tables.order_by("id", ascending=False))
    new_id = max_id_entry[0]['id'] + 1 if max_id_entry else 1
    entry_dict['id'] = new_id
    now = datetime.now().replace(microsecond=0)
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    try:
        app_tables.suggestion.add_row(added_time=formatted_time, **entry_dict)
        return {'status': 'success', 'message': 'Item added successfully.'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
      
@anvil.server.callable
def get_suggestion_entries():
    # Get a list of entries from the Data Table, sorted by 'created' column, in descending order
    return app_tables.suggestion.search(
      tables.order_by("added_time", ascending=False)
    )

@anvil.server.callable
def get_lexical_entries(headword):
    # Get a list of entries from the Data Table, sorted by 'created' column, in descending order
    matching_entries = app_tables.lexical_items.search(english_headword=headword)
    return list(matching_entries)
  
@anvil.server.callable
def update_entry(entry, entry_dict):
  existing_entry = app_tables.lexical_items.get(lexical_item_id=entry['lexical_item_id'])
  if existing_entry:
    if not isinstance(entry_dict, dict):
            entry_dict = dict(entry_dict)
    existing_entry.update(**entry_dict)
  else:
      raise Exception("Entry does not exist in either tables")
    
@anvil.server.callable
def delete_entry(entry):
  # check that the entry being deleted exists in the Data Table
  if app_tables.suggestion.has_row(entry):
    entry.delete()
  else:
    raise Exception("Entry does not exist")


@anvil.server.callable
def accept_entry(entry, section_heading_id):
    max_id_entry = app_tables.lexical_items.search(tables.order_by("lexical_item_id", ascending=False))
    new_id = max_id_entry[0]['lexical_item_id'] + 1 if max_id_entry else 1
    try:
        app_tables.lexical_items.add_row(
            lexical_item_id=new_id,
            section_heading_id=section_heading_id,
            **entry
        )
        return {'status': 'success', 'message': 'Item added successfully.'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

@anvil.server.callable
def verify_password(password):
    return password == "adminpass"

@anvil.server.callable
def get_map_data_by_ids(source_id, target_id):  
    row_data = app_tables.map.get(source=str(target_id))
    if row_data:  
        column_name = f'source_{source_id}'
        column_data = row_data[column_name]
        return column_data 
    return None

@anvil.server.callable  
def get_source_id_by_name(source_name):  
    return app_tables.category_sources.get(category_source=source_name)['category_source_id']  

@anvil.server.callable  
def get_target_id_by_name(target_name):  
    return app_tables.category_targets.get(category_target=target_name)['category_target_id']  