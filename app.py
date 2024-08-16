from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_migrate import Migrate
from datetime import datetime
from models import db, Category, Article, Campaign, Content, User
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
import os
import secrets

app = Flask(__name__)

# セッションに必要なシークレットキーを設定
app.config['SECRET_KEY'] = secrets.token_hex(16)

# データベース設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///soroban_circle.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# データベースの初期化
db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

# ログイン管理の設定
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        flash('ユーザー名またはパスワードが間違っています')
        return redirect(url_for('articles'))
    login_user(user)
    return redirect(url_for('articles'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('articles'))

# アップロードされたファイルを保存するためのパスを指定
UPLOAD_FOLDER = 'static/images/articles'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


CATEGORY_TRANSLATIONS = {
    "classroom": "教室",
    "exam": "検定",
    "event": "イベント",
    "competition": "大会",
    "campaign": "キャンペーン"
}

# 新規記事作成
@app.route('/create_article', methods=['POST'])
@login_required
def create_article():
    try:
        # 受け取ったフォームデータをすべてログ出力
        form_data = request.form.to_dict()
        print("Received form data:")
        for key, value in form_data.items():
            print(f"{key}: {value}")

        title = request.form['title']
        category = request.form['category']
        excerpt = request.form['excerpt']
        tags = request.form['tags'].strip()

        # タグの整形
        autotag_english = f"{category}" if category else ''
        autotag_japanese = CATEGORY_TRANSLATIONS.get(category, category)

        all_tags = set(tag.strip() for tag in tags.replace('#', '').split(',') if tag.strip())
        if autotag_english in all_tags:
            all_tags.remove(autotag_english)
        all_tags.add(autotag_japanese)

        tags = ', '.join(f"#{tag}" for tag in all_tags)

        # サムネイル画像の処理
        thumbnail = request.files['thumbnail']
        if thumbnail:
            category_folder = os.path.join(app.config['UPLOAD_FOLDER'], category)
            if not os.path.exists(category_folder):
                os.makedirs(category_folder)
            filename = secure_filename(thumbnail.filename)
            thumbnail_path = os.path.join(category_folder, filename)
            thumbnail.save(thumbnail_path)

        # 新しい記事の作成
        new_article = Article(
            title=title,
            category_id=Category.query.filter_by(name=category).first().id,
            excerpt=excerpt,
            thumbnail=thumbnail_path,
            tags=tags.replace('#', ''),
            updated_at=datetime.utcnow()
        )
        db.session.add(new_article)
        db.session.flush()  # flush to get the article ID before committing

        # コンテンツブロックの処理
        content_count = request.form.get('content_count', type=int, default=0)
        print(f"Content count received: {content_count}")

        for i in range(1, content_count + 1):
            content_type = request.form.get(f'contentType{i}')
            print(f"Processing content block {i} with type: {content_type}")

            if content_type == '80vw':
                text = request.form.get(f'content80Text{i}')
                if text:
                    content_block = Content(
                        article_id=new_article.id,
                        type='text',
                        size='80vw',
                        text=text
                    )
                    db.session.add(content_block)
                    print(f"Added text block: {text}")
            elif content_type == 'content-pair':
                position = request.form.get(f'pairPosition{i}')
                text = request.form.get(f'contentPairText{i}')
                image = request.files.get(f'contentPairImage{i}')
                if image:
                    image_filename = secure_filename(image.filename)
                    image_path = os.path.join(app.config['UPLOAD_FOLDER'], category, image_filename)
                    image.save(image_path)
                    content_block = Content(
                        article_id=new_article.id,
                        type='content-pair',
                        size=position,
                        text=text,
                        src=image_path
                    )
                    db.session.add(content_block)
                    print(f"Added content-pair block with text: {text} and image: {image_path}")

        db.session.commit()
        flash('記事が作成されました。')
    except Exception as e:
        db.session.rollback()  # rollback in case of error
        flash(f"記事の作成中にエラーが発生しました: {str(e)}")
    return redirect(url_for('articles'))


# 記事編集
@app.route('/edit_article', methods=['POST'])
@login_required
def edit_article():
    try:
        article_id = request.form['article']
        article = Article.query.get_or_404(article_id)

        article.title = request.form['title']
        article.category_id = Category.query.filter_by(name=request.form['category']).first().id
        article.excerpt = request.form['excerpt']
        tags = request.form['tags']

        # タグの整形
        autotag = f"#{request.form['category']}" if request.form['category'] else ''
        if autotag and autotag not in tags:
            tags = f"{tags}, {autotag}" if tags else autotag
        article.tags = tags.replace('#', '')  # #記号を除去して保存

        # autotag を日本語に変換
        autotag = CATEGORY_TRANSLATIONS.get(request.form['category'], request.form['category'])
        if autotag and autotag not in tags:
            tags = f"{tags}, {autotag}" if tags else autotag
        article.tags = tags

        # サムネイル画像の処理
        if 'thumbnail' in request.files:
            thumbnail = request.files['thumbnail']
            if thumbnail:
                category_folder = os.path.join(app.config['UPLOAD_FOLDER'], request.form['category'])
                if not os.path.exists(category_folder):
                    os.makedirs(category_folder)
                
                filename = secure_filename(thumbnail.filename)
                thumbnail_path = os.path.join(category_folder, filename)
                thumbnail.save(thumbnail_path)
                article.thumbnail = thumbnail_path

        # コンテンツブロックの処理
        Content.query.filter_by(article_id=article.id).delete()  # 古いコンテンツを削除
        content_count = int(request.form.get('content_count', 0))

        for i in range(1, content_count + 1):
            content_type = request.form.get(f'contentType{i}')
            if content_type == '80vw':
                text = request.form.get(f'content80Text{i}')
                if text:
                    content_block = Content(
                        article_id=article.id,
                        type='text',
                        size='80vw',
                        text=text
                    )
                    db.session.add(content_block)
            elif content_type == 'content-pair':
                position = request.form.get(f'pairPosition{i}')
                text = request.form.get(f'contentPairText{i}')
                image = request.files.get(f'contentPairImage{i}')
                if image:
                    image_filename = secure_filename(image.filename)
                    image_path = os.path.join(app.config['UPLOAD_FOLDER'], request.form['category'], image_filename)
                    image.save(image_path)
                    content_block = Content(
                        article_id=article.id,
                        type='content-pair',
                        size=position,
                        text=text,
                        src=image_path
                    )
                    db.session.add(content_block)

        article.updated_at = datetime.utcnow()
        db.session.commit()
        flash('記事が更新されました。')
    except Exception as e:
        db.session.rollback()  # rollback in case of error
        flash(f"記事の更新中にエラーが発生しました: {str(e)}")
    return redirect(url_for('articles'))


# 記事データ取得（記事編集用）
@app.route('/get_article_data/<int:article_id>', methods=['GET'])
def get_article_data(article_id):
    article = Article.query.get_or_404(article_id)
    content_blocks = []

    for block in article.content:
        content_blocks.append({
            'type': block.type,
            'size': block.size,  # 80vw or content-pairの場合のサイズ
            'text': block.text,  # テキストがある場合
            'position': block.size if block.type == 'content-pair' else None,  # content-pairの場合の位置
            'src': block.src  # 画像がある場合のパス
        })

    return jsonify({
        'title': article.title,
        'category': article.category.name,
        'excerpt': article.excerpt,
        'autoTag': f"#{article.category.name}",
        'tags': article.tags,
        'content': content_blocks
    })

# 記事削除
@app.route('/delete_article', methods=['POST'])
@login_required
def delete_article():
    article_id = request.form['article']
    article = Article.query.get_or_404(article_id)
    db.session.delete(article)
    db.session.commit()
    flash('記事が削除されました。')
    return redirect(url_for('articles'))



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
    'id':0,
    'title': 'お友達紹介キャンペーン',
    'excerpt': 'お友達を紹介していただくと、双方に特典があります！',
    'thumbnail': '/static/images/campaign/Brand-Image00.png',
    'category': 'campaign',
    'tags': ['キャンペーン'],
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
] 


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


