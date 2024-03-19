I needed to move my boards from Trello to Gitlab. It migrates the cards (issues), its columns (label), card checklists, card discussion and links to the attachments. While this solution may not compete with professional options, if you only have a couple of free boards, it might alleviate the pain.


# Installation

```python
pip install git+https://github.com/e3rd/trello_json2gitlab.git
```

# Requirements
* a JSON file, exported from a trello board
* Gitlab Access Token: https://gitlab.com/-/user_settings/personal_access_tokens

# Launch

Either define the token in an ".env" file or put it as an environmental variable:

```bash
GITLAB_TOKEN=... trello_json2gitlab.py TRELLO_JSON_PATH [GITLAB_PROJECT_ID] [GITLAB_URL]
GITLAB_TOKEN=... trello_json2gitlab.py downloaded.json  123456 https://gitlab.com
```