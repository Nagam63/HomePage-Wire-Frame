from models import Category, db
from app import app

def save_categories_to_db():
    category_data = {
        'classroom': {
            'background_image': '/static/images/article/classroom001.jpg',
            'title': '教室紹介',
            'description': 'そろばん教室では、計算力だけでなく、集中力や持続力の向上にも力を入れています。'
        },
        'exam': {
            'background_image': '/static/images/article/Brand-Image00.png',
            'title': '検定結果',
            'description': 'そろばん検定の結果発表！努力の成果を確認し、次へのステップに進みましょう。'
        },
        'event': {
            'background_image': '/static/images/article/event001.jpg',
            'title': 'イベントレポート',
            'description': '楽しいイベントが盛りだくさん！そろばんサークルの最新イベント情報をお届けします。'
        },
        'competition': {
            'background_image': '/static/images/article/competition001.jpg',
            'title': '大会結果',
            'description': 'そろばん大会の結果発表！全国から集まった精鋭たちが繰り広げた熱戦をレポートします。'
        },
        'campaign': {
            'background_image': '/static/images/article/campaign001.jpg',
            'title': 'キャンペーン情報',
            'description': 'お得なキャンペーン情報をお見逃しなく！'
        }
    }

    with app.app_context():
        for key, value in category_data.items():
            category = Category(name=key, background_image=value['background_image'], title=value['title'], description=value['description'])
            db.session.add(category)
        db.session.commit()
        print("Categories saved to the database.")

if __name__ == '__main__':
    save_categories_to_db()
