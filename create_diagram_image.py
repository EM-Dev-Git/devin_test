"""
アーキテクチャ図のJPEG画像を生成するスクリプト

このスクリプトはdraw.ioファイルの内容を解析し、
Pillowライブラリを使用して同等のJPEG画像を生成します。
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

def create_architecture_diagram(output_file, width=1200, height=800):
    """
    アーキテクチャ図のJPEG画像を生成する
    
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
            title_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 24)
            header_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 18)
            normal_font = ImageFont.truetype("DejaVuSans.ttf", 14)
            small_font = ImageFont.truetype("DejaVuSans.ttf", 12)
        except IOError:
            title_font = ImageFont.load_default()
            header_font = ImageFont.load_default()
            normal_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
        
        draw.text((width/2, 30), "EM_test_project システムアーキテクチャ図", fill="black", font=title_font, anchor="mt")
        
        windows_rect = (50, 80, 750, 600)
        draw.rectangle(windows_rect, outline="blue", fill=(220, 230, 242), width=2)
        draw.text((windows_rect[0] + 20, windows_rect[1] + 20), "Windows ホストシステム", fill="black", font=header_font)
        
        wsl_rect = (100, 130, 700, 550)
        draw.rectangle(wsl_rect, outline="green", fill=(220, 242, 220), width=2)
        draw.text((wsl_rect[0] + 20, wsl_rect[1] + 20), "WSL (Windows Subsystem for Linux)", fill="black", font=header_font)
        
        fastapi_rect = (150, 200, 400, 450)
        draw.rectangle(fastapi_rect, outline="orange", fill=(255, 242, 204), width=2)
        draw.text((fastapi_rect[0] + 20, fastapi_rect[1] + 20), "FastAPI アプリケーション", fill="black", font=normal_font)
        
        components = [
            (180, 250, 370, 290, "FastAPI コア"),
            (180, 310, 370, 350, "認証モジュール"),
            (180, 370, 370, 410, "OpenAI クライアント")
        ]
        for x1, y1, x2, y2, text in components:
            draw.rectangle((x1, y1, x2, y2), outline="orange", fill=(255, 230, 204), width=1)
            draw.text((x1 + 10, y1 + 10), text, fill="black", font=small_font)
        
        db_x, db_y = 550, 250
        draw.ellipse((db_x, db_y, db_x + 100, db_y + 30), outline="red", fill=(248, 206, 204), width=1)
        draw.rectangle((db_x, db_y + 15, db_x + 100, db_y + 120), outline="red", fill=(248, 206, 204), width=1)
        draw.ellipse((db_x, db_y + 105, db_x + 100, db_y + 135), outline="red", fill=(248, 206, 204), width=1)
        draw.text((db_x + 50, db_y + 60), "SQLite\nデータベース", fill="black", font=small_font, anchor="mm")
        
        cloud_x, cloud_y = 850, 200
        draw.ellipse((cloud_x - 100, cloud_y, cloud_x + 100, cloud_y + 150), outline="purple", fill=(225, 213, 231), width=2)
        draw.text((cloud_x, cloud_y + 40), "Microsoft Azure", fill="black", font=normal_font, anchor="mm")
        
        openai_rect = (cloud_x - 70, cloud_y + 70, cloud_x + 70, cloud_y + 120)
        draw.rectangle(openai_rect, outline="purple", fill=(225, 213, 231), width=1)
        draw.text((cloud_x, cloud_y + 95), "Azure OpenAI Service", fill="black", font=small_font, anchor="mm")
        
        client_x, client_y = 100, 650
        draw.ellipse((client_x - 10, client_y - 30, client_x + 10, client_y - 10), outline="black", width=1)
        draw.line((client_x, client_y - 10, client_x, client_y + 20), fill="black", width=1)
        draw.line((client_x, client_y, client_x - 15, client_y + 15), fill="black", width=1)
        draw.line((client_x, client_y, client_x + 15, client_y + 15), fill="black", width=1)
        draw.line((client_x, client_y + 20, client_x - 10, client_y + 40), fill="black", width=1)
        draw.line((client_x, client_y + 20, client_x + 10, client_y + 40), fill="black", width=1)
        draw.text((client_x, client_y + 60), "クライアント", fill="black", font=small_font, anchor="mm")
        
        draw.line((400, 325, 550, 325), fill="black", width=1)
        draw.text((475, 305), "SQLAlchemy ORM", fill="black", font=small_font, anchor="mm")
        
        points = [(370, 390), (450, 390), (450, 500), (800, 500), (800, 300), (850, 300)]
        for i in range(len(points) - 1):
            draw.line((points[i][0], points[i][1], points[i+1][0], points[i+1][1]), fill="black", width=1)
        draw.text((625, 480), "HTTPS / REST API", fill="black", font=small_font, anchor="mm")
        
        draw.line((client_x, client_y - 40, 275, 450), fill="black", width=1)
        draw.text((200, 500), "HTTP / REST API", fill="black", font=small_font, anchor="mm")
        
        legend_rect = (800, 400, 1100, 600)
        draw.rectangle(legend_rect, outline="black", fill="white", width=1)
        draw.text((legend_rect[0] + 20, legend_rect[1] + 20), "凡例", fill="black", font=normal_font)
        
        legend_items = [
            "Windows ホストシステム: 物理マシン",
            "WSL: Linux 仮想環境",
            "FastAPI: Python Webアプリケーションフレームワーク",
            "Azure OpenAI: マイクロソフトのAIサービス"
        ]
        
        for i, item in enumerate(legend_items):
            y_pos = legend_rect[1] + 60 + i * 30
            draw.text((legend_rect[0] + 30, y_pos), item, fill="black", font=small_font)
        
        img.save(output_file, "JPEG", quality=95)
        print(f"Successfully created architecture diagram at {output_file}")
        return True
        
    except Exception as e:
        print(f"Error creating architecture diagram: {str(e)}")
        return False

def main():
    """
    メイン関数
    """
    output_file = "DOC/アーキテクチャ/システムアーキテクチャ図.jpg"
    
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    success = create_architecture_diagram(output_file)
    
    if success:
        print(f"Image generation successful. JPEG image saved to {output_file}")
        return 0
    else:
        print("Image generation failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
