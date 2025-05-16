"""
システムアーキテクチャ図_simple.drawioをJPEG形式にエクスポートするスクリプト

このスクリプトはdraw.ioファイルの内容を解析し、
Pillowライブラリを使用してJPEG画像を生成します。
"""
import os
import sys
import base64
import xml.etree.ElementTree as ET
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

def extract_icons_from_drawio(drawio_file):
    """
    draw.ioファイルからアイコンとその位置情報を抽出する
    
    Args:
        drawio_file: draw.ioファイルのパス
        
    Returns:
        dict: アイコンIDとその情報（画像データ、位置、サイズ）の辞書
    """
    try:
        tree = ET.parse(drawio_file)
        root = tree.getroot()
        
        icons = {}
        
        diagram = root.find('.//diagram')
        if diagram is None:
            print("Error: No diagram element found in the draw.io file")
            return {}
            
        mxgraph_model = None
        for element in diagram:
            if element.tag == 'mxGraphModel':
                mxgraph_model = element
                break
                
        if mxgraph_model is None:
            diagram_text = diagram.text
            if diagram_text:
                if diagram_text.startswith('7Z'):
                    import zlib
                    try:
                        diagram_text = zlib.decompress(base64.b64decode(diagram_text), -15).decode('utf-8')
                        mxgraph_model = ET.fromstring(diagram_text)
                    except Exception as e:
                        print(f"Error decompressing diagram content: {str(e)}")
                        return {}
                elif diagram_text.startswith('U'):
                    try:
                        diagram_text = base64.b64decode(diagram_text).decode('utf-8')
                        mxgraph_model = ET.fromstring(diagram_text)
                    except Exception as e:
                        print(f"Error decoding diagram content: {str(e)}")
                        return {}
            
        if mxgraph_model is None:
            print("Error: Could not find mxGraphModel in the draw.io file")
            return {}
        
        root_element = mxgraph_model.find('.//root')
        if root_element is None:
            print("Error: Could not find root element in the mxGraphModel")
            return {}
        
        for cell in root_element.findall('.//mxCell'):
            style = cell.get('style', '')
            if 'image=' in style and 'data:image/png;base64,' in style:
                cell_id = cell.get('id', '')
                
                image_data_start = style.find('data:image/png;base64,') + len('data:image/png;base64,')
                image_data_end = style.find('"', image_data_start) if '"' in style[image_data_start:] else len(style)
                image_data = style[image_data_start:image_data_end]
                
                geometry = cell.find('.//mxGeometry')
                if geometry is not None:
                    x = float(geometry.get('x', '0'))
                    y = float(geometry.get('y', '0'))
                    width = float(geometry.get('width', '48'))
                    height = float(geometry.get('height', '48'))
                    
                    icons[cell_id] = {
                        'image_data': image_data,
                        'x': x,
                        'y': y,
                        'width': width,
                        'height': height
                    }
        
        return icons
        
    except Exception as e:
        print(f"Error extracting icons from draw.io file: {str(e)}")
        return {}

