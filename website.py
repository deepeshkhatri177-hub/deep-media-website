from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <html>

    <head>
        <title>Deep Media Group</title>

        <style>
            body{
                background:#111;
                color:white;
                font-family:Arial;
                text-align:center;
                padding:40px;
            }

            h1{
                color:#00bfff;
                font-size:50px;
            }

            .box{
    background:rgba(0,0,0,0.7);
    padding:20px;
    border-radius:15px;
    margin:20px auto;
    width:70%;
}
#bgvideo{
    position:fixed;
    top:0;
    left:0;
    width:100%;
    height:100%;
    object-fit:cover;
    z-index:-1;
}
            .btn{
                background:#00bfff;
                color:white;
                padding:12px 20px;
                border:none;
                border-radius:10px;
                font-size:18px;
                cursor:pointer;
            }

            a{
                text-decoration:none;
            }
        </style>
    </head>

    <body>

        <h1>Deep Media Group</h1>

        <h2>Professional Video Editing Services 🎬</h2>

        <p>
            High Quality Reels, Wedding Edits,
            Anniversary Videos, Client Projects,
            Social Media Content
        </p>

        <div class="box">
            <h2>About Me</h2>

            <p>
                Hi, I'm Deepesh. I help clients transform
                their raw footage into professional and
                engaging videos for social media and personal memories.
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

            https://instagram.com/deepmediagroup
                <button class="btn">
                    Contact on Instagram
                



    





            </a>
 
        </div>

    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True)
   