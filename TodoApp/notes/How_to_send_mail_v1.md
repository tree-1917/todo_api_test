# How to Send Mail Using Fastapi

## Step 1: Set Up Your FastAPI Project

1. **Initialize a FastAPI Project**: Set up a new FastAPI project if you haven't already. You can use `pip` to install FastAPI and create a basic project structure.

   ```bash
   pip install fastapi uvicorn
   ```

2. **Create a New FastAPI App**: Create a directory for your project and a new FastAPI application within it.

   ```bash
   mkdir fastapi_email_app
   cd fastapi_email_app
   touch main.py
   ```

3. **Install Required Libraries**: Install necessary libraries like `smtplib` and `pydantic` for email handling and data validation.

   ```bash
   pip install smtplib pydantic
   ```

## Step 2: Configure Gmail SMTP

4. **Set Up SMTP Configuration**: Configure Gmail SMTP settings in your FastAPI application.

   ```python
   import smtplib

   # Gmail SMTP server configuration
   gmail_server = 'smtp.gmail.com'
   gmail_port = 587  # TLS port for Gmail

   # Your Gmail credentials
   gmail_user = 'your_email@gmail.com'
   gmail_password = 'your_password'

   # Create an SMTP session
   smtp_server = smtplib.SMTP(gmail_server, gmail_port)
   smtp_server.starttls()  # Enable TLS encryption

   # Login to Gmail
   smtp_server.login(gmail_user, gmail_password)
   ```

## Step 3: Define FastAPI Endpoint

5. **Define Email Schema**: Create a Pydantic model to validate email data.

   ```python
   from pydantic import BaseModel

   class EmailSchema(BaseModel):
       recipient: str
       subject: str
       message: str
   ```

6. **Create FastAPI Endpoint**: Define a POST endpoint to send emails using FastAPI.

   ```python
   from fastapi import FastAPI, HTTPException
   from email.mime.multipart import MIMEMultipart
   from email.mime.text import MIMEText

   app = FastAPI()

   @app.post("/send_email/")
   async def send_email(email: EmailSchema):
       try:
           # Create a MIMEText object with email content
           msg = MIMEMultipart()
           msg['From'] = gmail_user
           msg['To'] = email.recipient
           msg['Subject'] = email.subject
           msg.attach(MIMEText(email.message, 'plain'))

           # Send email
           smtp_server.send_message(msg)
           return {"message": "Email sent successfully"}
       except Exception as e:
           raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")
   ```

## Step 4: Test Your Endpoint

7. **Test the Endpoint**: Start the FastAPI development server and test your email sending endpoint using a tool like `curl` or Postman.

   ```bash
   uvicorn main:app --reload
   ```

8. **Send Test Email**: Make a POST request to `/send_email/` with JSON data containing recipient email, subject, and message.

   ```http
   POST http://localhost:8000/send_email/
   Content-Type: application/json

   {
     "recipient": "recipient_email@example.com",
     "subject": "Test Email from FastAPI",
     "message": "Hello, this is a test email sent from FastAPI!"
   }
   ```

## Step 5: Security and Considerations

9. **Secure Gmail Credentials**: Avoid storing sensitive credentials directly in your code. Use environment variables or a secure vault.

10. **Handle Errors**: Implement error handling to manage exceptions that may occur during the email sending process (`smtplib` may raise exceptions for network errors, authentication failures, etc.).

11. **Authentication**: Ensure that Gmail allows less secure app access or consider using OAuth2 for more secure authentication.

## Summary

This tutorial outlines the basic steps to integrate email sending functionality into your FastAPI application using Gmail SMTP. Adjust the code according to your specific requirements and security considerations.
