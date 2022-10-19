from flask import Flask, render_template
from pathlib import Path

app = Flask(__name__,
            template_folder=str(Path(Path(__file__).parent,'templates'))
            )


@app.route("/")
def home_view():
    page_title = "HP Forums"
    return render_template('index.html', page_vars={'title': page_title})


if __name__ == '__main__':

    app.run(host="0.0.0.0", port=5001,
            debug=True)
