
document.addEventListener('DOMContentLoaded', function () {
    // Reusable Carousel Function
    const initCarousel = (trackSelector, navSelector, prevBtnSelector, nextBtnSelector, interval = 6000) => {
        const track = document.querySelector(trackSelector);
        if (!track) return;

        const slides = Array.from(track.children);
        const dotsNav = document.querySelector(navSelector);
        const dots = dotsNav ? Array.from(dotsNav.children) : [];
        const nextButton = document.querySelector(nextBtnSelector);
        const prevButton = document.querySelector(prevBtnSelector);

        if (slides.length === 0) return;

        // Check if slides are absolute (Hero) or relative/flex (Testimonials)
        // If absolute, we need to set 'left' property.
        // If relative/flex, we don't set 'left', the browser handles layout.
        const firstSlideStyle = window.getComputedStyle(slides[0]);
        const isAbsolute = firstSlideStyle.position === 'absolute';

        let slideWidth = slides[0].getBoundingClientRect().width;

        // 1. Position slides if needed
        const setSlidePosition = (slide, index) => {
            if (isAbsolute) {
                slide.style.left = slideWidth * index + 'px';
            }
        };
        slides.forEach(setSlidePosition);

        // 2. Move Logic
        const moveToSlide = (track, currentSlide, targetSlide) => {
            // For both cases, we translate the TRACK.
            // For Absolute: track moves -target.style.left
            // For Flex: track moves -(slideWidth * index)

            let amountToMove;

            if (isAbsolute) {
                amountToMove = targetSlide.style.left;
            } else {
                // Find index of target slide
                const targetIndex = slides.findIndex(slide => slide === targetSlide);
                amountToMove = (targetIndex * slideWidth) + 'px';
            }

            track.style.transform = 'translateX(-' + amountToMove + ')';

            currentSlide.classList.remove('current-slide');
            targetSlide.classList.add('current-slide');
        };

        const updateDots = (currentDot, targetDot) => {
            if (!currentDot || !targetDot) return;
            currentDot.classList.remove('active');
            targetDot.classList.add('active');
        };

        // Handle Window Resize
        window.addEventListener('resize', () => {
            slideWidth = slides[0].getBoundingClientRect().width;

            if (isAbsolute) {
                slides.forEach((slide, index) => {
                    slide.style.left = slideWidth * index + 'px';
                });
            }

            const currentSlide = track.querySelector('.current-slide');
            if (currentSlide) {
                // Determine re-center position
                let amountToMove;
                if (isAbsolute) {
                    amountToMove = currentSlide.style.left;
                } else {
                    const currentIndex = slides.findIndex(slide => slide === currentSlide);
                    amountToMove = (currentIndex * slideWidth) + 'px';
                }
                track.style.transform = 'translateX(-' + amountToMove + ')';
            }
        });

        // Navigation Handlers (Shared)
        const handleNav = (direction) => {
            const currentSlide = track.querySelector('.current-slide');
            const currentDot = dotsNav ? dotsNav.querySelector('.active') : null;

            let nextSlide, nextDot;

            if (direction === 'next') {
                nextSlide = currentSlide.nextElementSibling;
                nextDot = currentDot ? currentDot.nextElementSibling : null;
                if (!nextSlide) {
                    nextSlide = slides[0];
                    if (dots.length > 0) nextDot = dots[0];
                }
            } else {
                nextSlide = currentSlide.previousElementSibling;
                nextDot = currentDot ? currentDot.previousElementSibling : null;
                if (!nextSlide) {
                    nextSlide = slides[slides.length - 1];
                    if (dots.length > 0) nextDot = dots[dots.length - 1];
                }
            }

            moveToSlide(track, currentSlide, nextSlide);
            updateDots(currentDot, nextDot);
            resetAutoPlay();
        };

        if (nextButton) nextButton.addEventListener('click', () => handleNav('next'));
        if (prevButton) prevButton.addEventListener('click', () => handleNav('prev'));

        if (dotsNav) {
            dotsNav.addEventListener('click', e => {
                const targetDot = e.target.closest('button');
                if (!targetDot) return;

                const currentSlide = track.querySelector('.current-slide');
                const currentDot = dotsNav.querySelector('.active');
                const targetIndex = dots.findIndex(dot => dot === targetDot);
                const targetSlide = slides[targetIndex];

                moveToSlide(track, currentSlide, targetSlide);
                updateDots(currentDot, targetDot);
                resetAutoPlay();
            });
        }

        // Auto-play
        let autoPlayInterval;
        const startAutoPlay = () => {
            autoPlayInterval = setInterval(() => {
                const currentSlide = track.querySelector('.current-slide');
                if (!currentSlide) return;

                let nextSlide = currentSlide.nextElementSibling;
                const currentDot = dotsNav ? dotsNav.querySelector('.active') : null;
                let nextDot = currentDot ? currentDot.nextElementSibling : null;

                if (!nextSlide) {
                    nextSlide = slides[0];
                    if (dots.length > 0) nextDot = dots[0];
                }

                moveToSlide(track, currentSlide, nextSlide);
                updateDots(currentDot, nextDot);
            }, interval);
        };

        const resetAutoPlay = () => {
            clearInterval(autoPlayInterval);
            startAutoPlay();
        };

        startAutoPlay();
    };

    // Hero Carousel (Absolute Positioning)
    initCarousel(
        '.carousel-track',
        '.carousel-bar-nav',
        '.carousel-btn.prev-btn',
        '.carousel-btn.next-btn',
        6000
    );

    // Testimonial Carousel (Flexbox Positioning)
    initCarousel(
        '.testimonial-track',
        '.testimonial-nav',
        '.testimonial-btn.prev-btn',
        '.testimonial-btn.next-btn',
        5000
    );

    // Navbar Scroll Logic
    const header = document.querySelector('header');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });

    // Active Link Highlighting
    const currentPath = window.location.pathname;
    const navItems = document.querySelectorAll('.nav-links a');
    navItems.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    // Hamburger Menu Logic
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    if (hamburger && navLinks) {
        hamburger.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            hamburger.classList.toggle('active');
        });

        const links = navLinks.querySelectorAll('a');
        links.forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
                hamburger.classList.remove('active');
            });
        });
    }
});
