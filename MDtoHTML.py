import re
import sys

def parse_markdown_to_html(text):
    # Находим блоки кода и сохраняем их содержимое
    code_blocks = []
    def replace_code_blocks(match):
        code_blocks.append(match.group(1))
        return f"@@@{len(code_blocks) - 1}@@@"
    text = re.sub(r'```(.*?)```', replace_code_blocks, text, flags=re.DOTALL)

    # Обработка заголовков
    text = re.sub(r'^(#{1,6})\s(.*?)\n', lambda match: f'<h{len(match.group(1))}>{match.group(2)}</h{len(match.group(1))}>\n', text, flags=re.MULTILINE)
    
    # Обработка параграфов
    text = re.sub(r'(^|\n)(?!<h|<\/p>|<\/pre>|<\/ul>|<\/ol>|<\/blockquote>|<\/pre>|<li>|<\/li>|<\/code>)((?!<p>).+?)(?=\n\n|\n*$)', r'\1<p>\2</p>\n', text, flags=re.DOTALL)
    
    # Обработка списков
    text = re.sub(r'^(\s*)[*+-]\s(.*?)(\n|$)', lambda match: f'{match.group(1)}<li>{match.group(2)}</li>\n', text, flags=re.MULTILINE)
    text = re.sub(r'(<li>.*?<\/li>)', r'<ul>\g<1></ul>', text, flags=re.DOTALL)
    text = re.sub(r'(^|\n)\d+\.\s(.*?)(\n|$)', r'\1<li>\2</li>\n', text, flags=re.MULTILINE)
    text = re.sub(r'(<li>.*?<\/li>)', r'<ol>\g<1></ol>', text, flags=re.DOTALL)
    
    # Заменяем звездочки на теги <strong>, учитывая обратные слеши
    text = re.sub(r'(?<!\\)\*\*(.*?)(?<!\\)\*\*', r'<strong>\1</strong>', text)
    # Заменяем нижние подчеркивания на теги <em>, учитывая обратные слеши
    text = re.sub(r'(?<!\\)_(.*?)(?<!\\)_', r'<em>\1</em>', text)
    # Заменяем backticks на теги <code>, учитывая обратные слеши
    text = re.sub(r'(?<!\\)`(.*?)(?<!\\)`', r'<code>\1</code>', text)
    
    # Восстанавливаем блоки кода обратно, удаляя теги ```
    for i, code_block in enumerate(code_blocks):
        text = text.replace(f"@@@{i}@@@", f"<pre>{code_block}</pre>")

    return text

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Потрібно вказати ім'я файлу вводу та файлу виводу")
        print("Приклад використання: python markdown_to_html.py вхід.md вивід.html")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            input_text = file.read()
            html_output = parse_markdown_to_html(input_text)
            with open(output_file, 'w', encoding='utf-8') as out_file:
                out_file.write(html_output)
            print("HTML вивід збережено в", output_file)
    except FileNotFoundError:
        print("Помилка: один з файлів не знайдено")
