import pyttsx3
import streamlit as st
import smtplib
import speech_recognition as sr

# Define a function to send an email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


def send_email(sender_email, sender_password, receiver_email, subject, message, attachment_path=None):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        if attachment_path is not None:
            attachment = MIMEApplication(attachment_path.read(), _subtype='pdf')
            attachment.add_header('Content-Disposition', 'attachment', filename=attachment_path.name)
            msg.attach(attachment)
            st.success("File uploaded successfully!")
        else:
            st.warning("No file uploaded.")

        # Define the message content here
        msg.attach(MIMEText(message, 'plain'))

        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        st.success("Email sent successfully!")

    except Exception as e:
        st.error(f"An error occurred while sending the email: {e}")

# Define a function to capture audio from the user's microphone
def record_audio():
    with sr.Microphone() as source:
        r = sr.Recognizer()
        r.adjust_for_ambient_noise(source)
        st.info('Speak now...')
        audio = r.listen(source)
        try:
            st.info('Transcribing...')
            message = r.recognize_google(audio)
            st.success('Transcription successful')
            return message
        except Exception as e:
            st.error('Transcription failed: {}'.format(e))
            return ''


# Define the Streamlit app
def main():
    st.set_page_config(page_title='Email Autometa Solutions Pvt Ltd', page_icon=':email:')
    st.title('Email Autometa Solutions')


    # Define a form to get the email subject
    with st.container():
        st.subheader('Enter subject || Record your audio for message to be send')

        subject = st.text_input('Subject')

    # Add a sidebar to choose the sender and receiver email addresses
    with st.sidebar.beta_container():
        st.subheader('Email Addresses')
        sender_email = st.text_input('Enter Sender email', type='default')
        sender_password = st.text_input('Sender password', type='password')
        receiver_email = st.text_input('Enter receiver email', type='default')

        attachment_path = st.file_uploader('Choose an attachment', type=None)

    # Initialize the message variable with an empty string
    message = ''



    # Add a button to start voice recognition for message input
    button_key = hash('my unique ')
    if st.button('Start Recording',key=button_key):
        listner = sr.Recognizer()
        engine = pyttsx3.init()

        def talk(text):
            engine.say(text)
            engine.runAndWait()
        talk('Tell text for email')
        if st.button('Start Recording'):
            listner = sr.Recognizer()
            engine = pyttsx3.init()

            def talk(text):
                engine.say(text)
                engine.runAndWait()

            talk('Tell text for email')

        r = sr.Recognizer()
        message = record_audio()
        if message:
            st.session_state.message = message
            st.text_area('Message', value=message, height=200)
        else:
            st.warning('No message recorded')



    button_key = hash('my unique button key')
    if st.button('Start Your Email Automation by clicking me for Help !!!',key=button_key):
        listner = sr.Recognizer()
        engine = pyttsx3.init()

        def talk(text):
            engine.say(text)
            engine.runAndWait()

        talk('Welcome to Email Autometa Solutions. Remeber to turn ON the less Secure setting of your account. Have a great Automation!!!')
        # Add a button to send the email
    button_key = hash('my unique button ')
    if st.button('Send Email', key=button_key):
        # Update the message variable with the text from the text area
        message = st.session_state.message
        send_email(sender_email, sender_password, receiver_email, subject, message, attachment_path)
        listner = sr.Recognizer()
        engine = pyttsx3.init()

        def talk(text):
            engine.say(text)
            engine.runAndWait()


        if st.success("Email sent successfully!"):
            talk('Your email has been sent successfully, thanks for using Email Autometa Solutions. Have a great day')
    st.markdown(
        """
        <footer style='text-align: Right; margin-top: 15px;'>
        By Mitesh Ikar
        </footer>
        """,
        unsafe_allow_html=True
    )



if __name__ == '__main__':
    main()
