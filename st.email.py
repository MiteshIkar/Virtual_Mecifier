import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders


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

        msg.attach(MIMEText(message, 'plain'))

        if attachment_path is not None:
            attachment = MIMEApplication(attachment_path.read(), _subtype='pdf')
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


# Define the Streamlit app
def main():
    st.set_page_config(page_title='Email Autometa Solutions Pvt Ltd', page_icon=':email:')
    st.title('Email Autometa Solutions Pvt Ltd')

    # Define a form to get the email subject and message
    with st.container():
        st.subheader('Email Content')
        subject = st.text_input('Subject')
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
