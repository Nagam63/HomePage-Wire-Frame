from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)


# カテゴリごとのデータ
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

# 常時開催キャンペーンデータ
default_campaign = {
    'title': 'お友達紹介キャンペーン',
    'description': 'お友達を紹介していただくと、双方に特典があります！',
    'thumbnail': '/static/images/campaign/Brand-Image00.png',
    'start_date': datetime(2024, 1, 1),
    'end_date': datetime(2024, 12, 31)
}

# キャンペーンリスト
campaign_list = [
    {
        'id': 11,
        'title': '夏の特別割引',
        'excerpt': '夏の特別キャンペーン！お得な価格でご参加いただけます。',
        'thumbnail': '/static/images/campaign/Brand-Image00.png',
        'category': 'campaign',
        'tags': ['キャンペーン'],
        'start_date': datetime(2024, 8, 1),
        'end_date': datetime(2024, 8, 31),
        'content': [
            {
                'type': 'text',
                'size': '80vw',
                'text': 'この夏限定のお得なキャンペーン！そろばんのレッスンに特別割引価格で参加いただけます。ぜひ、この機会にご参加ください。'
            }
        ]
    },
    {
        'id': 12,
        'title': '新入生特典',
        'excerpt': '新しく入会された方には特典がつきます！',
        'thumbnail': '/static/images/campaign/Brand-Image00.png',
        'category': 'campaign',
        'tags': ['キャンペーン'],
        'start_date': datetime(2024, 9, 1),
        'end_date': datetime(2024, 12, 31),
        'content': [
            {
                'type': 'text',
                'size': '80vw',
                'text': '新しく入会された方には、初月のレッスンが無料になります。'
            }
        ]
    }
]
article_list = [
    {
        'id': 1,
        'title': '教室の紹介',
        'excerpt': 'そろばん教室の詳細について説明します。',
        'thumbnail': '/static/images/enrollment/IMG_3505.JPG',
        'category': 'classroom',
        'tags': ['教室'],
        'updated_at': datetime(2024, 8, 1),
        'content': [
            {
                'type': 'text',
                'size': '80vw',
                'text': 'そろばん教室では、計算力だけでなく、集中力や持続力の向上にも力を入れています。少人数制のクラスで、個々のペースに合わせたカリキュラムを実施し、生徒の自信を育みます。また、学ぶ楽しさを実感できるような工夫を凝らし、子どもたちが自然と意欲的に取り組める環境を提供しています。地域に密着し、保護者の皆様とも密にコミュニケーションを取りながら、一人ひとりの成長を見守っています。'
            },
            {
                'type': 'content-pair',
                'content': [
                    {
                        'type': 'image',
                        'size': '40vw',
                        'src': '/static/images/raw-background/IMG_0480.JPG'
                    },
                    {
                        'type': 'text',
                        'size': '40vw',
                        'text': 'そろばん教室は、計算力や集中力を高めるための最適な環境を提供します。生徒一人ひとりに合わせた指導法を取り入れ、基礎から応用までしっかりとサポートしています。'
                    }
                ]
            },
            {
                'type': 'content-pair',
                'content': [
                    {
                        'type': 'text',
                        'size': '40vw',
                        'text': '地域に根ざした教育を大切にし、楽しく学べる教室を目指しています。'
                    },
                    {
                        'type': 'image',
                        'size': '40vw',
                        'src': '/static/images/raw-background/IMG_0461.JPG'
                    }
                ]
            },
            {
                'type': 'text',
                'size': '80vw',
                'text': '教室では、計算力の向上だけでなく、日常生活で役立つスキルを総合的に学べるカリキュラムを提供しています。生徒たちは、学習を通じて論理的思考を養い、自己肯定感を高めることができます。'
            }
        ]
    },
    # 他の記事データ
    {
        'id': 2,
        'title': '検定の結果',
        'excerpt': '最近の検定結果についての報告です。',
        'thumbnail': '/static/images/features/IMG_3532.JPG',
        'category': 'exam',
        'tags': ['検定'],
        'updated_at': datetime(2024, 8, 2),
        'content': []
    },
    {
        'id': 3,
        'title': 'イベントレポート',
        'excerpt': '最近開催されたイベントの様子をお届けします。',
        'thumbnail': '/static/images/features/IMG_3648.JPG',
        'category': 'event',
        'tags': ['イベント'],
        'updated_at': datetime(2024, 8, 3),
        'content': []
    },
    {
        'id': 4,
        'title': '大会の結果',
        'excerpt': '最新の大会結果についてお知らせします。',
        'thumbnail': '/static/images/features/IMG_3660.JPG',
        'category': 'competition',
        'tags': ['大会'],
        'updated_at': datetime(2024, 8, 4),
        'content': []
    },
    {
        'id': 5,
        'title': '教室の設備',
        'excerpt': '教室の設備について紹介します。',
        'thumbnail': '/static/images/raw-background/IMG_3903.JPG',
        'category': 'classroom',
        'tags': ['教室','設備'],
        'updated_at': datetime(2024, 8, 5),
        'content': []
    },
    {
        'id': 6,
        'title': '競技大会',
        'excerpt': '競技大会の様子をお伝えします。',
        'thumbnail': '/static/images/raw-background/IMG_0461.JPG',
        'category': 'competition',
        'tags': ['大会', '競技'],
        'updated_at': datetime(2024, 8, 6),
        'content': []
    },
    {
        'id': 7,
        'title': '生徒の活動紹介',
        'excerpt': '生徒たちの日々の活動を紹介します。',
        'thumbnail': '/static/images/raw-background/IMG_0480.JPG',
        'category': 'classroom',
        'tags': ['教室', '活動'],
        'updated_at': datetime(2024, 8, 7),
        'content': []
    },
    {
        'id': 8,
        'title': '特別授業の案内',
        'excerpt': '特別授業についての案内を行います。',
        'thumbnail': '/static/images/raw-background/IMG_0484.JPG',
        'category': 'classroom',
        'tags': ['教室', '特別授業'],
        'updated_at': datetime(2024, 8, 8),
        'content': []
    },
    {
        'id': 9,
        'title': '年間行事予定',
        'excerpt': '年間行事予定についてお知らせします。',
        'thumbnail': '/static/images/raw-background/IMG_0485.JPG',
        'category': 'event',
        'tags': ['イベント', '予定'],
        'updated_at': datetime(2024, 8, 9),
        'content': []
    },
    {
        'id': 10,
        'title': '新入生歓迎イベント',
        'excerpt': '新入生を歓迎するイベントの様子をお届けします。',
        'thumbnail': '/static/images/raw-background/IMG_9919.JPG',
        'category': 'event',
        'tags': ['イベント', '新入生'],
        'updated_at': datetime(2024, 8, 10),
        'content': []
    }
] + campaign_list  # キャンペーンを記事リストに追加


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enrollment')
def enrollment():
    return render_template('enrollment.html')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/schedule')
def schedule():
    return render_template('schedule.html')

# 記事一覧ページ
@app.route('/articles')
def articles():
    # 更新日順にソート（キャンペーンは end_date を使用）
    sorted_articles = sorted(
        article_list, 
        key=lambda x: x.get('updated_at', x.get('end_date', datetime.min)), 
        reverse=True
    )
    return render_template('articles.html', articles=sorted_articles)

# 記事詳細ページ
@app.route('/article/<int:article_id>')
def article_detail(article_id):
    article = next((item for item in article_list if item["id"] == article_id), None)
    if article:
        category_info = category_data.get(article['category'], {})
        
        # 現在の日時でキャンペーンをフィルタリング
        current_date = datetime.now()
        active_campaigns = [campaign for campaign in campaign_list if campaign['start_date'] <= current_date <= campaign['end_date']]
        
        # 期間限定キャンペーンがない場合は常時開催キャンペーンを追加
        if not active_campaigns:
            active_campaigns.append(default_campaign)
        
        return render_template('article.html', article=article, category_info=category_info, campaigns=active_campaigns)
    else:
        return "Article not found", 404



if __name__ == '__main__':
    app.run(debug=True)
