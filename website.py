import os
import sqlite3
import secrets
from uuid import uuid4
from html import escape

from flask import Flask, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(app.static_folder, "uploads")
DATABASE = "deep_media.db"
UPLOAD_PASSWORD = os.environ.get("UPLOAD_PASSWORD", "ChangeThisPassword123")

ALLOWED_EXTENSIONS = {"mp4", "webm", "mov", "jpg", "jpeg", "png", "webp"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def setup_database():
    connection = get_db()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS likes (
            media_name TEXT PRIMARY KEY,
            total_likes INTEGER DEFAULT 0
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            media_name TEXT NOT NULL,
            person_name TEXT NOT NULL,
            comment_text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


setup_database()


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def get_likes(media_name):
    connection = get_db()
    result = connection.execute(
        "SELECT total_likes FROM likes WHERE media_name = ?",
        (media_name,)
    ).fetchone()
    connection.close()

    return result["total_likes"] if result else 0


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
        safe_file = escape(file, quote=True)
        safe_url = escape(file_url, quote=True)
        likes = get_likes(file)

        if extension in {"mp4", "webm", "mov"}:
            preview = f"""
            <video muted loop playsinline preload="metadata">
                <source src="{safe_url}">
            </video>
            <div class="play-icon">▶</div>
            """
            media_type = "video"
        else:
            preview = f'<img src="{safe_url}" alt="{safe_file}">'
            media_type = "image"

        gallery += f"""
        <div class="project-card"
             data-name="{safe_file}"
             data-url="{safe_url}"
             data-type="{media_type}">
            <div class="media-preview">
                {preview}
            </div>

            <div class="project-info">
                <p>{safe_file}</p>
                <span>❤ {likes} likes &nbsp; 💬 Comments</span>
            </div>
        </div>
        """

    if not gallery:
        gallery = "<p class='empty'>No projects uploaded yet.</p>"

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
            }}

            .box {{
                width: min(1050px, 94%);
                margin: 25px auto;
                padding: 28px;
                border-radius: 22px;
                background: rgba(255, 255, 255, 0.12);
                border: 1px solid rgba(255, 255, 255, 0.25);
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.22);
                backdrop-filter: blur(12px);
                line-height: 1.65;
                animation: fadeInUp 0.8s ease-out both;
            }}

            .box h2 {{
                color: #7cecff;
                margin-top: 0;
            }}

            .service-list p {{
                margin: 9px 0;
            }}

            .gallery {{
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
                gap: 18px;
                margin-top: 22px;
            }}

            .project-card {{
                overflow: hidden;
                border-radius: 16px;
                text-align: left;
                cursor: pointer;
                background: rgba(0, 0, 0, 0.42);
                border: 1px solid rgba(124, 236, 255, 0.35);
                transition: 0.3s ease;
            }}

            .project-card:hover {{
                transform: translateY(-8px);
                border-color: #7cecff;
                box-shadow: 0 0 24px rgba(0, 191, 255, 0.45);
            }}

            .media-preview {{
                height: 205px;
                position: relative;
                overflow: hidden;
                background: #050505;
            }}

            .media-preview video,
            .media-preview img {{
                width: 100%;
                height: 100%;
                object-fit: cover;
                display: block;
            }}

            .play-icon {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: rgba(0, 0, 0, 0.65);
                border: 1px solid white;
                width: 48px;
                height: 48px;
                border-radius: 50%;
                text-align: center;
                padding: 12px 0 0 3px;
            }}

            .project-info {{
                padding: 12px;
            }}

            .project-info p {{
                margin: 0 0 5px;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }}

            .project-info span {{
                color: #bdefff;
                font-size: 13px;
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
                font-size: 16px;
                font-weight: bold;
                transition: 0.3s ease;
            }}

            .btn:hover {{
                transform: scale(1.06);
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

            .empty {{
                color: #d7f8ff;
            }}

            .modal {{
                display: none;
                position: fixed;
                inset: 0;
                z-index: 10;
                padding: 20px;
                background: rgba(0, 0, 0, 0.86);
                overflow-y: auto;
            }}

            .modal-content {{
                position: relative;
                width: min(900px, 96%);
                margin: 25px auto;
                padding: 20px;
                border-radius: 20px;
                background: #0c1233;
                border: 1px solid rgba(124, 236, 255, 0.45);
                text-align: left;
            }}

            .close {{
                position: absolute;
                top: 10px;
                right: 16px;
                color: white;
                font-size: 34px;
                cursor: pointer;
            }}

            #modalMedia video,
            #modalMedia img {{
                width: 100%;
                max-height: 560px;
                object-fit: contain;
                background: black;
                border-radius: 12px;
            }}

            .modal-actions {{
                display: flex;
                align-items: center;
                gap: 12px;
                margin: 18px 0;
            }}

            .like-btn {{
                border: 1px solid #ff7bbd;
                color: white;
                cursor: pointer;
                padding: 10px 17px;
                border-radius: 25px;
                font-size: 16px;
                background: rgba(255, 50, 150, 0.15);
            }}

            .like-btn:hover {{
                background: #d72c77;
            }}

            .comments {{
                margin-top: 15px;
                border-top: 1px solid rgba(255, 255, 255, 0.2);
                padding-top: 16px;
            }}

            .comment {{
                padding: 10px;
                margin: 8px 0;
                border-radius: 10px;
                background: rgba(255, 255, 255, 0.08);
            }}

            .comment strong {{
                color: #7cecff;
            }}

            .comment-form {{
                display: flex;
                gap: 8px;
                margin-top: 12px;
            }}

            .comment-form input {{
                margin: 0;
                flex: 1;
            }}

            @keyframes gradientMove {{
                0% {{ background-position: 0% 50%; }}
                50% {{ background-position: 100% 50%; }}
                100% {{ background-position: 0% 50%; }}
            }}

            @keyframes titleUp {{
                from {{ opacity: 0; transform: translateY(40px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}

            @keyframes fadeIn {{
                from {{ opacity: 0; }}
                to {{ opacity: 1; }}
            }}

            @keyframes fadeInUp {{
                from {{ opacity: 0; transform: translateY(25px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}

            @keyframes glow {{
                from {{ text-shadow: 0 0 10px #00bfff; }}
                to {{ text-shadow: 0 0 28px #8b5cf6; }}
            }}

            @media (max-width: 600px) {{
                body {{
                    padding: 38px 12px;
                }}

                .box {{
                    width: 100%;
                    padding: 20px 14px;
                }}

                .gallery {{
                    grid-template-columns: repeat(2, 1fr);
                    gap: 10px;
                }}

                .media-preview {{
                    height: 150px;
                }}

                .project-info {{
                    padding: 8px;
                }}

                .comment-form {{
                    flex-direction: column;
                }}
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
            <p>Click any project to watch it, like it or leave a comment.</p>

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

        <div class="modal" id="mediaModal">
            <div class="modal-content">
                <span class="close" id="closeModal">&times;</span>

                <div id="modalMedia"></div>

                <h2 id="modalTitle"></h2>

                <div class="modal-actions">
                    <button class="like-btn" id="likeButton">
                        ❤ Like (<span id="likeCount">0</span>)
                    </button>
                </div>

                <div class="comments">
                    <h3>Comments 💬</h3>

                    <div id="commentsList"></div>

                    <form class="comment-form" id="commentForm">
                        <input type="text" id="personName"
                               placeholder="Your name" maxlength="30" required>

                        <input type="text" id="commentText"
                               placeholder="Write a comment..." maxlength="300" required>

                        <button class="btn" type="submit">Post</button>
                    </form>
                </div>
            </div>
        </div>

        <script>
            let currentMedia = "";

            const modal = document.getElementById("mediaModal");
            const modalMedia = document.getElementById("modalMedia");
            const modalTitle = document.getElementById("modalTitle");
            const likeCount = document.getElementById("likeCount");
            const commentsList = document.getElementById("commentsList");

            document.querySelectorAll(".project-card").forEach(function(card) {{
                card.addEventListener("click", function() {{
                    currentMedia = card.dataset.name;
                    const url = card.dataset.url;
                    const type = card.dataset.type;

                    modalTitle.textContent = currentMedia;

                    if (type === "video") {{
                        modalMedia.innerHTML =
                            '<video controls autoplay playsinline>' +
                            '<source src="' + url + '">' +
                            '</video>';
                    }} else {{
                        modalMedia.innerHTML =
                            '<img src="' + url + '" alt="Project image">';
                    }}

                    modal.style.display = "block";
                    loadLikes();
                    loadComments();
                }});
            }});

            document.getElementById("closeModal").addEventListener("click", closeModal);

            modal.addEventListener("click", function(event) {{
                if (event.target === modal) {{
                    closeModal();
                }}
            }});

            function closeModal() {{
                modal.style.display = "none";
                modalMedia.innerHTML = "";
            }}

            function loadLikes() {{
                fetch("/likes?media=" + encodeURIComponent(currentMedia))
                    .then(response => response.json())
                    .then(data => {{
                        likeCount.textContent = data.likes;
                    }});
            }}

            document.getElementById("likeButton").addEventListener("click", function() {{
                fetch("/like", {{
                    method: "POST",
                    headers: {{
                        "Content-Type": "application/json"
                    }},
                    body: JSON.stringify({{ media: currentMedia }})
                }})
                .then(response => response.json())
                .then(data => {{
                    likeCount.textContent = data.likes;
                }});
            }});

            function loadComments() {{
                commentsList.innerHTML = "Loading comments...";

                fetch("/comments?media=" + encodeURIComponent(currentMedia))
                    .then(response => response.json())
                    .then(data => {{
                        commentsList.innerHTML = "";

                        if (data.comments.length === 0) {{
                            commentsList.innerHTML = "<p>No comments yet.</p>";
                            return;
                        }}

                        data.comments.forEach(function(comment) {{
                            const commentBox = document.createElement("div");
                            commentBox.className = "comment";

                            const name = document.createElement("strong");
                            name.textContent = comment.name + ": ";

                            const text = document.createElement("span");
                            text.textContent = comment.text;

                            commentBox.appendChild(name);
                            commentBox.appendChild(text);
                            commentsList.appendChild(commentBox);
                        }});
                    }});
            }}

            document.getElementById("commentForm").addEventListener("submit", function(event) {{
                event.preventDefault();

                const name = document.getElementById("personName").value;
                const text = document.getElementById("commentText").value;

                fetch("/comment", {{
                    method: "POST",
                    headers: {{
                        "Content-Type": "application/json"
                    }},
                    body: JSON.stringify({{
                        media: currentMedia,
                        name: name,
                        text: text
                    }})
                }})
                .then(response => response.json())
                .then(() => {{
                    document.getElementById("commentText").value = "";
                    loadComments();
                }});
            }});
        </script>
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


@app.route("/likes")
def likes():
    media_name = request.args.get("media", "")
    return jsonify({"likes": get_likes(media_name)})


@app.route("/like", methods=["POST"])
def like():
    data = request.get_json()
    media_name = data.get("media", "")

    if not media_name:
        return jsonify({"error": "Project not found"}), 400

    connection = get_db()

    connection.execute("""
        INSERT INTO likes (media_name, total_likes)
        VALUES (?, 1)
        ON CONFLICT(media_name)
        DO UPDATE SET total_likes = total_likes + 1
    """, (media_name,))

    connection.commit()

    result = connection.execute(
        "SELECT total_likes FROM likes WHERE media_name = ?",
        (media_name,)
    ).fetchone()

    connection.close()

    return jsonify({"likes": result["total_likes"]})


@app.route("/comments")
def comments():
    media_name = request.args.get("media", "")

    connection = get_db()

    rows = connection.execute("""
        SELECT person_name, comment_text
        FROM comments
        WHERE media_name = ?
        ORDER BY id DESC
    """, (media_name,)).fetchall()

    connection.close()

    return jsonify({
        "comments": [
            {
                "name": row["person_name"],
                "text": row["comment_text"]
            }
            for row in rows
        ]
    })


@app.route("/comment", methods=["POST"])
def comment():
    data = request.get_json()

    media_name = data.get("media", "").strip()
    person_name = data.get("name", "").strip()
    comment_text = data.get("text", "").strip()

    if not media_name or not person_name or not comment_text:
        return jsonify({"error": "Missing comment details"}), 400

    if len(person_name) > 30 or len(comment_text) > 300:
        return jsonify({"error": "Comment is too long"}), 400

    connection = get_db()

    connection.execute("""
        INSERT INTO comments (media_name, person_name, comment_text)
        VALUES (?, ?, ?)
    """, (media_name, person_name, comment_text))

    connection.commit()
    connection.close()

    return jsonify({"success": True})


@app.errorhandler(413)
def file_too_large(error):
    return redirect(url_for(
        "home",
        error="File is too large. Maximum upload size is 100 MB."
    ))


if __name__ == "__main__":
    app.run()
