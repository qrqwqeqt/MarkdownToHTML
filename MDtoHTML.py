import sys
import os

def markdown_to_html(markdown):
    html = ''
    in_paragraph = False
    
    for line in markdown.split('\n'):
        if line.strip():
            if line.startswith('#'):
                level = line.count('#')
                tag = f'h{level}'
                html += f'<{tag}>{line[level+1:].strip()}</{tag}>\n'
            elif line.startswith('* '):
                html += f'<li>{line[2:].strip()}</li>\n'
            elif line.startswith('- '):
                html += f'<li>{line[2:].strip()}</li>\n'
            else:
                if not in_paragraph:
                    html += '<p>'
                    in_paragraph = True
                html += f'{line.strip()}<br>'
        else:
            if in_paragraph:
                html += '</p>\n'
                in_paragraph = False
    
    if in_paragraph:
        html += '</p>\n'
    
    return html

def process_markdown_file(input_file_path, output_file_path=None):
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            markdown_text = file.read()
    except FileNotFoundError:
        print("Error: Input file not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    html_output = markdown_to_html(markdown_text)
    
    if output_file_path:
        try:
            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.write(html_output)
            print(f"HTML output written to {output_file_path}")
        except Exception as e:
            print(f"Error writing to output file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(html_output)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python markdown_to_html.py input.md [output.html]", file=sys.stderr)
        sys.exit(1)
    
    input_file_path = sys.argv[1]
    output_file_path = None
    if len(sys.argv) >= 3:
        output_file_path = sys.argv[2]
    
    process_markdown_file(input_file_path, output_file_path)