@app.route('/articles')
def articles():
    try:
        # データベースから記事を読み込む
        articles = Article.query.order_by(Article.updated_at.desc()).all()

        # カテゴリ名をテンプレートに渡すための処理
        articles_with_categories = []
        for article in articles:
            article_data = {
                'id': article.id,
                'title': article.title,
                'excerpt': article.excerpt,
                'thumbnail': article.thumbnail,
                'category': article.category.name,
                'tags': article.tags.split(','),  # タグをカンマで分割してリストとして渡す
                'updated_at': article.updated_at
            }
            articles_with_categories.append(article_data)

        # データベースからキャンペーンを読み込む
        campaigns = Campaign.query.order_by(Campaign.end_date.desc()).all()

        # 記事リストにキャンペーンを追加
        all_items = articles_with_categories + campaigns
        
        # 日付順にソート（記事はupdated_at、キャンペーンはend_dateを使用）
        all_items.sort(key=lambda x: x['updated_at'] if 'updated_at' in x else x.end_date, reverse=True)
        
        # デフォルトキャンペーンを一位に追加
        all_items.insert(0, default_campaign)
        if not all_items:
            raise Exception("No articles found in the database.")

    except Exception as e:
        # エラーが発生した場合、またはデータが見つからなかった場合、フォールバックとしてリストデータを使用
        all_items = article_list + campaign_list
        all_items.sort(key=lambda x: x.get('updated_at', x.get('end_date', datetime.min)), reverse=True)
        # デフォルトキャンペーンを一位に追加
        all_items.insert(0, default_campaign)

    return render_template('articles.html', articles=all_items)



# 記事詳細ページ
@app.route('/article/<int:article_id>')
def article_detail(article_id):
    try:
        # データベースから記事を取得
        article = Article.query.get_or_404(article_id)
        category_info = Category.query.filter_by(id=article.category_id).first()

        # デバッグ情報
        print(f"Article ID: {article.id}")
        print(f"Title: {article.title}")
        print(f"Excerpt: {article.excerpt}")
        print(f"Category ID: {article.category_id}")
        print(f"Thumbnail: {article.thumbnail}")
        print(f"Tags: {article.tags}")
        print(f"Content Blocks: {article.contents}")

        if not article.contents:
            print("No content blocks found for this article.")
        else:
            for block in article.contents:
                print(f"Content Block ID: {block.id}, Type: {block.type}, Text: {block.text}, Image: {block.src}")

        # 現在の日時でキャンペーンをフィルタリング
        current_date = datetime.now()
        active_campaigns = Campaign.query.filter(Campaign.start_date <= current_date, Campaign.end_date >= current_date).all()

        # 期間限定キャンペーンがない場合は常時開催キャンペーンを追加
        if not active_campaigns:
            active_campaigns = [default_campaign]

    except Exception as e:
        # データベースから取得できない場合のフォールバック
        print(f"Error retrieving article: {e}")
        article = next((item for item in article_list if item["id"] == article_id), None)
        category_info = category_data.get(article['category'], {})
        active_campaigns = [campaign for campaign in campaign_list if campaign['start_date'] <= datetime.now() <= campaign['end_date']]

        if not article:
            return "Article not found", 404

    return render_template('article.html', article=article, category_info=category_info, campaigns=active_campaigns)

if __name__ == '__main__':
    app.run(debug=True)