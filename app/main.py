from flask import Flask, render_template

app = Flask(__name__,
            # template_folder=str(Path(Path(__file__).parent,'templates'))
            )


@app.route("/")
def home_view():
    page_title: str = "HP Forums"
    h2_text: str = """
                    This website aims at gathering information regarding 
                    defective HP laptops
        """
    carousel_id = "carouselHP"
    carousel_slides: list = [{'slide_name': 'broken_hinge', 'slide_position': "0", "slide_wait_time":1000},
                             {'slide_name': 'broken_hinge_screen', 'slide_position': "1", "slide_wait_time":1000},
                             {'slide_name': 'battery_issue', 'slide_position': "2", "slide_wait_time":1000},
                             ]

    return render_template('index.html', page_vars={'title': page_title,
                                                    'h2_text': h2_text,
                                                    'carousel_id': carousel_id,
                                                    'carousel_slides': carousel_slides
                                                    })


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001,
            debug=True)
