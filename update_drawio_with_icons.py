"""
draw.ioファイルにWebアイコンを追加するスクリプト

このスクリプトはdraw.ioファイルを解析し、
各コンポーネントにWebアイコンを追加します。
"""
import os
import sys
import base64
import xml.etree.ElementTree as ET
import requests
from io import BytesIO
from PIL import Image

def download_image(url, size=(48, 48)):
    """
    URLから画像をダウンロードし、指定されたサイズにリサイズしてBase64エンコードする
    
    Args:
        url: 画像のURL
        size: リサイズするサイズ（幅, 高さ）
        
    Returns:
        str: Base64エンコードされた画像データ
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        img = Image.open(BytesIO(response.content))
        img = img.convert("RGBA")
        img = img.resize(size)
        
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return img_str
    except Exception as e:
        print(f"Error downloading image from {url}: {str(e)}")
        return None

def update_drawio_with_icons(drawio_file, output_file):
    """
    draw.ioファイルにWebアイコンを追加する
    
    Args:
        drawio_file: 入力draw.ioファイルのパス
        output_file: 出力draw.ioファイルのパス
        
    Returns:
        bool: 更新が成功した場合はTrue、それ以外はFalse
    """
    try:
        icon_urls = {
            "windows": "https://cdn-icons-png.flaticon.com/512/888/888882.png",
            "linux": "https://cdn-icons-png.flaticon.com/512/6124/6124995.png",
            "fastapi": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png",
            "database": "https://cdn-icons-png.flaticon.com/512/148/148825.png",
            "azure": "https://cdn-icons-png.flaticon.com/512/873/873107.png",
            "openai": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/ChatGPT_logo.svg/512px-ChatGPT_logo.svg.png",
            "client": "https://cdn-icons-png.flaticon.com/512/2521/2521826.png"
        }
        
        icon_data = {}
        for name, url in icon_urls.items():
            print(f"Downloading {name} icon from {url}")
            icon_data[name] = download_image(url)
            if icon_data[name]:
                print(f"Successfully downloaded {name} icon")
            else:
                print(f"Failed to download {name} icon")
        
        tree = ET.parse(drawio_file)
        root = tree.getroot()
        
        diagram = root.find('.//diagram')
        if diagram is None:
            print("Error: No diagram element found in the draw.io file")
            return False
            
        mxgraph_model = diagram.find('.//mxGraphModel')
        if mxgraph_model is None:
            diagram_text = diagram.text
            if diagram_text:
                if diagram_text.startswith('7Z'):
                    import zlib
                    diagram_text = zlib.decompress(base64.b64decode(diagram_text), -15).decode('utf-8')
                elif diagram_text.startswith('U'):
                    diagram_text = base64.b64decode(diagram_text).decode('utf-8')
                
                diagram_root = ET.fromstring(diagram_text)
                mxgraph_model = diagram_root
            else:
                print("Error: Could not find mxGraphModel in the draw.io file")
                return False
        
        root_element = mxgraph_model.find('.//root')
        if root_element is None:
            print("Error: Could not find root element in the mxGraphModel")
            return False
        
        components = {
            "windows_host": {"icon": "windows", "x": 40, "y": 40, "width": 48, "height": 48},
            "wsl_subsystem": {"icon": "linux", "x": 80, "y": 100, "width": 40, "height": 40},
            "fastapi_app": {"icon": "fastapi", "x": 120, "y": 160, "width": 40, "height": 40},
            "database": {"icon": "database", "x": 380, "y": 200, "width": 40, "height": 40},
            "azure_cloud": {"icon": "azure", "x": 600, "y": 120, "width": 48, "height": 48},
            "openai_service": {"icon": "openai", "x": 650, "y": 200, "width": 40, "height": 40},
            "client": {"icon": "client", "x": 40, "y": 500, "width": 40, "height": 40}
        }
        
        max_id = 0
        for cell in root_element.findall('.//mxCell'):
            cell_id = cell.get('id')
            if cell_id and cell_id.isdigit():
                max_id = max(max_id, int(cell_id))
        
        for component_id, config in components.items():
            icon_name = config["icon"]
            if icon_data[icon_name]:
                component = None
                for cell in root_element.findall('.//mxCell'):
                    if cell.get('id') == component_id:
                        component = cell
                        break
                
                if component is not None:
                    x = config["x"]
                    y = config["y"]
                    width = config["width"]
                    height = config["height"]
                    
                    new_id = str(max_id + 1)
                    max_id += 1
                    
                    icon_element = ET.SubElement(root_element, 'mxCell')
                    icon_element.set('id', f"{component_id}_icon")
                    icon_element.set('value', "")
                    icon_element.set('style', f"shape=image;html=1;verticalAlign=top;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;imageAspect=0;aspect=fixed;image=data:image/png;base64,{icon_data[icon_name]}")
                    icon_element.set('vertex', "1")
                    icon_element.set('parent', "WIyWlLk6GJQsqaUBKTNV-1")
                    
                    geometry = ET.SubElement(icon_element, 'mxGeometry')
                    geometry.set('x', str(x))
                    geometry.set('y', str(y))
                    geometry.set('width', str(width))
                    geometry.set('height', str(height))
                    geometry.set('as', "geometry")
                    
                    print(f"Added {icon_name} icon to {component_id}")
        
        tree.write(output_file, encoding='utf-8', xml_declaration=True)
        print(f"Successfully updated draw.io file with icons at {output_file}")
        return True
        
    except Exception as e:
        print(f"Error updating draw.io file with icons: {str(e)}")
        return False

def main():
    """
    メイン関数
    """
    input_file = "DOC/アーキテクチャ/システムアーキテクチャ図.drawio"
    output_file = "DOC/アーキテクチャ/システムアーキテクチャ図_enhanced.drawio"
    
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} does not exist")
        return 1
        
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    success = update_drawio_with_icons(input_file, output_file)
    
    if success:
        print(f"Successfully updated draw.io file with icons at {output_file}")
        return 0
    else:
        print("Failed to update draw.io file with icons")
        return 1

if __name__ == "__main__":
    sys.exit(main())
