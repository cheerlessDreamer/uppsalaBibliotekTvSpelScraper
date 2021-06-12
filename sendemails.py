#!/usr/bin/env python3

from string import Template
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from credentials import *
from scraping import li3


def get_contacts(filename):
    all_names = []
    all_emails = []
    with open(filename, mode="r", encoding="utf-8") as contacts_file:
        for row in contacts_file:
            all_names.append(row.split()[0])
            all_emails.append(row.split()[1])
    return all_names, all_emails


def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


def list_new_titles(new_titles_list):
    row = "- "
    full_list = ""
    for title in new_titles_list:
        new_row = row + title
        full_list = full_list + new_row + "\n"
    return full_list

sexy_list = list_new_titles(li3)

# Set up the SMTP server
s = smtplib.SMTP(host=SMTP_HOST, port=SMTP_PORT)
s.starttls()
s.login(MY_ADDRESS, PASSWORD)

names, emails = get_contacts('contacts.txt')  # read contacts

# CHOOSE APPROPRIATE MESSAGE TEMPLATE (I.E., NEW CONTENT OR NOT)
if not li3:
    message_template = read_template('nothing_new_message.txt')
else:
    message_template = read_template('message.txt')

# SEND AN EMAIL TO EACH CONTACT:
for name, email in zip(names, emails):
    msg = MIMEMultipart()  # create a message

    # add in the actual person name to the message template
    message = message_template.substitute(PERSON_NAME=name.title(), TITLE_LIST=sexy_list)

    # setup the parameters of the message
    msg['From'] = FROM_ADDRESS
    msg['To'] = email
    msg['Subject'] = "This is a TEST"

    # add in the message body
    msg.attach(MIMEText(message, 'plain'))

    # send the message via the server set up earlier.
    s.send_message(msg)

    del msg
