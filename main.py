import json
from flask import Flask, redirect, render_template, request

app = Flask(__name__)


def load_posts():
    with open('posts.json') as f:
        return json.load(f)


def save_posts(posts):
    with open('posts.json', 'w') as f:
        json.dump(posts, f, indent=4, ensure_ascii=False)


@app.route("/")
def index():
    posts = load_posts()
    return render_template("index.html", posts=posts)


@app.route('/add_post', methods=['POST'])
def add_post():
    post = {
        "title": request.form.get('title'),
        "content": request.form.get('content'),
        "author": request.form.get('author'),
        "likes": 0,
        "comments": []
    }
    posts = load_posts()
    posts.append(post)
    save_posts(posts)
    return redirect('/')


@app.route('/delete_post/<int:index>')
def delete_post(index):
    posts = load_posts()
    if 0 <= index < len(posts):
        del posts[index]
        save_posts(posts)
    return redirect('/')


@app.route('/add_comment/<int:index>', methods=['POST'])
def add_comment(index):
    posts = load_posts()
    if 0 <= index < len(posts):
        comment = request.form.get('comment')
        posts[index]["comments"].append(comment)
        save_posts(posts)
    return redirect('/')


@app.route('/like_post/<int:index>', methods=['POST'])
def like_post(index):
    posts = load_posts()
    if 0 <= index < len(posts):
        posts[index]["likes"] += 1
        save_posts(posts)
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
