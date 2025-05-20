"""
VSCode互換のdraw.ioファイルにWebアイコンを追加するスクリプト

このスクリプトはdraw.ioファイルを解析し、
VSCodeでも表示できるようにWebアイコンを追加します。
"""
import os
import sys
import xml.etree.ElementTree as ET
import requests
from io import BytesIO
from PIL import Image
import base64

def download_icon(url, size=(48, 48)):
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

def fix_drawio_with_icons(input_file, output_file):
    """
    draw.ioファイルにVSCode互換のWebアイコンを追加する
    
    Args:
        input_file: 入力draw.ioファイルのパス
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
            icon_data[name] = download_icon(url)
            if icon_data[name]:
                print(f"Successfully downloaded {name} icon")
            else:
                print(f"Failed to download {name} icon")
        
        tree = ET.parse(input_file)
        root = tree.getroot()
        
        diagram = root.find('.//diagram')
        if diagram is None:
            print("Error: No diagram element found in the draw.io file")
            return False
        
        new_root = ET.Element('mxfile')
        new_root.set('host', 'app.diagrams.net')
        new_root.set('modified', '2025-05-16T08:30:00.000Z')
        new_root.set('agent', 'Mozilla/5.0')
        new_root.set('etag', 'abc123')
        new_root.set('version', '21.3.7')
        
        new_diagram = ET.SubElement(new_root, 'diagram')
        new_diagram.set('id', 'C5RBs43oDa-KdzZeNtuy')
        new_diagram.set('name', 'システムアーキテクチャ')
        
        mxgraph_model = ET.SubElement(new_diagram, 'mxGraphModel')
        mxgraph_model.set('dx', '1223')
        mxgraph_model.set('dy', '871')
        mxgraph_model.set('grid', '1')
        mxgraph_model.set('gridSize', '10')
        mxgraph_model.set('guides', '1')
        mxgraph_model.set('tooltips', '1')
        mxgraph_model.set('connect', '1')
        mxgraph_model.set('arrows', '1')
        mxgraph_model.set('fold', '1')
        mxgraph_model.set('page', '1')
        mxgraph_model.set('pageScale', '1')
        mxgraph_model.set('pageWidth', '827')
        mxgraph_model.set('pageHeight', '1169')
        mxgraph_model.set('math', '0')
        mxgraph_model.set('shadow', '0')
        
        root_element = ET.SubElement(mxgraph_model, 'root')
        
        cell0 = ET.SubElement(root_element, 'mxCell')
        cell0.set('id', 'WIyWlLk6GJQsqaUBKTNV-0')
        
        cell1 = ET.SubElement(root_element, 'mxCell')
        cell1.set('id', 'WIyWlLk6GJQsqaUBKTNV-1')
        cell1.set('parent', 'WIyWlLk6GJQsqaUBKTNV-0')
        
        components = [
            {
                "id": "windows_host",
                "value": "Windows ホストシステム",
                "style": "rounded=1;whiteSpace=wrap;html=1;fontSize=16;fillColor=#dae8fc;strokeColor=#6c8ebf;verticalAlign=top;fontStyle=1",
                "geometry": {"x": 40, "y": 40, "width": 520, "height": 400},
                "icon": {
                    "type": "windows",
                    "x": 50, "y": 70, "width": 48, "height": 48
                }
            },
            {
                "id": "wsl_subsystem",
                "value": "WSL (Windows Subsystem for Linux)",
                "style": "rounded=1;whiteSpace=wrap;html=1;fontSize=14;fillColor=#d5e8d4;strokeColor=#82b366;verticalAlign=top;fontStyle=1",
                "geometry": {"x": 80, "y": 100, "width": 440, "height": 300},
                "icon": {
                    "type": "linux",
                    "x": 90, "y": 130, "width": 40, "height": 40
                }
            },
            {
                "id": "fastapi_app",
                "value": "FastAPI アプリケーション",
                "style": "rounded=1;whiteSpace=wrap;html=1;fontSize=12;fillColor=#fff2cc;strokeColor=#d6b656;verticalAlign=top;fontStyle=1",
                "geometry": {"x": 120, "y": 160, "width": 200, "height": 200},
                "icon": {
                    "type": "fastapi",
                    "x": 130, "y": 180, "width": 40, "height": 40
                }
            },
            {
                "id": "fastapi_core",
                "value": "FastAPI コア",
                "style": "rounded=1;whiteSpace=wrap;html=1;fontSize=11;fillColor=#ffe6cc;strokeColor=#d79b00;",
                "geometry": {"x": 140, "y": 200, "width": 160, "height": 40}
            },
            {
                "id": "auth_module",
                "value": "認証モジュール",
                "style": "rounded=1;whiteSpace=wrap;html=1;fontSize=11;fillColor=#ffe6cc;strokeColor=#d79b00;",
                "geometry": {"x": 140, "y": 250, "width": 160, "height": 30}
            },
            {
                "id": "openai_client",
                "value": "OpenAI クライアント",
                "style": "rounded=1;whiteSpace=wrap;html=1;fontSize=11;fillColor=#ffe6cc;strokeColor=#d79b00;",
                "geometry": {"x": 140, "y": 290, "width": 160, "height": 30}
            },
            {
                "id": "database",
                "value": "SQLite データベース",
                "style": "shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fontSize=12;fillColor=#f8cecc;strokeColor=#b85450;",
                "geometry": {"x": 380, "y": 200, "width": 100, "height": 120},
                "icon": {
                    "type": "database",
                    "x": 410, "y": 230, "width": 40, "height": 40
                }
            },
            {
                "id": "azure_cloud",
                "value": "Microsoft Azure",
                "style": "ellipse;shape=cloud;whiteSpace=wrap;html=1;fontSize=16;fillColor=#e1d5e7;strokeColor=#9673a6;verticalAlign=top;fontStyle=1",
                "geometry": {"x": 600, "y": 120, "width": 240, "height": 200},
                "icon": {
                    "type": "azure",
                    "x": 620, "y": 150, "width": 48, "height": 48
                }
            },
            {
                "id": "openai_service",
                "value": "Azure OpenAI Service",
                "style": "rounded=1;whiteSpace=wrap;html=1;fontSize=12;fillColor=#e1d5e7;strokeColor=#9673a6;",
                "geometry": {"x": 650, "y": 200, "width": 140, "height": 60},
                "icon": {
                    "type": "openai",
                    "x": 670, "y": 210, "width": 40, "height": 40
                }
            },
            {
                "id": "client",
                "value": "クライアント",
                "style": "shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;fontSize=12;",
                "geometry": {"x": 40, "y": 500, "width": 30, "height": 60},
                "icon": {
                    "type": "client",
                    "x": 35, "y": 450, "width": 40, "height": 40
                }
            }
        ]
        
        connections = [
            {
                "id": "db_connection",
                "source": "fastapi_app",
                "target": "database",
                "style": "endArrow=classic;startArrow=classic;html=1;rounded=0;",
                "source_point": {"x": 390, "y": 450},
                "target_point": {"x": 440, "y": 400}
            },
            {
                "id": "azure_connection",
                "source": "openai_client",
                "target": "openai_service",
                "style": "endArrow=classic;startArrow=classic;html=1;rounded=0;",
                "source_point": {"x": 390, "y": 450},
                "target_point": {"x": 440, "y": 400},
                "points": [
                    {"x": 360, "y": 305},
                    {"x": 360, "y": 360},
                    {"x": 600, "y": 360},
                    {"x": 600, "y": 230}
                ]
            },
            {
                "id": "client_connection",
                "source": "client",
                "target": "fastapi_app",
                "style": "endArrow=classic;startArrow=classic;html=1;rounded=0;",
                "source_point": {"x": 390, "y": 450},
                "target_point": {"x": 440, "y": 400},
                "points": [
                    {"x": 170, "y": 530}
                ]
            }
        ]
        
        labels = [
            {
                "id": "db_label",
                "value": "SQLAlchemy ORM",
                "style": "text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=10;",
                "geometry": {"x": 320, "y": 230, "width": 60, "height": 30}
            },
            {
                "id": "api_label",
                "value": "HTTPS / REST API",
                "style": "text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=10;",
                "geometry": {"x": 450, "y": 330, "width": 100, "height": 30}
            },
            {
                "id": "client_label",
                "value": "HTTP / REST API",
                "style": "text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=10;",
                "geometry": {"x": 100, "y": 500, "width": 100, "height": 30}
            }
        ]
        
        legend = {
            "id": "legend",
            "value": "凡例",
            "style": "swimlane;fontStyle=0;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;fontSize=12;",
            "geometry": {"x": 600, "y": 360, "width": 240, "height": 150},
            "items": [
                {
                    "id": "legend_1",
                    "value": "Windows ホストシステム: 物理マシン",
                    "style": "text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;fontSize=11;"
                },
                {
                    "id": "legend_2",
                    "value": "WSL: Linux 仮想環境",
                    "style": "text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;fontSize=11;"
                },
                {
                    "id": "legend_3",
                    "value": "FastAPI: Python Webアプリケーションフレームワーク",
                    "style": "text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;fontSize=11;"
                },
                {
                    "id": "legend_4",
                    "value": "Azure OpenAI: マイクロソフトのAIサービス",
                    "style": "text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;fontSize=11;"
                }
            ]
        }
        
        title = {
            "id": "title",
            "value": "EM_test_project システムアーキテクチャ図",
            "style": "text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=20;fontStyle=1",
            "geometry": {"x": 160, "y": 10, "width": 400, "height": 30}
        }
        
        for component in components:
            cell = ET.SubElement(root_element, 'mxCell')
            cell.set('id', component["id"])
            cell.set('value', component["value"])
            cell.set('style', component["style"])
            cell.set('vertex', "1")
            cell.set('parent', "WIyWlLk6GJQsqaUBKTNV-1")
            
            geometry = ET.SubElement(cell, 'mxGeometry')
            geometry.set('x', str(component["geometry"]["x"]))
            geometry.set('y', str(component["geometry"]["y"]))
            geometry.set('width', str(component["geometry"]["width"]))
            geometry.set('height', str(component["geometry"]["height"]))
            geometry.set('as', "geometry")
            
            if "icon" in component:
                icon_type = component["icon"]["type"]
                if icon_data[icon_type]:
                    icon_cell = ET.SubElement(root_element, 'mxCell')
                    icon_cell.set('id', f"{component['id']}_icon")
                    icon_cell.set('value', "")
                    icon_cell.set('style', f"shape=image;imageAspect=0;aspect=fixed;verticalLabelPosition=bottom;verticalAlign=top;image=data:image/png;base64,{icon_data[icon_type]}")
                    icon_cell.set('vertex', "1")
                    icon_cell.set('parent', "WIyWlLk6GJQsqaUBKTNV-1")
                    
                    icon_geometry = ET.SubElement(icon_cell, 'mxGeometry')
                    icon_geometry.set('x', str(component["icon"]["x"]))
                    icon_geometry.set('y', str(component["icon"]["y"]))
                    icon_geometry.set('width', str(component["icon"]["width"]))
                    icon_geometry.set('height', str(component["icon"]["height"]))
                    icon_geometry.set('as', "geometry")
        
        for connection in connections:
            conn = ET.SubElement(root_element, 'mxCell')
            conn.set('id', connection["id"])
            conn.set('value', "")
            conn.set('style', connection["style"])
            conn.set('edge', "1")
            conn.set('parent', "WIyWlLk6GJQsqaUBKTNV-1")
            conn.set('source', connection["source"])
            conn.set('target', connection["target"])
            
            geometry = ET.SubElement(conn, 'mxGeometry')
            geometry.set('relative', "1")
            geometry.set('as', "geometry")
            
            source_point = ET.SubElement(geometry, 'mxPoint')
            source_point.set('x', str(connection["source_point"]["x"]))
            source_point.set('y', str(connection["source_point"]["y"]))
            source_point.set('as', "sourcePoint")
            
            target_point = ET.SubElement(geometry, 'mxPoint')
            target_point.set('x', str(connection["target_point"]["x"]))
            target_point.set('y', str(connection["target_point"]["y"]))
            target_point.set('as', "targetPoint")
            
            if "points" in connection:
                array = ET.SubElement(geometry, 'Array')
                array.set('as', "points")
                
                for point in connection["points"]:
                    point_elem = ET.SubElement(array, 'mxPoint')
                    point_elem.set('x', str(point["x"]))
                    point_elem.set('y', str(point["y"]))
        
        for label in labels:
            label_cell = ET.SubElement(root_element, 'mxCell')
            label_cell.set('id', label["id"])
            label_cell.set('value', label["value"])
            label_cell.set('style', label["style"])
            label_cell.set('vertex', "1")
            label_cell.set('parent', "WIyWlLk6GJQsqaUBKTNV-1")
            
            geometry = ET.SubElement(label_cell, 'mxGeometry')
            geometry.set('x', str(label["geometry"]["x"]))
            geometry.set('y', str(label["geometry"]["y"]))
            geometry.set('width', str(label["geometry"]["width"]))
            geometry.set('height', str(label["geometry"]["height"]))
            geometry.set('as', "geometry")
        
        legend_cell = ET.SubElement(root_element, 'mxCell')
        legend_cell.set('id', legend["id"])
        legend_cell.set('value', legend["value"])
        legend_cell.set('style', legend["style"])
        legend_cell.set('vertex', "1")
        legend_cell.set('parent', "WIyWlLk6GJQsqaUBKTNV-1")
        
        legend_geometry = ET.SubElement(legend_cell, 'mxGeometry')
        legend_geometry.set('x', str(legend["geometry"]["x"]))
        legend_geometry.set('y', str(legend["geometry"]["y"]))
        legend_geometry.set('width', str(legend["geometry"]["width"]))
        legend_geometry.set('height', str(legend["geometry"]["height"]))
        legend_geometry.set('as', "geometry")
        
        for i, item in enumerate(legend["items"]):
            item_cell = ET.SubElement(root_element, 'mxCell')
            item_cell.set('id', item["id"])
            item_cell.set('value', item["value"])
            item_cell.set('style', item["style"])
            item_cell.set('vertex', "1")
            item_cell.set('parent', legend["id"])
            
            item_geometry = ET.SubElement(item_cell, 'mxGeometry')
            item_geometry.set('y', str(i * 30))
            item_geometry.set('width', str(legend["geometry"]["width"]))
            item_geometry.set('height', "30")
            item_geometry.set('as', "geometry")
        
        title_cell = ET.SubElement(root_element, 'mxCell')
        title_cell.set('id', title["id"])
        title_cell.set('value', title["value"])
        title_cell.set('style', title["style"])
        title_cell.set('vertex', "1")
        title_cell.set('parent', "WIyWlLk6GJQsqaUBKTNV-1")
        
        title_geometry = ET.SubElement(title_cell, 'mxGeometry')
        title_geometry.set('x', str(title["geometry"]["x"]))
        title_geometry.set('y', str(title["geometry"]["y"]))
        title_geometry.set('width', str(title["geometry"]["width"]))
        title_geometry.set('height', str(title["geometry"]["height"]))
        title_geometry.set('as', "geometry")
        
        tree = ET.ElementTree(new_root)
        tree.write(output_file, encoding='utf-8', xml_declaration=True)
        
        print(f"Successfully created VSCode-compatible draw.io file with icons at {output_file}")
        return True
        
    except Exception as e:
        print(f"Error creating VSCode-compatible draw.io file with icons: {str(e)}")
        return False

def main():
    """
    メイン関数
    """
    input_file = "DOC/アーキテクチャ/システムアーキテクチャ図.drawio"
    output_file = "DOC/アーキテクチャ/システムアーキテクチャ図_vscode.drawio"
    
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} does not exist")
        return 1
        
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    success = fix_drawio_with_icons(input_file, output_file)
    
    if success:
        print(f"Successfully created VSCode-compatible draw.io file with icons at {output_file}")
        return 0
    else:
        print("Failed to create VSCode-compatible draw.io file with icons")
        return 1

if __name__ == "__main__":
    sys.exit(main())
