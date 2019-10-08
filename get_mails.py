from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import email
import base64
from apiclient import errors

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():


    def getMimeMessage(service, user_id, msg_id):
        try:
            message = service.users().messages().get(userId=user_id, id=msg_id, format='raw').execute()
            msg_bytes = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
            mime_msg = email.message_from_bytes(msg_bytes)
            messageMainType = mime_msg.get_content_maintype()
            if messageMainType == 'multipart':
                for part in mime_msg.get_payload():
                    if part.get_content_maintype() == 'text':
                        return part.get_payload()
                return ""
            elif messageMainType == 'text':
                return mime_msg.get_payload()
        except errors.HttpError as error:
            print('An error occurred: %s' % error)

    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)


    service = build('gmail', 'v1', credentials=creds)

    msg_list_params = {
        'userId': 'me'
    }
    # Call the Gmail API
    results = service.users().messages()
    messages_request = results.list(**msg_list_params)
    with open('mail.txt', 'w') as f:
        while messages_request is not None:
            gmail_msg_list = messages_request.execute()
            for gmail_msg in gmail_msg_list['messages']:
                f.write(getMimeMessage(service, 'me', gmail_msg['id']))





if __name__ == '__main__':
    main()