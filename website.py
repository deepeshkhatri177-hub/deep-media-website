from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Deep Media Group</title>

        <style>
            * {
                box-sizing: border-box;
            }

            body {
                margin: 0;
                min-height: 100vh;
                color: white;
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 55px 20px;
                overflow-x: hidden;
            }

            #bgvideo {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                object-fit: cover;
                z-index: -2;
            }

            .overlay {
                position: fixed;
                inset: 0;
                background: rgba(0, 0, 0, 0.64);
                z-index: -1;
            }

            .hero-title {
                color: #00bfff;
                font-size: clamp(38px, 7vw, 68px);
                margin: 0;
                animation: titleUp 1.2s ease-out both, glow 2s ease-in-out infinite alternate;
            }

            .hero-subtitle {
                font-size: clamp(20px, 3vw, 28px);
                margin: 18px 0;
                animation: fadeIn 1.5s ease-out 0.5s both;
            }

            .intro {
                max-width: 700px;
                margin: 0 auto 32px;
                line-height: 1.7;
                animation: fadeIn 1.5s ease-out 0.9s both;
            }

            .box {
                background: rgba(0, 0, 0, 0.66);
                backdrop-filter: blur(7px);
                padding: 24px;
                border: 1px solid rgba(0, 191, 255, 0.35);
                border-radius: 16px;
                margin: 22px auto;
                width: min(760px, 92%);
                line-height: 1.65;
                animation: fadeInUp 0.8s ease-out both;
                transition: transform 0.3s ease, border-color 0.3s ease;
            }

            .box:hover {
                transform: translateY(-6px);
                border-color: #00bfff;
            }

            .box h2 {
                color: #00bfff;
            }

            .btn {
                display: inline-block;
                background: #00bfff;
                color: white;
                padding: 13px 22px;
                border-radius: 10px;
                font-size: 17px;
                font-weight: bold;
                transition: 0.3s ease;
            }

            .btn:hover {
                background: white;
                color: #0077a8;
                transform: scale(1.05);
            }

            a {
                text-decoration: none;
            }

            @keyframes titleUp {
                from { opacity: 0; transform: translateY(45px); }
                to { opacity: 1; transform: translateY(0); }
            }

            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }

            @keyframes fadeInUp {
                from { opacity: 0; transform: translateY(25px); }
                to { opacity: 1; transform: translateY(0); }
            }

            @keyframes glow {
                from { text-shadow: 0 0 10px #00bfff; }
                to { text-shadow: 0 0 28px #00bfff, 0 0 48px #0077ff; }
            }
        </style>
    </head>

    <body>
        <video autoplay muted loop playsinline id="bgvideo">
            <source src="/static/background.mp4" type="video/mp4">
        </video>

        <div class="overlay"></div>

        <h1 class="hero-title">Deep Media Group</h1>
        <h2 class="hero-subtitle">Professional Video Editing Services 🎬</h2>

        <p class="intro">
            High Quality Reels, Wedding Edits, Anniversary Videos,
            Client Projects and Social Media Content.
        </p>

        <div class="box">
            <h2>About Me</h2>
            <p>
                Hi, I'm Deepesh. I help clients transform their raw footage
                into professional and engaging videos for social media and
                personal memories.
            </p>
        </div>

        <div class="box">
            <h2>Services Available ✅</h2>
            <p>💍 Wedding Video Editing</p>
            <p>🎉 Anniversary Video Editing</p>
            <p>🎂 Birthday Highlights</p>
            <p>📱 Instagram Reels Editing</p>
            <p>🎥 Personal Client Projects</p>
            <p>🏢 Business Promotional Videos</p>
            <p>🎞️ Cinematic Video Editing</p>
            <p>✨ Color Grading & Effects</p>
        </div>

        <div class="box">
            <h2>Why Choose Me?</h2>
            <p>
                ✔ Professional Quality<br>
                ✔ Fast Delivery<br>
                ✔ Smooth Transitions<br>
                ✔ Cinematic Look<br>
                ✔ Client Satisfaction First
            </p>
        </div>

        <div class="box">
            <h2>Contact</h2>
            <p>Instagram: @deepmediagroup</p>

            <a href="https://instagram.com/deepmediagroup" target="_blank">
                <span class="btn">Contact on Instagram</span>
            </a>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run()
