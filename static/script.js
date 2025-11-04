let timerInterval;

function formatTime(totalSeconds) {
    const days = Math.floor(totalSeconds  / 86400);
    const hours = Math.floor((totalSeconds % 86400) / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const seconds = totalSeconds % 60;

    const dd = String(days).padStart(2, '0');
    const hh = String(hours).padStart(2, '0');
    const mm = String(minutes).padStart(2, '0');
    const ss = String(seconds).padStart(2, '0');

    return `${dd}:${hh}:${mm}:${ss}`;
}

function startLocalCountdown(seconds) {
    clearInterval(timerInterval);

    let remaining = seconds;
    document.getElementById('timerDisplay').textContent = formatTime(remaining);

    timerInterval = setInterval(() => {
        remaining--;
        if (remaining < 0) {
            clearInterval(timerInterval);
            document.getElementById('timerDisplay').textContent = "Time's up!";
            return;
        }
        document.getElementById('timerDisplay').textContent = formatTime(remaining);}, 1000);
    }

    async function fetchRemainingTime() {
        try {
            const res = await fetch('/get-remaining-time');
            const data = await res.json();
            return data.remaining_seconds;
        } catch (err) {
            console.error('Failed to fetch remaining time:', err);
            return 0
        }
    }

    document.getElementById('submitBtn').addEventListener('click', async () => {
        const days = parseInt(document.getElementById('days').value) || 0;
        const hours = parseInt(document.getElementById('hours').value) || 0;
        const minutes = parseInt(document.getElementById('minutes').value) || 0;
        const seconds = parseInt(document.getElementById('seconds').value) || 0;
        // Prevents negative input
        if (days < 0 || hours < 0 || minutes < 0 || seconds < 0) {
            alert("Please enter only positive numbers.");
            return;
        }

        const total = days + hours + minutes + seconds;
        if (total === 0) {
            alert("Please enter a duration greater than 0.");
            return;
        }

        const submitBtn = document.getElementById('submitBtn');
        submitBtn.disabled = true;

        try {
            await fetch('/submit-time', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify ({days, hours, minutes, seconds })
            });

            const remaining = await fetchRemainingTime();
            startLocalCountdown(remaining);
        } catch (err) {
            console.error('Error submitting time:', err);
            alert('Failed to submit timer. Please try again.');
        } finally {
            submitBtn.disabled = false;
        }
    });

    document.getElementById('syncBtn').addEventListener('click', async () => {
        const remaining = await fetchRemainingTime();
        startLocalCountdown(remaining);
    });

    window.onload = async () => {
        const remaining = await fetchRemainingTime();
        if (remaining > 0) startLocalCountdown(remaining);
    };
