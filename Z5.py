import imaplib

import pyttsx3
import streamlit as st
import smtplib
import speech_recognition as sr
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

engine = pyttsx3.init()
listener = sr.Recognizer()


def talk(text):
    engine.say(text)
    engine.runAndWait()


# Define a function to recognize speech
def recognize_speech():
    with sr.Microphone() as source:
        st.write('Speak now...')
        audio = listener.listen(source)
    try:
        st.write('Transcribing...')
        text = listener.recognize_google(audio)
        st.write(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        st.write('Sorry, I could not understand you')
        return ''
    except sr.RequestError as e:
        st.write(f"Could not request results from Google Speech Recognition service; {e}")
        return ''


# Define a function to send an email
def send_email(sender_email, sender_password, receiver_email, subject, message, attachment_path=None):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        if attachment_path is not None:
            attachment = MIMEBase('application', 'octet-stream')
            attachment.set_payload(attachment_path.read())
            encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition', 'attachment', filename=attachment_path.name)
            msg.attach(attachment)
            st.success("File uploaded successfully!")
        else:
            st.warning("No file uploaded.")

        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")

    except Exception as e:
        print(f"An error occurred while sending the email: {e}")
        if st.button('Display Inbox'):
            display_inbox(sender_email, sender_password)


# Define a function to display the inbox
def display_inbox(email, password):
    try:
        # Connect to the email server
        server = imaplib.IMAP4_SSL("imap.gmail.com")
        server.login(email, password)

        # Select the inbox and search for all the emails
        server.select("inbox")
        _, search_data = server.search(None, "ALL")

        # Iterate through the emails and display them
        for num in search_data[0].split():
            _, data = server.fetch(num, "(RFC822)")
            message = email.message_from_bytes(data[0][1])
            st.write(f"From: {message['From']}")
            st.write(f"Subject: {message['Subject']}")
            st.write(f"Date: {message['Date']}")

        # Close the server connection
        server.close()
        server.logout()

    except Exception as e:
        st.write(f"An error occurred while displaying the inbox: {e}")


# Add a button to display the inbox


# Define the Streamlit app
def main():
    st.set_page_config(page_title='Email Autometa Solutions Pvt Ltd', page_icon=':email:')
    st.title('Email Autometa Solutions Pvt Ltd')

    # Define a form to get the email subject and message
    with st.container():
        st.subheader('Email Content')
        subject = st.text_input('Subject')

        # Add a checkbox to toggle voice input
        use_voice_input = st.checkbox('Use voice input')

        # Add a text input or voice input based on checkbox value
        if use_voice_input:
            talk('Please say your message')
            message = recognize_speech()
        else:
            message = st.text_area('Message', height=200)

    # Add a sidebar to choose the sender and receiver email addresses
    with st.sidebar.beta_container():
        st.subheader('Email Addresses')
        sender_email = st.text_input('Enter Sender email', type='default')
        sender_password = st.text_input('Sender password', type='password')
        receiver_email = st.text_input('Enter receiver email', type='default')

        attachment_path = st.file_uploader('Choose an attachment', type=None)

        # Add a button to send the email
        if st.button('Send Email'):
            if attachment_path is not None:
                send_email(sender_email, sender_password, receiver_email, subject, message, attachment_path)
            else:
                send_email(sender_email, sender_password, receiver_email, subject, message, None)


if __name__ == '__main__':
    main()
