import os
import secrets
from uuid import uuid4
from html import escape

from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(app.static_folder, "uploads")
UPLOAD_PASSWORD = os.environ.get("UPLOAD_PASSWORD", "ChangeThisPassword123")

ALLOWED_EXTENSIONS = {"mp4", "webm", "mov", "jpg", "jpeg", "png", "webp"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@app.route("/")
def home():
    message = escape(request.args.get("message", ""))
    error = escape(request.args.get("error", ""))

    files = sorted(
        os.listdir(UPLOAD_FOLDER),
        key=lambda file: os.path.getmtime(os.path.join(UPLOAD_FOLDER, file)),
        reverse=True
    )

    gallery = ""

    for file in files:
        extension = file.rsplit(".", 1)[-1].lower()
        file_url = url_for("static", filename=f"uploads/{file}")
        file_name = escape(file)

        if extension in {"mp4", "webm", "mov"}:
            gallery += f"""
            <div class="project-card">
                <video controls preload="metadata">
                    <source src="{file_url}">
                    Your browser does not support video.
                </video>
                <p>{file_name}</p>
            </div>
            """
        else:
            gallery += f"""
            <div class="project-card">
                <img src="{file_url}" alt="{file_name}">
                <p>{file_name}</p>
            </div>
            """

    if not gallery:
        gallery = "<p class='empty'>No samples uploaded yet.</p>"

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Deep Media Group</title>

        <style>
            * {{
                box-sizing: border-box;
            }}

            body {{
                margin: 0;
                min-height: 100vh;
                padding: 55px 20px;
                color: white;
                font-family: Arial, sans-serif;
                text-align: center;
                background: linear-gradient(-45deg, #050b2c, #102b6a, #5a1674, #007b9e);
                background-size: 400% 400%;
                animation: gradientMove 12s ease infinite;
            }}

            .hero-title {{
                color: white;
                font-size: clamp(38px, 7vw, 68px);
                margin: 0;
                animation: titleUp 1s ease-out both, glow 2s ease-in-out infinite alternate;
            }}

            .hero-subtitle {{
                color: #a8eaff;
                font-size: clamp(20px, 3vw, 28px);
                margin: 18px 0;
                animation: fadeIn 1.5s ease-out 0.4s both;
            }}

            .intro {{
                max-width: 700px;
                margin: 20px auto 35px;
                line-height: 1.7;
                color: #e8f8ff;
                animation: fadeIn 1.5s ease-out 0.8s both;
            }}

            .box {{
                width: min(900px, 92%);
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
            }}

            .box:hover {{
                transform: translateY(-7px);
                background: rgba(255, 255, 255, 0.18);
            }}

            .box h2 {{
                color: #7cecff;
                margin-top: 0;
            }}

            .service-list p {{
                margin: 9px 0;
            }}

            input {{
                width: min(420px, 100%);
                padding: 13px;
                margin: 8px 0;
                border-radius: 10px;
                border: 1px solid #7cecff;
                font-size: 15px;
            }}

            .btn {{
                display: inline-block;
                border: none;
                cursor: pointer;
                background: linear-gradient(90deg, #00bfff, #8b5cf6);
                color: white;
                padding: 14px 24px;
                border-radius: 30px;
                font-size: 17px;
                font-weight: bold;
                transition: 0.3s ease;
            }}

            .btn:hover {{
                transform: scale(1.08);
                box-shadow: 0 0 22px #00bfff;
            }}

            a {{
                text-decoration: none;
            }}

            .success {{
                color: #8dffb0;
                font-weight: bold;
            }}

            .error {{
                color: #ffb0b0;
                font-weight: bold;
            }}

            .gallery {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
                gap: 18px;
                margin-top: 20px;
            }}

            .project-card {{
                overflow: hidden;
                border-radius: 14px;
                background: rgba(0, 0, 0, 0.35);
                border: 1px solid rgba(124, 236, 255, 0.35);
            }}

            .project-card video,
            .project-card img {{
                width: 100%;
                height: 190px;
                display: block;
                object-fit: cover;
                background: #000;
            }}

            .project-card p {{
                padding: 10px;
                margin: 0;
                overflow-wrap: anywhere;
            }}

            .empty {{
                color: #d7f8ff;
            }}

            @keyframes gradientMove {{
                0% {{ background-position: 0% 50%; }}
                50% {{ background-position: 100% 50%; }}
                100% {{ background-position: 0% 50%; }}
            }}

            @keyframes titleUp {{
                from {{
                    opacity: 0;
                    transform: translateY(40px);
                }}
                to {{
                    opacity: 1;
                    transform: translateY(0);
                }}
            }}

            @keyframes fadeIn {{
                from {{ opacity: 0; }}
                to {{ opacity: 1; }}
            }}

            @keyframes fadeInUp {{
                from {{
                    opacity: 0;
                    transform: translateY(25px);
                }}
                to {{
                    opacity: 1;
                    transform: translateY(0);
                }}
            }}

            @keyframes glow {{
                from {{ text-shadow: 0 0 10px #00bfff; }}
                to {{ text-shadow: 0 0 28px #8b5cf6; }}
            }}
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
            <h2>My Projects & Samples 🎞️</h2>
            <div class="gallery">
                {gallery}
            </div>
        </div>

        <div class="box">
            <h2>Upload a New Project 🔒</h2>

            <p class="success">{message}</p>
            <p class="error">{error}</p>

            <form action="/upload" method="POST" enctype="multipart/form-data">
                <input type="file" name="project_file"
                       accept=".mp4,.webm,.mov,.jpg,.jpeg,.png,.webp" required>
                <br>

                <input type="password" name="password"
                       placeholder="Upload password" required>
                <br><br>

                <button class="btn" type="submit">Upload Project</button>
            </form>
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


@app.route("/upload", methods=["POST"])
def upload():
    entered_password = request.form.get("password", "")

    if not secrets.compare_digest(entered_password, UPLOAD_PASSWORD):
        return redirect(url_for("home", error="Wrong upload password."))

    file = request.files.get("project_file")

    if not file or not file.filename:
        return redirect(url_for("home", error="Please select a file."))

    if not allowed_file(file.filename):
        return redirect(url_for(
            "home",
            error="Only MP4, WEBM, MOV, JPG, PNG and WEBP files are allowed."
        ))

    safe_name = secure_filename(file.filename)
    unique_name = f"{uuid4().hex}_{safe_name}"

    file.save(os.path.join(app.config["UPLOAD_FOLDER"], unique_name))

    return redirect(url_for("home", message="Project uploaded successfully!"))


@app.errorhandler(413)
def file_too_large(error):
    return redirect(url_for(
        "home",
        error="File is too large. Maximum upload size is 100 MB."
    ))


if __name__ == "__main__":
    app.run()
