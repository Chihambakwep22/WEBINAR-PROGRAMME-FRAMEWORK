(function () {
    var countdownEl = document.querySelector('.countdown');
    if (countdownEl) {
        var eventStart = countdownEl.getAttribute('data-event-start');
        var target = new Date(eventStart).getTime();

        function renderCountdown() {
            var now = Date.now();
            var diff = Math.max(0, target - now);

            var days = Math.floor(diff / (1000 * 60 * 60 * 24));
            var hours = Math.floor((diff / (1000 * 60 * 60)) % 24);
            var minutes = Math.floor((diff / (1000 * 60)) % 60);
            var seconds = Math.floor((diff / 1000) % 60);

            var d = document.getElementById('cd-days');
            var h = document.getElementById('cd-hours');
            var m = document.getElementById('cd-minutes');
            var s = document.getElementById('cd-seconds');

            if (d) d.textContent = String(days).padStart(2, '0');
            if (h) h.textContent = String(hours).padStart(2, '0');
            if (m) m.textContent = String(minutes).padStart(2, '0');
            if (s) s.textContent = String(seconds).padStart(2, '0');
        }

        renderCountdown();
        setInterval(renderCountdown, 1000);
    }

    var ctas = document.querySelectorAll('[data-track="offer_click"]');
    ctas.forEach(function (btn) {
        btn.addEventListener('click', function () {
            var csrf = document.querySelector('input[name="csrfmiddlewaretoken"]');
            var body = new URLSearchParams();
            body.append('event_type', btn.getAttribute('data-track') || 'offer_click');
            body.append('cta_url', btn.getAttribute('data-url') || '');
            body.append('registration_id', btn.getAttribute('data-registration') || '');

            fetch('/track-click/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrf ? csrf.value : ''
                },
                body: body.toString()
            });
        });
    });
})();
