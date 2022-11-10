import json
import ast
from flask import Flask, render_template
from typing import Dict
from app.data_analysis.gsheet_api import get_hp_claims_from_api_json
from pathlib import Path
app = Flask(__name__,
            template_folder=str(Path(Path(__file__).parent,'templates'))
            )

broken_hinge_api_json: Dict = get_hp_claims_from_api_json()
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


@app.route("/")
def home_view():
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


@app.route("/hp_issue_<issue_type>")
def hp_issue(issue_type):
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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001,
            debug=True)
