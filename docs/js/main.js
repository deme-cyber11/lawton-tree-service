/* ============================================
   Lawton Tree Pros — Main JS
   ============================================ */

(function () {
  'use strict';

  /* --- Sticky Header Scroll --- */
  const header = document.querySelector('.site-header');
  if (header) {
    window.addEventListener('scroll', function () {
      header.classList.toggle('scrolled', window.scrollY > 50);
    }, { passive: true });
  }

  /* --- Mobile Menu Toggle --- */
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.main-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      nav.classList.toggle('open');
      const expanded = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', !expanded);
    });
    document.addEventListener('click', function (e) {
      if (!toggle.contains(e.target) && !nav.contains(e.target)) {
        nav.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  /* --- Before/After Slider --- */
  document.querySelectorAll('.before-after-slider').forEach(function (slider) {
    var handle = slider.querySelector('.ba-slider-handle');
    var line = slider.querySelector('.ba-slider-line');
    var beforeImg = slider.querySelector('.ba-img-before');
    var isDragging = false;

    function updateSlider(x) {
      var rect = slider.getBoundingClientRect();
      var pct = Math.max(0, Math.min(100, ((x - rect.left) / rect.width) * 100));
      beforeImg.style.clipPath = 'inset(0 ' + (100 - pct) + '% 0 0)';
      handle.style.left = pct + '%';
      line.style.left = pct + '%';
    }

    handle.addEventListener('mousedown', function (e) {
      e.preventDefault();
      isDragging = true;
    });
    document.addEventListener('mousemove', function (e) {
      if (isDragging) updateSlider(e.clientX);
    });
    document.addEventListener('mouseup', function () {
      isDragging = false;
    });

    handle.addEventListener('touchstart', function (e) {
      isDragging = true;
    }, { passive: true });
    slider.addEventListener('touchmove', function (e) {
      if (isDragging) {
        updateSlider(e.touches[0].clientX);
      }
    }, { passive: true });
    document.addEventListener('touchend', function () {
      isDragging = false;
    });

    slider.addEventListener('click', function (e) {
      updateSlider(e.clientX);
    });
  });

  /* --- FAQ Accordion --- */
  document.querySelectorAll('.faq-question').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var item = btn.closest('.faq-item');
      var answer = item.querySelector('.faq-answer');
      var isActive = item.classList.contains('active');

      item.closest('.faq-list').querySelectorAll('.faq-item.active').forEach(function (open) {
        open.classList.remove('active');
        open.querySelector('.faq-answer').style.maxHeight = null;
      });

      if (!isActive) {
        item.classList.add('active');
        answer.style.maxHeight = answer.scrollHeight + 'px';
      }
    });
  });

  /* --- Contact Form (Web3Forms) --- */
  var form = document.getElementById('contact-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var btn = form.querySelector('button[type="submit"]');
      var origText = btn.textContent;
      btn.textContent = 'Sending...';
      btn.disabled = true;

      fetch('https://api.web3forms.com/submit', {
        method: 'POST',
        body: new FormData(form)
      })
        .then(function (res) { return res.json(); })
        .then(function (data) {
          if (data.success) {
            window.location.href = '/thank-you.html';
          } else {
            btn.textContent = 'Error — Try Again';
            btn.disabled = false;
            setTimeout(function () { btn.textContent = origText; }, 3000);
          }
        })
        .catch(function () {
          btn.textContent = 'Error — Try Again';
          btn.disabled = false;
          setTimeout(function () { btn.textContent = origText; }, 3000);
        });
    });
  }

})();
