document.addEventListener('DOMContentLoaded', function() {
    // フィルターボタンのクリックイベント
    document.querySelectorAll('.filter-btn').forEach(button => {
        button.addEventListener('click', function() {
            const selectedCategory = this.getAttribute('data-category');
            console.log('Selected Category:', selectedCategory); // 追加
            
            const articles = document.querySelectorAll('.article-item');
            
            articles.forEach(article => {
                console.log('Article Category:', article.getAttribute('data-category')); // 追加
                if (selectedCategory === 'all' || article.getAttribute('data-category') === selectedCategory) {
                    article.style.display = 'flex';
                } else {
                    article.style.display = 'none';
                }
            });
    
            document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
        });
    });
    // ハンバーガーメニューのトグル
    document.querySelector('.hamburger').addEventListener('click', function() {
        document.querySelector('nav ul').classList.toggle('active');
    });

    // Slick Sliderの初期化
    $('.schedule-carousel').slick({
        dots: true,
        infinite: true,
        autoplayspeed: 100,
        autoplay: true,
        slidesToShow: 3,
        centerMode: true,
        variableWidth: true
    });

    $('.classroom-carousel').slick({
        centerMode: true,
        centerPadding: '60px',
        slidesToShow: 1,
        autoplay: true,
        autoplaySpeed: 2000,
        dots: true,
        variableWidth: true,
        responsive: [{
            breakpoint: 768,
            settings: {
                arrows: false,
                centerMode: true,
                centerPadding: '40px',
                slidesToShow: 1
            }
        }]
    });

    // スライダー変更時のイベントハンドラを追加
    $('.classroom-carousel').on('beforeChange', function() {
        $('.slick-current').removeClass('is--active');
    }).on('afterChange', function() {
        $('.slick-current').addClass('is--active');
    });

    // カスタムカルーセルロジック
    const boxes = document.querySelectorAll('.class-box');
    const carousel = document.querySelector('.schedule-carousel');
    let currentIndex = 0;
    let isHovering = false;

    function moveToBox(index) {
        if (!isHovering) {
            boxes[currentIndex].classList.remove('active-box');
            currentIndex = index;
            boxes[currentIndex].classList.add('active-box');
            carousel.scrollLeft = boxes[currentIndex].offsetLeft - (carousel.offsetWidth / 2) + (boxes[currentIndex].offsetWidth / 2);
        }
    }

    function centerActiveBox() {
        if (!isHovering) {
            moveToBox(currentIndex);
        }
    }

    boxes.forEach((box, index) => {
        box.addEventListener('mouseover', () => {
            isHovering = true;
            boxes[currentIndex].classList.remove('active-box');
            box.classList.add('active-box');
        });

        box.addEventListener('mouseout', () => {
            isHovering = false;
            box.classList.remove('active-box');
            boxes[currentIndex].classList.add('active-box');
        });
    });

    moveToBox(0);
    setInterval(centerActiveBox, 3000);

    // Smooth scroll for anchor links
    $('a[href^="#"]').click(function() {
        const target = $(this.getAttribute('href'));
        $('html, body').animate({ scrollTop: target.offset().top }, 500, 'swing');
        return false;
    });
});