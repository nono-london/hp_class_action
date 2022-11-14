from datetime import datetime
from pathlib import Path
from typing import Dict

from flask import (Flask, render_template,
                   request, flash)

from app.data_analysis.gsheet_api import get_hp_claims_from_api_json
from app.visitor_information.contact_form import save_contact_message
from app.visitor_information.ip_address import get_customer_ip_address

app = Flask(__name__,
            template_folder=str(Path(Path(__file__).parent, 'templates'))
            )
app.secret_key = "dssdnbvjhu(ç*$@@@@####"

broken_hinge_api_json: Dict = get_hp_claims_from_api_json()
broken_hinge_api_json_last_update: datetime = datetime.utcnow()

home_carousel_slides: list = [{'slide_name': 'broken_hinge', 'slide_position': 0, "slide_wait_interval": 3000,
                               'slide_title': 'Broken Hinges', 'slide_h5': 'HP Forum Support',
                               'slide_p': 'Data gathered from HP users testimonies'
                               },
                              {'slide_name': 'broken_hinge_screen', 'slide_position': 1, "slide_wait_interval": 2000,
                               'slide_title': 'Broken Hinges And Screens', 'slide_h5': 'HP Forum Support',
                               'slide_p': 'Data gathered from HP users testimonies'
                               },
                              {'slide_name': 'battery_issue', 'slide_position': 2, "slide_wait_interval": 2000,
                               'slide_title': 'Batteries', 'slide_h5': 'HP Forum Support',
                               'slide_p': 'Data gathered from HP users testimonies'
                               },
                              ]


def refresh_dataset(force_update: bool = False):
    global broken_hinge_api_json
    global broken_hinge_api_json_last_update
    if (datetime.utcnow() - broken_hinge_api_json_last_update).days == 0 or not force_update:
        return

    broken_hinge_api_json = get_hp_claims_from_api_json()
    broken_hinge_api_json_last_update = datetime.utcnow()


# multiple issues home index
# @app.route("/")
def home_view():
    get_customer_ip_address()

    refresh_dataset()

    page_title: str = "HP Forums"
    h2_text: str = """
                    This website aims at gathering information regarding 
                    defective HP laptops
        """
    carousel_id = "carouselHP"

    return render_template('index.html', page_vars={'title': page_title,
                                                    'h2_text': h2_text,
                                                    'carousel_id': carousel_id,
                                                    'carousel_slides': home_carousel_slides
                                                    })


# image carousel home index
@app.route("/")
def home_view():
    get_customer_ip_address()

    refresh_dataset()

    page_title: str = "HP Hinge Broken"
    h2_text: str = """
                    Defective hinge laptops
        """
    carousel_id = "carouselHP"
    image_paths = ['images/broken_hinge/' + path.name for path in
                   Path(Path(__file__).parent, 'static', 'images', 'broken_hinge').glob('*.jpg')]
    print(f"Carousel image paths: {image_paths}")

    return render_template('index_images.html', page_vars={'title': page_title,
                                                           'h2_text': h2_text,
                                                           'carousel_id': carousel_id,
                                                           'image_paths': image_paths,
                                                           'slide_interval': 3000
                                                           })


@app.route("/hp_issue_<issue_type>")
def hp_issue(issue_type):
    get_customer_ip_address()

    page_title: str = str(issue_type.replace('_', ' ')).title()
    print("in hp issue router")
    h2_text = "HP issue: " + page_title

    print("BROKEN HING DETECTED")
    broken_hinge_api_json['data']['data'] = broken_hinge_api_json['data']['data'][:5000]
    json_dataset = broken_hinge_api_json['data']

    return render_template('hp_issue.html', page_vars={'title': page_title,
                                                       'h2_text': h2_text,
                                                       'json_dataset': json_dataset
                                                       })


@app.route("/contact_form", methods=['GET', 'POST'])
def contact_form():
    get_customer_ip_address()
    page_title = "Contact Form"

    if request.method == 'POST':
        save_contact_message(form_request=request.form)
        flash('Message sent successfully. Thank you!')

    return render_template('contact_form.html', page_vars={'title': page_title, })

@app.route("/rest_api", methods=['GET'])
def rest_api():
    get_customer_ip_address()
    page_title = "REST API"

    return render_template('rest_api.html', page_vars={'title': page_title, })


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001,
            debug=True)
