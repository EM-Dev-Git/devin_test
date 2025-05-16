"""
アーキテクチャ図のJPEG画像を生成するスクリプト（アイコン付き）

このスクリプトはWebから取得したアイコンを使用して、
視覚的に見やすいアーキテクチャ図のJPEG画像を生成します。
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

def create_enhanced_architecture_diagram(output_file, width=1200, height=800):
    """
    アイコン付きアーキテクチャ図のJPEG画像を生成する
    
    Args:
        output_file: 出力JPEG画像のパス
        width: 画像の幅（ピクセル）
        height: 画像の高さ（ピクセル）
        
    Returns:
        bool: 生成が成功した場合はTrue、それ以外はFalse
    """
    try:
        img = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(img)
        
        try:
            title_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 28)
            header_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 20)
            normal_font = ImageFont.truetype("DejaVuSans.ttf", 16)
            small_font = ImageFont.truetype("DejaVuSans.ttf", 14)
        except IOError:
            title_font = ImageFont.load_default()
            header_font = ImageFont.load_default()
            normal_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
        
        draw.text((width/2, 40), "EM_test_project システムアーキテクチャ図", fill="black", font=title_font, anchor="mt")
        
        try:
            windows_icon = Image.open("icons/windows.png").convert("RGBA")
            linux_icon = Image.open("icons/linux.png").convert("RGBA")
            fastapi_icon = Image.open("icons/fastapi.png").convert("RGBA")
            azure_icon = Image.open("icons/azure.png").convert("RGBA")
            database_icon = Image.open("icons/database.png").convert("RGBA")
            openai_icon = Image.open("icons/openai.png").convert("RGBA")
            client_icon = Image.open("icons/client.png").convert("RGBA")
            
            windows_icon = windows_icon.resize((48, 48))
            linux_icon = linux_icon.resize((40, 40))
            fastapi_icon = fastapi_icon.resize((40, 40))
            azure_icon = azure_icon.resize((48, 48))
            database_icon = database_icon.resize((40, 40))
            openai_icon = openai_icon.resize((40, 40))
            client_icon = client_icon.resize((40, 40))
            
        except Exception as e:
            print(f"Warning: Could not load icons: {str(e)}")
            windows_icon = linux_icon = fastapi_icon = azure_icon = database_icon = openai_icon = client_icon = None
        
        windows_rect = (50, 80, 750, 600)
        draw.rectangle(windows_rect, outline="#0078D7", fill="#E6F2FF", width=2)
        
        if windows_icon:
            icon_pos = (windows_rect[0] + 20, windows_rect[1] + 20)
            img.paste(windows_icon, icon_pos, windows_icon)
            draw.text((icon_pos[0] + 60, icon_pos[1] + 24), "Windows ホストシステム", fill="#0078D7", font=header_font)
        else:
            draw.text((windows_rect[0] + 20, windows_rect[1] + 20), "Windows ホストシステム", fill="#0078D7", font=header_font)
        
        wsl_rect = (100, 130, 700, 550)
        draw.rectangle(wsl_rect, outline="#16C60C", fill="#E6FFE6", width=2)
        
        if linux_icon:
            icon_pos = (wsl_rect[0] + 20, wsl_rect[1] + 20)
            img.paste(linux_icon, icon_pos, linux_icon)
            draw.text((icon_pos[0] + 50, icon_pos[1] + 20), "WSL (Windows Subsystem for Linux)", fill="#16C60C", font=header_font)
        else:
            draw.text((wsl_rect[0] + 20, wsl_rect[1] + 20), "WSL (Windows Subsystem for Linux)", fill="#16C60C", font=header_font)
        
        fastapi_rect = (150, 200, 400, 450)
        draw.rectangle(fastapi_rect, outline="#009688", fill="#E0F2F1", width=2)
        
        if fastapi_icon:
            icon_pos = (fastapi_rect[0] + 20, fastapi_rect[1] + 20)
            img.paste(fastapi_icon, icon_pos, fastapi_icon)
            draw.text((icon_pos[0] + 50, icon_pos[1] + 20), "FastAPI アプリケーション", fill="#009688", font=normal_font)
        else:
            draw.text((fastapi_rect[0] + 20, fastapi_rect[1] + 20), "FastAPI アプリケーション", fill="#009688", font=normal_font)
        
        components = [
            (180, 250, 370, 290, "FastAPI コア"),
            (180, 310, 370, 350, "認証モジュール"),
            (180, 370, 370, 410, "OpenAI クライアント")
        ]
        for x1, y1, x2, y2, text in components:
            draw.rectangle((x1, y1, x2, y2), outline="#009688", fill="#B2DFDB", width=1)
            draw.text((x1 + 15, y1 + 20), text, fill="#00796B", font=small_font, anchor="lm")
        
        db_x, db_y = 550, 250
        
        if database_icon:
            icon_pos = (db_x + 30, db_y + 40)
            img.paste(database_icon, icon_pos, database_icon)
            draw.text((db_x + 50, db_y + 100), "SQLite\nデータベース", fill="#D32F2F", font=small_font, anchor="mm")
        else:
            draw.ellipse((db_x, db_y, db_x + 100, db_y + 30), outline="#D32F2F", fill="#FFEBEE", width=1)
            draw.rectangle((db_x, db_y + 15, db_x + 100, db_y + 120), outline="#D32F2F", fill="#FFEBEE", width=1)
            draw.ellipse((db_x, db_y + 105, db_x + 100, db_y + 135), outline="#D32F2F", fill="#FFEBEE", width=1)
            draw.text((db_x + 50, db_y + 60), "SQLite\nデータベース", fill="#D32F2F", font=small_font, anchor="mm")
        
        cloud_x, cloud_y = 850, 200
        
        if azure_icon:
            icon_pos = (cloud_x - 24, cloud_y + 20)
            img.paste(azure_icon, icon_pos, azure_icon)
            draw.text((cloud_x, cloud_y + 80), "Microsoft Azure", fill="#0078D4", font=normal_font, anchor="mm")
        else:
            draw.ellipse((cloud_x - 100, cloud_y, cloud_x + 100, cloud_y + 150), outline="#0078D4", fill="#E8F0FE", width=2)
            draw.text((cloud_x, cloud_y + 40), "Microsoft Azure", fill="#0078D4", font=normal_font, anchor="mm")
        
        openai_rect = (cloud_x - 70, cloud_y + 100, cloud_x + 70, cloud_y + 150)
        draw.rectangle(openai_rect, outline="#0078D4", fill="#E8F0FE", width=1)
        
        if openai_icon:
            icon_pos = (openai_rect[0] + 15, openai_rect[1] + 5)
            img.paste(openai_icon, icon_pos, openai_icon)
            draw.text((openai_rect[0] + 65, openai_rect[1] + 25), "Azure OpenAI Service", fill="#0078D4", font=small_font, anchor="lm")
        else:
            draw.text((cloud_x, openai_rect[1] + 25), "Azure OpenAI Service", fill="#0078D4", font=small_font, anchor="mm")
        
        client_x, client_y = 100, 650
        
        if client_icon:
            icon_pos = (client_x - 20, client_y - 20)
            img.paste(client_icon, icon_pos, client_icon)
            draw.text((client_x, client_y + 40), "クライアント", fill="#5E35B1", font=small_font, anchor="mm")
        else:
            draw.ellipse((client_x - 10, client_y - 30, client_x + 10, client_y - 10), outline="black", width=1)
            draw.line((client_x, client_y - 10, client_x, client_y + 20), fill="black", width=1)
            draw.line((client_x, client_y, client_x - 15, client_y + 15), fill="black", width=1)
            draw.line((client_x, client_y, client_x + 15, client_y + 15), fill="black", width=1)
            draw.line((client_x, client_y + 20, client_x - 10, client_y + 40), fill="black", width=1)
            draw.line((client_x, client_y + 20, client_x + 10, client_y + 40), fill="black", width=1)
            draw.text((client_x, client_y + 60), "クライアント", fill="black", font=small_font, anchor="mm")
        
        draw.line((400, 325, 550, 325), fill="#2196F3", width=2)
        draw.text((475, 305), "SQLAlchemy ORM", fill="#1976D2", font=small_font, anchor="mm")
        
        points = [(370, 390), (450, 390), (450, 500), (800, 500), (800, 300), (850, 300)]
        for i in range(len(points) - 1):
            draw.line((points[i][0], points[i][1], points[i+1][0], points[i+1][1]), fill="#2196F3", width=2)
        draw.text((625, 480), "HTTPS / REST API", fill="#1976D2", font=small_font, anchor="mm")
        
        draw.line((client_x, client_y - 40, 275, 450), fill="#2196F3", width=2)
        draw.text((200, 500), "HTTP / REST API", fill="#1976D2", font=small_font, anchor="mm")
        
        legend_rect = (800, 400, 1100, 600)
        draw.rectangle(legend_rect, outline="#9E9E9E", fill="white", width=1)
        draw.text((legend_rect[0] + 20, legend_rect[1] + 20), "凡例", fill="#212121", font=normal_font)
        
        legend_items = [
            "Windows ホストシステム: 物理マシン",
            "WSL: Linux 仮想環境",
            "FastAPI: Python Webアプリケーションフレームワーク",
            "Azure OpenAI: マイクロソフトのAIサービス"
        ]
        
        for i, item in enumerate(legend_items):
            y_pos = legend_rect[1] + 60 + i * 30
            draw.text((legend_rect[0] + 30, y_pos), item, fill="#424242", font=small_font)
        
        img.save(output_file, "JPEG", quality=95)
        print(f"Successfully created enhanced architecture diagram at {output_file}")
        return True
        
    except Exception as e:
        print(f"Error creating enhanced architecture diagram: {str(e)}")
        return False

def main():
    """
    メイン関数
    """
    output_file = "DOC/アーキテクチャ/システムアーキテクチャ図_enhanced.jpg"
    
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    success = create_enhanced_architecture_diagram(output_file)
    
    if success:
        print(f"Enhanced image generation successful. JPEG image saved to {output_file}")
        return 0
    else:
        print("Enhanced image generation failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
