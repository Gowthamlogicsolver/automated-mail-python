import tkinter as tk
from tkinter import filedialog
import csv
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def send_emails():
    smtp_server = 'smtp.kct.ac.in'
    smtp_port = 587
    sender_email = 'test@test.com' # Add your email
    sender_password = 'xyz' # Add your App password here
    csv_path = csv_entry.get()
    text_path = text_entry.get()
    image_path = image_entry.get()

    # Read emails from CSV
    emails_list = read_emails_from_csv(csv_path)

    # Establish connection to SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)

    # Send emails in batches of 99
    batch_size = 99
    for i in range(0, len(emails_list), batch_size):
        batch_emails = emails_list[i:i + batch_size]

        for receiver_email in batch_emails:
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = subject_entry.get()

            if not body_only_var.get():
                with open(text_path, "r") as file:
                    body = file.read()
                    message.attach(MIMEText(body, "plain"))

            if not image_only_var.get():
                with open(image_path, "rb") as attachment:
                    image = MIMEImage(attachment.read(), name="image.png")
                    message.attach(image)

            if not body_only_var.get() or not image_only_var.get():
                server.sendmail(sender_email, receiver_email, message.as_string())
                time.sleep(5)  # Adding a slight delay between emails

    server.quit()
    status_label.config(text="All emails sent successfully!")

def read_emails_from_csv(file_path):
    emails = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            x = emails.append(row[0])
    return emails

# ... (rest of the code remains unchanged)


def browse_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    csv_entry.delete(0, tk.END)
    csv_entry.insert(0, file_path)

def browse_text():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    text_entry.delete(0, tk.END)
    text_entry.insert(0, file_path)

def browse_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    image_entry.delete(0, tk.END)
    image_entry.insert(0, file_path)

# Create the main window
root = tk.Tk()
root.title("Email Sender")

# Create a frame with blue background
frame = tk.Frame(root, bg="#99ccff", padx=20, pady=20, borderwidth=2, relief="solid")
frame.place(relx=0.5, rely=0.5, anchor="center")

# Function to create entry with label
def create_entry(parent, label_text, browse_command):
    frame = tk.Frame(parent, bg="#99ccff")
    frame.pack(pady=5)
    label = tk.Label(frame, text=label_text, width=15, anchor='w', font=("Arial", 10), bg="#99ccff")
    label.pack(side='left', padx=(10, 5))
    entry = tk.Entry(frame, width=40, font=("Arial", 10))
    entry.pack(side='left', padx=(0, 10))
    if browse_command:
        browse_button = tk.Button(frame, text="Browse", command=browse_command, font=("Arial", 8))
        browse_button.pack(side='left')
    return entry

subject_entry = create_entry(frame, "Subject:", None)
csv_entry = create_entry(frame, "CSV File Path:", browse_csv)
text_entry = create_entry(frame, "Text File Path:", browse_text)
image_entry = create_entry(frame, "Image File Path:", browse_image)

body_only_var = tk.BooleanVar()
body_only_check = tk.Checkbutton(frame, text="Send Image Only", variable=body_only_var, font=("Arial", 10), bg="#99ccff")
body_only_check.pack()

image_only_var = tk.BooleanVar()
image_only_check = tk.Checkbutton(frame, text="Send Body Only", variable=image_only_var, font=("Arial", 10), bg="#99ccff")
image_only_check.pack()

send_button = tk.Button(frame, text="Send Emails", command=send_emails, font=("Arial", 10, "bold"), bg="#4CAF50", fg="white")
send_button.pack(pady=15)

status_label = tk.Label(frame, text="", font=("Arial", 10, "italic"), bg="#99ccff")
status_label.pack()

root.mainloop()
