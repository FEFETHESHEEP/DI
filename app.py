<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { margin: 0; padding: 20px; font-family: 'Segoe UI', sans-serif; text-align: center; background-color: #fff0f5; min-height: 100vh; }
        .card { background: white; padding: 30px; border-radius: 20px; display: inline-block; box-shadow: 0 4px 15px rgba(0,0,0,0.1); width: 100%; max-width: 400px; margin-top: 50px; }
        .hidden { display: none; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 20px 0; }
        .option { padding: 15px; border: 2px solid #ffb6c1; border-radius: 10px; cursor: pointer; }
        .option.selected { background: #ffb6c1; color: white; border-color: #ff69b4; }
        button { padding: 15px 30px; border-radius: 10px; border: none; background: #ffb6c1; color: white; font-weight: bold; cursor: pointer; }
        textarea { width: 100%; margin: 15px 0; padding: 10px; border-radius: 10px; border: 1px solid #ffb6c1; box-sizing: border-box; }
    </style>
</head>
<body>
    <div id="homepage" class="card">
        <h1>Hello my Moon 🌙</h1>
        <button onclick="document.getElementById('homepage').style.display='none'; document.getElementById('formPage').classList.remove('hidden');">Let's get started</button>
    </div>

    <div id="formPage" class="card hidden">
        <h1>What would you like to do? ✨</h1>
        <div class="grid">
            <div class="option" onclick="selectVibe(this, 'River Thames')">River Thames 🌊</div>
            <div class="option" onclick="selectVibe(this, 'Ashley Park')">Ashley Park 🌳</div>
            <div class="option" onclick="selectVibe(this, 'The Heart')">The Heart 🛍️</div>
            <div class="option" onclick="selectVibe(this, 'Cinema')">Cinema 🎬</div>
        </div>
        <textarea id="notes" placeholder="Any notes for me?"></textarea>
        <input type="date" id="date" style="width:100%; padding:10px; margin-bottom:20px;">
        <button onclick="sendDate()">Set the date! 💖</button>
    </div>

    <script>
        let selectedVibe = "";
        function selectVibe(el, v) { 
            selectedVibe = v; 
            document.querySelectorAll('.option').forEach(o => o.classList.remove('selected')); 
            el.classList.add('selected'); 
        }
        async function sendDate() {
            const date = document.getElementById('date').value;
            const notes = document.getElementById('notes').value;
            if (!selectedVibe || !date) return alert("Select place & date!");
            
            // CHANGE 'YOUR_APP_NAME' BELOW TO YOUR ACTUAL RAILWAY APP NAME
            const res = await fetch('date.up.railway.app', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ activity: selectedVibe, date: date, notes: notes })
            });
            
            if (res.ok) alert('Date set, Love you! 💖');
            else alert('Error: Server did not respond. Check the F12 Console.');
        }
    </script>
</body>
</html>