def extract_shapes_from_drawio(drawio_file):
    """
    draw.ioファイルから図形とその位置情報を抽出する
    
    Args:
        drawio_file: draw.ioファイルのパス
        
    Returns:
        list: 図形情報（タイプ、位置、サイズ、テキスト、スタイル）のリスト
    """
    try:
        tree = ET.parse(drawio_file)
        root = tree.getroot()
        
        shapes = []
        
        diagram = root.find('.//diagram')
        if diagram is None:
            print("Error: No diagram element found in the draw.io file")
            return []
            
        mxgraph_model = None
        for element in diagram:
            if element.tag == 'mxGraphModel':
                mxgraph_model = element
                break
                
        if mxgraph_model is None:
            diagram_text = diagram.text
            if diagram_text:
                if diagram_text.startswith('7Z'):
                    import zlib
                    try:
                        diagram_text = zlib.decompress(base64.b64decode(diagram_text), -15).decode('utf-8')
                        mxgraph_model = ET.fromstring(diagram_text)
                    except Exception as e:
                        print(f"Error decompressing diagram content: {str(e)}")
                        return []
                elif diagram_text.startswith('U'):
                    try:
                        diagram_text = base64.b64decode(diagram_text).decode('utf-8')
                        mxgraph_model = ET.fromstring(diagram_text)
                    except Exception as e:
                        print(f"Error decoding diagram content: {str(e)}")
                        return []
            
        if mxgraph_model is None:
            print("Error: Could not find mxGraphModel in the draw.io file")
            return []
        
        root_element = mxgraph_model.find('.//root')
        if root_element is None:
            print("Error: Could not find root element in the mxGraphModel")
            return []
        
        for cell in root_element.findall('.//mxCell'):
            cell_id = cell.get('id', '')
            if cell_id in ['0', '1']:  # ルートセルはスキップ
                continue
                
            style = cell.get('style', '')
            if 'image=' in style:  # アイコンはスキップ
                continue
                
            value = cell.get('value', '')
            
            geometry = cell.find('.//mxGeometry')
            if geometry is not None:
                x = float(geometry.get('x', '0'))
                y = float(geometry.get('y', '0'))
                width = float(geometry.get('width', '0'))
                height = float(geometry.get('height', '0'))
                
                shape_type = 'rectangle'
                if 'ellipse' in style:
                    shape_type = 'ellipse'
                elif 'cloud' in style:
                    shape_type = 'cloud'
                elif 'cylinder' in style:
                    shape_type = 'cylinder'
                elif 'umlActor' in style:
                    shape_type = 'actor'
                elif 'swimlane' in style:
                    shape_type = 'swimlane'
                elif 'endArrow' in style:
                    shape_type = 'arrow'
                    
                fill_color = None
                if 'fillColor=' in style:
                    fill_color_start = style.find('fillColor=') + len('fillColor=')
                    fill_color_end = style.find(';', fill_color_start) if ';' in style[fill_color_start:] else len(style)
                    fill_color = style[fill_color_start:fill_color_end]
                    
                stroke_color = None
                if 'strokeColor=' in style:
                    stroke_color_start = style.find('strokeColor=') + len('strokeColor=')
                    stroke_color_end = style.find(';', stroke_color_start) if ';' in style[stroke_color_start:] else len(style)
                    stroke_color = style[stroke_color_start:stroke_color_end]
                
                shapes.append({
                    'id': cell_id,
                    'type': shape_type,
                    'x': x,
                    'y': y,
                    'width': width,
                    'height': height,
                    'text': value,
                    'fill_color': fill_color,
                    'stroke_color': stroke_color,
                    'style': style
                })
        
        return shapes
        
    except Exception as e:
        print(f"Error extracting shapes from draw.io file: {str(e)}")
        return []

def extract_connections_from_drawio(drawio_file):
    """
    draw.ioファイルから接続線とその位置情報を抽出する
    
    Args:
        drawio_file: draw.ioファイルのパス
        
    Returns:
        list: 接続線情報（ソース、ターゲット、ポイント）のリスト
    """
    try:
        tree = ET.parse(drawio_file)
        root = tree.getroot()
        
        connections = []
        
        diagram = root.find('.//diagram')
        if diagram is None:
            print("Error: No diagram element found in the draw.io file")
            return []
            
        mxgraph_model = None
        for element in diagram:
            if element.tag == 'mxGraphModel':
                mxgraph_model = element
                break
                
        if mxgraph_model is None:
            diagram_text = diagram.text
            if diagram_text:
                if diagram_text.startswith('7Z'):
                    import zlib
                    try:
                        diagram_text = zlib.decompress(base64.b64decode(diagram_text), -15).decode('utf-8')
                        mxgraph_model = ET.fromstring(diagram_text)
                    except Exception as e:
                        print(f"Error decompressing diagram content: {str(e)}")
                        return []
                elif diagram_text.startswith('U'):
                    try:
                        diagram_text = base64.b64decode(diagram_text).decode('utf-8')
                        mxgraph_model = ET.fromstring(diagram_text)
                    except Exception as e:
                        print(f"Error decoding diagram content: {str(e)}")
                        return []
            
        if mxgraph_model is None:
            print("Error: Could not find mxGraphModel in the draw.io file")
            return []
        
        root_element = mxgraph_model.find('.//root')
        if root_element is None:
            print("Error: Could not find root element in the mxGraphModel")
            return []
        
        for cell in root_element.findall('.//mxCell'):
            cell_id = cell.get('id', '')
            if cell_id in ['0', '1']:  # ルートセルはスキップ
                continue
                
            source = cell.get('source', '')
            target = cell.get('target', '')
            
            if source and target:  # ソースとターゲットがある場合は接続線
                style = cell.get('style', '')
                value = cell.get('value', '')
                
                geometry = cell.find('.//mxGeometry')
                points = []
                
                if geometry is not None:
                    for point in geometry.findall('.//mxPoint'):
                        x = float(point.get('x', '0'))
                        y = float(point.get('y', '0'))
                        points.append((x, y))
                
                connections.append({
                    'id': cell_id,
                    'source': source,
                    'target': target,
                    'points': points,
                    'text': value,
                    'style': style
                })
        
        return connections
        
    except Exception as e:
        print(f"Error extracting connections from draw.io file: {str(e)}")
        return []

