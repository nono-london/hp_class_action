from datetime import datetime, timezone
from pathlib import Path
from random import randint
from time import sleep
from typing import Union
from urllib.parse import urljoin

import pandas as pd
import requests
from lxml.html import fromstring, Element
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup as bs
from hp_class_action.app_config import get_project_download_path
from hp_class_action.hinge_issue.hp_hinge_stats import upload_data

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


