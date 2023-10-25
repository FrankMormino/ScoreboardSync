// static/js/main.js

document.addEventListener("DOMContentLoaded", function() {
    // Placeholder for any JavaScript functionality you'll add later
    console.log('ScoreboardSync loaded successfully');
});

document.getElementById('link-calendar-form').addEventListener('submit', function(e) {
    var calendarUrl = document.getElementById('calendar_url').value;
    if (!calendarUrl) {
        alert('Please enter a Calendar URL');
        e.preventDefault();
    }
});
// ... existing code ...
document.getElementById('link-calendar-form').addEventListener('submit', function(e) {
    // ... existing code ...
    document.getElementById('loading-spinner').style.display = 'block';
});
