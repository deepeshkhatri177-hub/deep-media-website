from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Deep Media Group</title>

        <style>
            * {
                box-sizing: border-box;
            }

            body {
                margin: 0;
                min-height: 100vh;
                padding: 55px 20px;
                color: white;
                font-family: Arial, sans-serif;
                text-align: center;
                background: linear-gradient(-45deg, #050b2c, #102b6a, #5a1674, #007b9e);
                background-size: 400% 400%;
                animation: gradientMove 12s ease infinite;
            }

            .hero-title {
                color: white;
                font-size: clamp(38px, 7vw, 68px);
                margin: 0;
                animation: titleUp 1s ease-out both, glow 2s ease-in-out infinite alternate;
            }

            .hero-subtitle {
                color: #a8eaff;
                font-size: clamp(20px, 3vw, 28px);
                margin: 18px 0;
                animation: fadeIn 1.5s ease-out 0.4s both;
            }

            .intro {
                max-width: 700px;
                margin: 20px auto 35px;
                line-height: 1.7;
                color: #e8f8ff;
                animation: fadeIn 1.5s ease-out 0.8s both;
            }

            .box {
                width: min(760px, 92%);
                margin: 22px auto;
                padding: 25px;
                border-radius: 20px;
                background: rgba(255, 255, 255, 0.12);
                border: 1px solid rgba(255, 255, 255, 0.25);
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.22);
                backdrop-filter: blur(12px);
                line-height: 1.65;
                animation: fadeInUp 0.8s ease-out both;
                transition: 0.3s ease;
            }

            .box:hover {
                transform: translateY(-7px);
                background: rgba(255, 255, 255, 0.18);
            }

            .box h2 {
                color: #7cecff;
                margin-top: 0;
            }

            .service-list p {
                margin: 9px 0;
            }

            .btn {
                display: inline-block;
                background: linear-gradient(90deg, #00bfff, #8b5cf6);
                color: white;
                padding: 14px 24px;
                border-radius: 30px;
                font-size: 17px;
                font-weight: bold;
                transition: 0.3s ease;
            }

            .btn:hover {
                transform: scale(1.08);
                box-shadow: 0 0 22px #00bfff;
            }

            a {
                text-decoration: none;
            }

            @keyframes gradientMove {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }

            @keyframes titleUp {
                from {
                    opacity: 0;
                    transform: translateY(40px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }

            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(25px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            @keyframes glow {
                from { text-shadow: 0 0 10px #00bfff; }
                to { text-shadow: 0 0 28px #8b5cf6; }
            }
        </style>
    </head>

    <body>
        <h1 class="hero-title">Deep Media Group</h1>

        <h2 class="hero-subtitle">
            Professional Video Editing Services 🎬
        </h2>

        <p class="intro">
            High Quality Reels, Wedding Edits, Anniversary Videos,
            Client Projects and Social Media Content.
        </p>

        <div class="box">
            <h2>About Me</h2>
            <p>
                Hi, I'm Deepesh. I help clients transform their raw footage
                into professional and engaging videos for social media
                and personal memories.
            </p>
        </div>

        <div class="box service-list">
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