def create_jpeg_from_drawio(drawio_file, output_file, width=1200, height=800):
    """
    draw.ioファイルからJPEG画像を生成する
    
    Args:
        drawio_file: draw.ioファイルのパス
        output_file: 出力JPEG画像のパス
        width: 画像の幅（ピクセル）
        height: 画像の高さ（ピクセル）
        
    Returns:
        bool: 生成が成功した場合はTrue、それ以外はFalse
    """
    try:
        icons = extract_icons_from_drawio(drawio_file)
        shapes = extract_shapes_from_drawio(drawio_file)
        connections = extract_connections_from_drawio(drawio_file)
        
        img = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(img)
        
        try:
            title_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 24)
            header_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 18)
            normal_font = ImageFont.truetype("DejaVuSans.ttf", 14)
            small_font = ImageFont.truetype("DejaVuSans.ttf", 12)
        except IOError:
            title_font = ImageFont.load_default()
            header_font = ImageFont.load_default()
            normal_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
        
        for shape in shapes:
            x, y = shape['x'], shape['y']
            width, height = shape['width'], shape['height']
            shape_type = shape['type']
            text = shape['text']
            
            fill_color = shape['fill_color'] if shape['fill_color'] else '#ffffff'
            stroke_color = shape['stroke_color'] if shape['stroke_color'] else '#000000'
            
            def html_to_rgb(color):
                if color.startswith('#'):
                    color = color[1:]
                    if len(color) == 3:
                        color = ''.join([c*2 for c in color])
                    return tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
                return (255, 255, 255)  # デフォルトは白
                
            fill_rgb = html_to_rgb(fill_color)
            stroke_rgb = html_to_rgb(stroke_color)
            
            if shape_type == 'rectangle':
                draw.rectangle((x, y, x + width, y + height), outline=stroke_rgb, fill=fill_rgb, width=2)
            elif shape_type == 'ellipse':
                draw.ellipse((x, y, x + width, y + height), outline=stroke_rgb, fill=fill_rgb, width=2)
            elif shape_type == 'cylinder':
                draw.ellipse((x, y, x + width, y + height * 0.2), outline=stroke_rgb, fill=fill_rgb, width=1)
                draw.rectangle((x, y + height * 0.1, x + width, y + height * 0.9), outline=stroke_rgb, fill=fill_rgb, width=1)
                draw.ellipse((x, y + height * 0.8, x + width, y + height), outline=stroke_rgb, fill=fill_rgb, width=1)
            elif shape_type == 'cloud':
                draw.ellipse((x, y, x + width, y + height), outline=stroke_rgb, fill=fill_rgb, width=2)
            elif shape_type == 'actor':
                center_x = x + width / 2
                center_y = y + height / 2
                head_radius = min(width, height) * 0.2
                draw.ellipse((center_x - head_radius, y, center_x + head_radius, y + head_radius * 2), outline=stroke_rgb, width=1)
                draw.line((center_x, y + head_radius * 2, center_x, y + height * 0.7), fill=stroke_rgb, width=1)
                draw.line((center_x, y + height * 0.4, center_x - width * 0.3, y + height * 0.5), fill=stroke_rgb, width=1)
                draw.line((center_x, y + height * 0.4, center_x + width * 0.3, y + height * 0.5), fill=stroke_rgb, width=1)
                draw.line((center_x, y + height * 0.7, center_x - width * 0.2, y + height), fill=stroke_rgb, width=1)
                draw.line((center_x, y + height * 0.7, center_x + width * 0.2, y + height), fill=stroke_rgb, width=1)
            elif shape_type == 'swimlane':
                draw.rectangle((x, y, x + width, y + height), outline=stroke_rgb, fill=fill_rgb, width=1)
                draw.line((x, y + 30, x + width, y + 30), fill=stroke_rgb, width=1)
            
            if text:
                text_x = x + width / 2
                text_y = y + height / 2
                
                max_width = width * 0.9
                lines = []
                current_line = ""
                
                for word in text.split():
                    test_line = current_line + " " + word if current_line else word
                    text_width = draw.textlength(test_line, font=normal_font)
                    
                    if text_width <= max_width:
                        current_line = test_line
                    else:
                        lines.append(current_line)
                        current_line = word
                
                if current_line:
                    lines.append(current_line)
                
                line_height = normal_font.size * 1.2
                total_height = line_height * len(lines)
                start_y = text_y - total_height / 2
                
                for i, line in enumerate(lines):
                    line_y = start_y + i * line_height
                    draw.text((text_x, line_y), line, fill=stroke_rgb, font=normal_font, anchor="mm")
        
        for connection in connections:
            source = connection['source']
            target = connection['target']
            points = connection['points']
            text = connection['text']
            
            source_shape = next((s for s in shapes if s['id'] == source), None)
            target_shape = next((s for s in shapes if s['id'] == target), None)
            
            if source_shape and target_shape:
                start_x = source_shape['x'] + source_shape['width'] / 2
                start_y = source_shape['y'] + source_shape['height'] / 2
                end_x = target_shape['x'] + target_shape['width'] / 2
                end_y = target_shape['y'] + target_shape['height'] / 2
                
                if points:
                    all_points = [(start_x, start_y)] + points + [(end_x, end_y)]
                else:
                    all_points = [(start_x, start_y), (end_x, end_y)]
                
                for i in range(len(all_points) - 1):
                    draw.line((all_points[i][0], all_points[i][1], all_points[i+1][0], all_points[i+1][1]), fill=(0, 0, 0), width=1)
                
                if text:
                    if len(all_points) > 2:
                        middle_index = len(all_points) // 2
                        text_x = (all_points[middle_index-1][0] + all_points[middle_index][0]) / 2
                        text_y = (all_points[middle_index-1][1] + all_points[middle_index][1]) / 2
                    else:
                        text_x = (start_x + end_x) / 2
                        text_y = (start_y + end_y) / 2
                    
                    text_width = draw.textlength(text, font=small_font)
                    text_height = small_font.size
                    draw.rectangle((text_x - text_width/2 - 5, text_y - text_height/2 - 5, text_x + text_width/2 + 5, text_y + text_height/2 + 5), fill=(255, 255, 255), outline=None)
                    
                    draw.text((text_x, text_y), text, fill=(0, 0, 0), font=small_font, anchor="mm")
        
        for icon_id, icon_info in icons.items():
            try:
                image_data = base64.b64decode(icon_info['image_data'])
                icon_img = Image.open(BytesIO(image_data))
                
                x, y = icon_info['x'], icon_info['y']
                width, height = icon_info['width'], icon_info['height']
                
                icon_img = icon_img.resize((int(width), int(height)))
                img.paste(icon_img, (int(x), int(y)), icon_img if icon_img.mode == 'RGBA' else None)
                
            except Exception as e:
                print(f"Error drawing icon {icon_id}: {str(e)}")
        
        img.save(output_file, "JPEG", quality=95)
        print(f"Successfully created JPEG image at {output_file}")
        return True
        
    except Exception as e:
        print(f"Error creating JPEG image: {str(e)}")
        return False

def main():
    """
    メイン関数
    """
    drawio_file = "DOC/アーキテクチャ/システムアーキテクチャ図_simple.drawio"
    output_file = "DOC/アーキテクチャ/システムアーキテクチャ図_simple.jpg"
    
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    success = create_jpeg_from_drawio(drawio_file, output_file)
    
    if success:
        print(f"JPEG image generation successful. Image saved to {output_file}")
        return 0
    else:
        print("JPEG image generation failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
