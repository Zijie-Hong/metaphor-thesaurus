import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime
from functools import lru_cache
import itertools

@lru_cache(maxsize=128)
@anvil.server.callable
def search_lexical_items(input):
    query1 = f'% {input} %'  # 单词在中间
    query2 = f'{input} %'    # 单词在开头
    query3 = f'% {input}'    # 单词在结尾
    query4 = f'{input}'      # 精确匹配

    matching_rows = app_tables.lexical_items.search(
    english_headword=q.any_of(
        q.like(query1),
        q.like(query2),
        q.like(query3),
        q.like(query4)
        )
    )
    return list(set((row['english_headword'], row['metaphorical_word_class']) for row in matching_rows)) or None
  

def search_with_connectors(input1: str, input2: str, connectors: list) -> list:
    results = []
    for connector in connectors:
        query = f'%{input1}% {connector} %{input2}%'
        matching_rows = app_tables.main_headings.search(main_heading=q.like(query))
        results.extend([row['main_heading'] for row in matching_rows])
    return results or None

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
    # 查询以指定字母开头的主题，不区分大小写
    results = app_tables.main_headings.search(
        main_heading=q.ilike(letter + '%')
    )
    # 按字母排序并返回结果
    sorted_results = sorted(results, key=lambda x: x['main_heading'])
    return [theme['main_heading'] for theme in sorted_results]

@anvil.server.callable
def explore_source_by_letter(letter):
    # 查询以指定字母开头的主题，不区分大小写
    results = app_tables.sources.search(
        source=q.ilike(letter + '%')
    )
    # 按字母排序并返回结果
    sorted_results = sorted(results, key=lambda x: x['source'])
    return [theme['source'] for theme in sorted_results]

@anvil.server.callable
def find_combinations(source):
    combinations = []

    for item in source:
        source_row = app_tables.sources.get(source=item)
        # 从 sources 表中找到对应的 source id
        matching_rows = app_tables.main_headings.search(source_id=source_row)

        target_ids = set()
        for row in matching_rows:
            target_ids.add(row['target_id']['target'])
        
        for target_id in target_ids:
            combinations.append((item, target_id))
    return combinations
  
@anvil.server.callable
def get_main_heading_data(section_heading_id):
    section_heading_row = app_tables.section_headings.get(section_heading_id=section_heading_id)
    if not section_heading_row:
        return None
    
    main_heading_row = section_heading_row['main_heading_id']
    if not main_heading_row:
        return None
    
    main_heading_data = {
        "main_heading_id": main_heading_row['main_heading_id'],
        "main_heading": main_heading_row['main_heading'],
        "category_source": main_heading_row['category_source_id']['category_source'],
        "category_target": main_heading_row['category_target_id']['category_target']
    }
    
    return main_heading_data, section_heading_row['section_heading']

@anvil.server.callable
def get_main_heading_data_by_heading(main_heading):
    row = next(iter(app_tables.main_headings.search(main_heading=main_heading)), None)
    if row:
        return {
            "main_heading_id": row['main_heading_id'],
            "main_heading": row['main_heading'],
            "category_source": row['category_source_id']['category_source'],
            "category_target": row['category_target_id']['category_target']
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
                "category_target": row['category_target_id']['category_target']
            }
    return None
  
@anvil.server.callable
def get_category_descriptions(source_row, target_row):
    # 直接从行对象获取描述信息
    source_description = source_row['category_source'] if source_row else "Source not found"
    target_description = target_row['category_target'] if target_row else "Target not found"
    return source_description, target_description


@anvil.server.callable
def get_section_heading(main_heading_id):
    section_headings = app_tables.section_headings.search(main_heading_id['main_heading_id']=main_heading_id)
    return [{'section_heading_id': row['section_heading_id'], 'section_heading': row['section_heading']} for row in section_headings]

@anvil.server.callable
def get_lexical_items(section_heading_id):
    rows = app_tables.lexical_items.search(section_heading_id=section_heading_id)
    return [(row['english_headword'], row['metaphorical_word_class']) for row in rows]

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
def search_in_lexical_list(input_list, search_target):
    search_target = search_target.lower()
    results = []
    for item in input_list:
      if search_target in item[0].lower():
          results.append(item) 
    return results if results else None



@anvil.server.callable
def get_matching_headings(source_text, target_text):
    source_row = app_tables.category_sources.get(category_source=source_text)
    target_row = app_tables.category_targets.get(category_target=target_text)

    source_id = source_row['category_source_id'] if source_row else None
    target_id = target_row['category_target_id'] if target_row else None
  
    if source_id and target_id:
        matching_rows = app_tables.main_headings.search(
            category_source_id=source_row, category_target_id=target_row
        )
    elif source_id:
        matching_rows = app_tables.main_headings.search(
            category_source_id=source_row
        )
    elif target_id:
        matching_rows = app_tables.main_headings.search(
            category_target_id=target_row
        )
    else:
        return []
    result = [{'main_heading_id': row['main_heading_id'], 'main_heading': row['main_heading']} for row in matching_rows]
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
    # 假设管理员密码为 "adminpass"，实际使用中应更加复杂并使用哈希存储
    return password == "adminpass"