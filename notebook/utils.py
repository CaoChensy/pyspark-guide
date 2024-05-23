import os
import json
import base64
import argparse

parser = argparse.ArgumentParser(description='IPYNB路径')
parser.add_argument('ipynb', type=str, help='IPYNB路径')
args = parser.parse_args()

def GetIpynbCells(ipynb_path):
    """"""
    with open(ipynb_path, encoding='utf-8') as F:
        data = json.load(F)
    cells = data['cells']
    language = data['metadata']['kernelspec']['language']
    return cells, language

def OutPutImage(bs64, img_path):
    """
    """
    img_data = base64.b64decode(bs64)
    with open(img_path,'wb') as img_f:
        img_f.write(img_data)
        
        
def RenderCells(cells, code='python', ):
    """"""
    text_md = ''
    for cell in cells:
        cell_type = cell.get('cell_type')
        execution_count = cell.get('execution_count')
        metadata = cell.get('metadata')
        outputs = cell.get('outputs')
        source = cell.get('source')
        
        if cell_type == 'code':
            code_text = f'```{code}\n' + ''.join(source) + '\n```\n'
            text_md += code_text
            
        if cell_type == 'markdown':
            text = "\n".join(source)
            text_md += f'\n{text}\n'
            
        if outputs:
            for i, output in enumerate(outputs):
                out_data = output.get('data')
                if out_data and code == 'python':
                    if out_data.get('image/png'):
                        img_file_path = os.path.join(img_path, f'{project_name}_img_{execution_count}_{i}.png')
                        OutPutImage(out_data.get('image/png'), img_file_path)
                        text_md += f"![img]({img_file_path})\n"

                    if out_data.get('text/plain'):
                        output_text = '>>> '.join(out_data.get('text/plain'))
                        if 'Figure size' not in output_text and 'matplotlib.lines' not in output_text:
                            text_md += f'```bash\n>>> output Data:\n>>> ' + output_text + '\n```\n'
                        else:
                            continue
                if output.get('text'):
                    output_text = ''.join(output.get('text'))
                    text_md += f'```bash\n>>> output Data:\n>>>\n' + output_text + '```\n'
                    
    return text_md


ipynb_path = args.ipynb
path, file_name = os.path.split(ipynb_path)
project_name, ext = os.path.splitext(file_name)
img_path = './img'

if not os.path.exists(img_path):
    os.mkdir(img_path)

cells, language = GetIpynbCells(ipynb_path)
text_md = RenderCells(cells, language)
with open(f'{project_name}.md','w', encoding='utf-8') as md_f:
    md_f.write(text_md)
    
    
    