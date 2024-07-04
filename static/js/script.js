// script.js
document.addEventListener('DOMContentLoaded', function() {
    // ハンバーガーメニューのトグル
    const hamburger = document.querySelector('.hamburger');
    const navUL = document.querySelector('nav ul');

    hamburger.addEventListener('click', function() {
        navUL.classList.toggle('active');
    });

    // Slick Sliderの初期化
    $('.schedule-carousel').slick({
        dots: true,
        infinite: true,
        autoplayspeed: 100,
        autoplay: true, // 自動再生を有効にする
        slidesToShow: 3,
        centerMode: true,
        variableWidth: true,
        dots: true, // ドットナビゲーションを表示

    });

    $('.classroom-carousel').slick({
        centerMode: true, // 中央モードを有効化
        centerPadding: '60px', // 中央の画像の両側に余白を設ける
        slidesToShow: 1, // 画面に表示するスライドの数
        autoplay: true, // 自動再生を有効にする
        autoplaySpeed: 2000, // 自動再生のスピード（ミリ秒）
        dots: true, // ドットナビゲーションを表示
        variableWidth: true,

        responsive: [{
            breakpoint: 768, // 768px以下のサイズに適用
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
    });
    $('.classroom-carousel').on('afterChange', function() {
        $('.slick-current').addClass('is--active');
    });



    // カスタムカルーセルロジック
    let boxes = document.querySelectorAll('.class-box');
    let carousel = document.querySelector('.schedule-carousel');
    let currentIndex = 0;
    let isHovering = false; // ホバー状態を追跡するための変数

    function moveToBox(index) {
        if (!isHovering) {
            boxes[currentIndex].classList.remove('active-box');
            currentIndex = index;
            boxes[currentIndex].classList.add('active-box');

            let scrollX = boxes[currentIndex].offsetLeft - (carousel.offsetWidth / 2) + (boxes[currentIndex].offsetWidth / 2);
            carousel.scrollLeft = scrollX;
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

    moveToBox(0); // 初期設定
    setInterval(centerActiveBox, 3000); // 3秒ごとに中央のBOXを更新
    $(function() {
        $('a[href^="#"]').click(function() {
            var speed = 500; // スクロール速度(ミリ秒)
            var href = $(this).attr("href");
            var target = $(href == "#" || href == "" ? 'html' : href);
            var position = target.offset().top;
            $('html, body').animate({ scrollTop: position }, speed, 'swing');
            return false;
        });
    });

    // 次の/前のスライドへ移動する関数
    window.moveSlide = function(n) {
        showSlides(slideIndex += n);
    }




});