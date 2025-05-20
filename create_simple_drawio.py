"""
VSCode互換の単純なdraw.ioファイルを作成するスクリプト

このスクリプトは最もシンプルな形式のdraw.ioファイルを作成し、
VSCodeのDraw.io Integration拡張機能で確実に表示できるようにします。
"""
import os
import sys
import base64
import requests
from io import BytesIO
from PIL import Image

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

def create_simple_drawio():
    """
    VSCode互換の単純なdraw.ioファイルを作成する
    
    Returns:
        str: draw.ioファイルの内容
    """
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
    
    drawio_content = """
<mxfile host="65bd71144e">
    <diagram id="C5RBs43oDa-KdzZeNtuy" name="Page-1">
        <mxGraphModel dx="1223" dy="871" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" math="0" shadow="0">
            <root>
                <mxCell id="WIyWlLk6GJQsqaUBKTNV-0"/>
                <mxCell id="WIyWlLk6GJQsqaUBKTNV-1" parent="WIyWlLk6GJQsqaUBKTNV-0"/>
                
                <!-- タイトル -->
                <mxCell id="title" value="EM_test_project システムアーキテクチャ図" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=20;fontStyle=1" vertex="1" parent="WIyWlLk6GJQsqaUBKTNV-1">
                    <mxGeometry x="160" y="10" width="400" height="30" as="geometry"/>
                </mxCell>
                
                <!-- Windows ホストシステム -->
                <mxCell id="windows_host" value="Windows ホストシステム" style="rounded=1;whiteSpace=wrap;html=1;fontSize=16;fillColor=#dae8fc;strokeColor=#6c8ebf;verticalAlign=top;fontStyle=1" vertex="1" parent="WIyWlLk6GJQsqaUBKTNV-1">
                    <mxGeometry x="40" y="40" width="520" height="400" as="geometry"/>
                </mxCell>
                
                <!-- Windows アイコン -->
                <mxCell id="windows_icon" value="" style="shape=image;verticalLabelPosition=bottom;labelBackgroundColor=default;verticalAlign=top;aspect=fixed;imageAspect=0;image=data:image/png;base64,{windows_icon}" vertex="1" parent="WIyWlLk6GJQsqaUBKTNV-1">
                    <mxGeometry x="50" y="70" width="48" height="48" as="geometry"/>
                </mxCell>
                
                <!-- WSL サブシステム -->
                <mxCell id="wsl_subsystem" value="WSL (Windows Subsystem for Linux)" style="rounded=1;whiteSpace=wrap;html=1;fontSize=14;fillColor=#d5e8d4;strokeColor=#82b366;verticalAlign=top;fontStyle=1" vertex="1" parent="WIyWlLk6GJQsqaUBKTNV-1">
                    <mxGeometry x="80" y="100" width="440" height="300" as="geometry"/>
                </mxCell>
                
                <!-- Linux アイコン -->
                <mxCell id="linux_icon" value="" style="shape=image;verticalLabelPosition=bottom;labelBackgroundColor=default;verticalAlign=top;aspect=fixed;imageAspect=0;image=data:image/png;base64,{linux_icon}" vertex="1" parent="WIyWlLk6GJQsqaUBKTNV-1">
                    <mxGeometry x="90" y="130" width="40" height="40" as="geometry"/>
                </mxCell>
                
                <!-- FastAPI アプリケーション -->
                <mxCell id="fastapi_app" value="FastAPI アプリケーション" style="rounded=1;whiteSpace=wrap;html=1;fontSize=12;fillColor=#fff2cc;strokeColor=#d6b656;verticalAlign=top;fontStyle=1" vertex="1" parent="WIyWlLk6GJQsqaUBKTNV-1">
                    <mxGeometry x="120" y="160" width="200" height="200" as="geometry"/>
                </mxCell>
                
                <!-- FastAPI アイコン -->
                <mxCell id="fastapi_icon" value="" style="shape=image;verticalLabelPosition=bottom;labelBackgroundColor=default;verticalAlign=top;aspect=fixed;imageAspect=0;image=data:image/png;base64,{fastapi_icon}" vertex="1" parent="WIyWlLk6GJQsqaUBKTNV-1">
                    <mxGeometry x="130" y="180" width="40" height="40" as="geometry"/>
                </mxCell>
                
                <!-- FastAPI コンポーネント -->
                <mxCell id="fastapi_core" value="FastAPI コア" style="rounded=1;whiteSpace=wrap;html=1;fontSize=11;fillColor=#ffe6cc;strokeColor=#d79b00;" vertex="1" parent="WIyWlLk6GJQsqaUBKTNV-1">
                    <mxGeometry x="140" y="220" width="160" height="30" as="geometry"/>
                </mxCell>
                
                <mxCell id="auth_module" value="認証モジュール" style="rounded=1;whiteSpace=wrap;html=1;fontSize=11;fillColor=#ffe6cc;strokeColor=#d79b00;" vertex="1" parent="WIyWlLk6GJQsqaUBKTNV-1">
                    <mxGeometry x="140" y="260" width="160" height="30" as="geometry"/>
                </mxCell>
                
                <mxCell id="openai_client" value="OpenAI クライアント" style="rounded=1;whiteSpace=wrap;html=1;fontSize=11;fillColor=#ffe6cc;strokeColor=#d79b00;" vertex="1" parent="WIyWlLk6GJQsqaUBKTNV-1">
                    <mxGeometry x="140" y="300" width="160" height="30" as="geometry"/>
                </mxCell>
                
                <!-- SQLite データベース -->
                <mxCell id="database" value="SQLite データベース" style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fontSize=12;fillColor=#f8cecc;strokeColor=#b85450;" vertex="1" parent="WIyWlLk6GJQsqaUBKTNV-1">
                    <mxGeometry x="380" y="200" width="100" height="120" as="geometry"/>
                </mxCell>
                
                <!-- データベース アイコン -->
                <mxCell id="database_icon" value="" style="shape=image;verticalLabelPosition=bottom;labelBackgroundColor=default;verticalAlign=top;aspect=fixed;imageAspect=0;image=data:image/png;base64,{database_icon}" vertex="1" parent="WIyWlLk6GJQsqaUBKTNV-1">
                    <mxGeometry x="410" y="230" width="40" height="40" as="geometry"/>
                </mxCell>
                
                <!-- Microsoft Azure -->
                <mxCell id="azure_cloud" value="Microsoft Azure" style="ellipse;shape=cloud;whiteSpace=wrap;html=1;fontSize=16;fillColor=#e1d5e7;strokeColor=#9673a6;verticalAlign=top;fontStyle=1" vertex="1" parent="WIyWlLk6GJQsqaUBKTNV-1">
                    <mxGeometry x="600" y="120" width="240" height="200" as="geometry"/>
                </mxCell>
                
                <!-- Azure アイコン -->
                <mxCell id="azure_icon" value="" style="shape=image;verticalLabelPosition=bottom;labelBackgroundColor=default;verticalAlign=top;aspect=fixed;imageAspect=0;image=data:image/png;base64,{azure_icon}" vertex="1" parent="WIyWlLk6GJQsqaUBKTNV-1">
                    <mxGeometry x="620" y="150" width="48" height="48" as="geometry"/>
                </mxCell>
                
                <!-- Azure OpenAI Service -->
                <mxCell id="openai_service" value="Azure OpenAI Service" style="rounded=1;whiteSpace=wrap;html=1;fontSize=12;fillColor=#e1d5e7;strokeColor=#9673a6;" vertex="1" parent="WIyWlLk6GJQsqaUBKTNV-1">
                    <mxGeometry x="650" y="200" width="140" height="60" as="geometry"/>
                </mxCell>
                
                <!-- OpenAI アイコン -->
                <mxCell id="openai_icon" value="" style="shape=image;verticalLabelPosition=bottom;labelBackgroundColor=default;verticalAlign=top;aspect=fixed;imageAspect=0;image=data:image/png;base64,{openai_icon}" vertex="1" parent="WIyWlLk6GJQsqaUBKTNV-1">
                    <mxGeometry x="670" y="210" width="40" height="40" as="geometry"/>
                </mxCell>
                
                <!-- クライアント -->
                <mxCell id="client" value="クライアント" style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;fontSize=12;" vertex="1" parent="WIyWlLk6GJQsqaUBKTNV-1">
                    <mxGeometry x="40" y="500" width="30" height="60" as="geometry"/>
                </mxCell>
                
                <!-- クライアント アイコン -->
                <mxCell id="client_icon" value="" style="shape=image;verticalLabelPosition=bottom;labelBackgroundColor=default;verticalAlign=top;aspect=fixed;imageAspect=0;image=data:image/png;base64,{client_icon}" vertex="1" parent="WIyWlLk6GJQsqaUBKTNV-1">
                    <mxGeometry x="35" y="450" width="40" height="40" as="geometry"/>
                </mxCell>
                
                <!-- 接続 -->
                <mxCell id="db_connection" value="" style="endArrow=classic;startArrow=classic;html=1;rounded=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="WIyWlLk6GJQsqaUBKTNV-1" source="fastapi_app" target="database">
                    <mxGeometry width="50" height="50" relative="1" as="geometry">
                        <mxPoint x="390" y="450" as="sourcePoint"/>
                        <mxPoint x="440" y="400" as="targetPoint"/>
                    </mxGeometry>
                </mxCell>
                
                <mxCell id="db_label" value="SQLAlchemy ORM" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=10;" vertex="1" parent="WIyWlLk6GJQsqaUBKTNV-1">
                    <mxGeometry x="320" y="230" width="60" height="30" as="geometry"/>
                </mxCell>
                
                <mxCell id="azure_connection" value="" style="endArrow=classic;startArrow=classic;html=1;rounded=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="WIyWlLk6GJQsqaUBKTNV-1" source="openai_client" target="openai_service">
                    <mxGeometry width="50" height="50" relative="1" as="geometry">
                        <mxPoint x="390" y="450" as="sourcePoint"/>
                        <mxPoint x="440" y="400" as="targetPoint"/>
                        <Array as="points">
                            <mxPoint x="360" y="315"/>
                            <mxPoint x="360" y="360"/>
                            <mxPoint x="600" y="360"/>
                            <mxPoint x="600" y="230"/>
                        </Array>
                    </mxGeometry>
                </mxCell>
                
                <mxCell id="api_label" value="HTTPS / REST API" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=10;" vertex="1" parent="WIyWlLk6GJQsqaUBKTNV-1">
                    <mxGeometry x="450" y="330" width="100" height="30" as="geometry"/>
                </mxCell>
                
                <mxCell id="client_connection" value="" style="endArrow=classic;startArrow=classic;html=1;rounded=0;exitX=0.5;exitY=0;exitDx=0;exitDy=0;exitPerimeter=0;entryX=0.25;entryY=1;entryDx=0;entryDy=0;" edge="1" parent="WIyWlLk6GJQsqaUBKTNV-1" source="client" target="fastapi_app">
                    <mxGeometry width="50" height="50" relative="1" as="geometry">
                        <mxPoint x="390" y="450" as="sourcePoint"/>
                        <mxPoint x="440" y="400" as="targetPoint"/>
                        <Array as="points">
                            <mxPoint x="170" y="500"/>
                        </Array>
                    </mxGeometry>
                </mxCell>
                
                <mxCell id="client_label" value="HTTP / REST API" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=10;" vertex="1" parent="WIyWlLk6GJQsqaUBKTNV-1">
                    <mxGeometry x="100" y="470" width="100" height="30" as="geometry"/>
                </mxCell>
                
                <!-- 凡例 -->
                <mxCell id="legend" value="凡例" style="swimlane;fontStyle=0;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;fontSize=12;" vertex="1" parent="WIyWlLk6GJQsqaUBKTNV-1">
                    <mxGeometry x="600" y="360" width="240" height="150" as="geometry"/>
                </mxCell>
                
                <mxCell id="legend_1" value="Windows ホストシステム: 物理マシン" style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;fontSize=11;" vertex="1" parent="legend">
                    <mxGeometry y="30" width="240" height="30" as="geometry"/>
                </mxCell>
                
                <mxCell id="legend_2" value="WSL: Linux 仮想環境" style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;fontSize=11;" vertex="1" parent="legend">
                    <mxGeometry y="60" width="240" height="30" as="geometry"/>
                </mxCell>
                
                <mxCell id="legend_3" value="FastAPI: Python Webアプリケーションフレームワーク" style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;fontSize=11;" vertex="1" parent="legend">
                    <mxGeometry y="90" width="240" height="30" as="geometry"/>
                </mxCell>
                
                <mxCell id="legend_4" value="Azure OpenAI: マイクロソフトのAIサービス" style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;fontSize=11;" vertex="1" parent="legend">
                    <mxGeometry y="120" width="240" height="30" as="geometry"/>
                </mxCell>
            </root>
        </mxGraphModel>
    </diagram>
</mxfile>
""".format(
        windows_icon=icon_data["windows"],
        linux_icon=icon_data["linux"],
        fastapi_icon=icon_data["fastapi"],
        database_icon=icon_data["database"],
        azure_icon=icon_data["azure"],
        openai_icon=icon_data["openai"],
        client_icon=icon_data["client"]
    )
    
    return drawio_content

def main():
    """
    メイン関数
    """
    output_file = "DOC/アーキテクチャ/システムアーキテクチャ図_simple.drawio"
    
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    try:
        drawio_content = create_simple_drawio()
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(drawio_content)
            
        print(f"Successfully created simple draw.io file at {output_file}")
        return 0
    except Exception as e:
        print(f"Error creating simple draw.io file: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
