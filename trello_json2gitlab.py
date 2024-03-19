#!/usr/bin/env python3
import json
import logging
import os
from pathlib import Path
from urllib.parse import unquote

import click
from dotenv import load_dotenv
import gitlab
from tqdm.autonotebook import tqdm

load_dotenv()
logging.basicConfig(level=logging.DEBUG, force=True)  # see all requests

class GitlabImport:

    def get_member(self, id):
        for member in trello["members"]:
            if member["id"] == id:
                return member

    def get_list(self, list_id):
        for label in trello["lists"]:
            if label["id"] == list_id:
                return label

    def get_checklists(self, card_id):
        """ migrate to-do lists"""
        res = []
        for checklist in trello["checklists"]:
            if checklist["idCard"] == card_id:
                items = ["* [" + ("x" if item["state"] == "complete" else " ") + "] " + item["name"]
                         for item in checklist["checkItems"]]
                res.append(f"**{checklist['name']}**\n\n" + '\n'.join(items))
        return "\n".join(res)

    def get_attachments(self, card):
        return "\n".join(f'[{unquote(item["fileName"])}]({item["url"]})' for item in card["attachments"])

    def migrate_labels(self):
        gl_labels = set(x.name for x in project.labels.list())

        for label_ in trello["lists"]:
            label = label_["name"]
            if label not in gl_labels:
                project.labels.create({"name": label, "color": "blue"})

    def migrate_issues(self):
        issues = project.issues.list()
        titles = set(x.title for x in issues)
        for card in tqdm(trello["cards"]):
            if card["name"] not in titles:
                issue = project.issues.create({"title": card["name"],
                                               "description": "\n\n".join((self.get_attachments(card), card["desc"], self.get_checklists(card["id"]))),
                                               "labels": self.get_list(card["idList"])["name"]
                                               })

                if card["closed"]:
                    issue.state_event = 'close'

                # migrate discussion
                for action in trello["actions"]:
                    if action["type"] == "commentCard" and action["data"]["card"]["id"] == card["id"]:
                        issue.discussions.create({
                            "body": f'{self.get_member(action["idMemberCreator"])["username"]}: {action["data"]["text"]}',
                            "created_at": action["date"]
                        })


@click.command()
@click.argument('TRELLO_JSON_PATH')
@click.argument('GITLAB_PROJECT_ID', type=int, default=os.environ.get("GITLAB_PROJECT_ID"))
@click.argument('GITLAB_URL', default=os.environ.get("GITLAB_URL") or "https://gitlab.com")
def main(trello_json_path, gitlab_project_id, gitlab_url):
    global trello, project

    trello = json.loads(Path(trello_json_path).read_text())
    "Trello model"

    token = os.environ["GITLAB_TOKEN"]
    if not token:
        print("Missing token. Use GITLAB_TOKEN=... environmental value or use the .env file.")

    gl = gitlab.Gitlab(gitlab_url, private_token=token)
    project = gl.projects.get(gitlab_project_id)


    gi = GitlabImport()
    gi.migrate_labels()
    gi.migrate_issues()


if __name__ == "__main__":
    main()
