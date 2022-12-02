import random
import yaml
import smtplib
import argparse
import pandas as pd
from email.message import EmailMessage

# Function to shuffle the names


def shuffle_names(names):
    # Shuffle the names
    random.shuffle(names)
    # Return the shuffled names
    return names

# Function to get pairs of names from the shuffled list


def get_pairs(names):
    # Create a list to store the pairs
    pairs = []
    # Loop through the list of names
    for i in range(0, len(names)):
        if i == len(names) - 1:
            # If the last name in the list, pair with the first name
            pairs.append((names[i], names[0]))
        else:
            # Pair the name with the next name in the list
            pairs.append((names[i], names[i+1]))
    # Return the list of pairs
    return pairs

# Function to check if the pairs in forward or reverse order are in the exclusion list


def contains_excluded_pairs(pairs, exclusion_list):
    # Loop through the list of pairs
    for pair in pairs:
        # Check if the pair is in the exclusion list
        if pair in exclusion_list:
            # If the pair is in the exclusion list, return False
            return True
        # Check if the pair is in the exclusion list in reverse order
        elif (pair[1], pair[0]) in exclusion_list:
            # If the pair is in the exclusion list in reverse order, return False
            return True
    # If the pair is not in the exclusion list, return True
    return False

# Function to read in yaml config file


def read_config(filpath):
    # Open the yaml file
    with open(filpath, 'r') as stream:
        # Load the yaml file
        config = yaml.full_load(stream)
    # Return the config
    return config

# Function to send email give a list of tuples and dataframe of email addresses


# def send_email(pairs, df, config):
#     # Create a list to store the emails
#     emails = []
#     # Loop through the list of pairs
#     for pair in pairs:
#         # Get the email addresses for the secret sock santa
#         email = df.query('Name == @pair[0]')['Email'].values[0]
#         # Create the email message
#         message = f"Hey {pair[0]}, you have {pair[1]} for secret sock santa!"
#         # Add the email to the list of emails
#         emails.append((email['Email'].values[0], message))
#     # Create the email server
#     server = smtplib.SMTP('smtp.gmail.com', 587)
#     # Start the email server
#     server.starttls()
#     # Get password from config text file
#     with open(config['password_file'], 'r') as stream:
#         password = stream.read()
#     # Get username from config
#     username = config['email']['username']
#     # Login to the email server
#     server.login(username, password)
#     # Loop through the list of emails
#     for email in emails:
#         # Recipient email address
#         to = email[0]
#         # Message
#         msg = email[1]
#         # Send the email
#         server.sendmail(config['email']['username'], to, msg)
#     # Close the email server
#     server.quit()

# Function to send test emails to grace
def send_emails_to_grace(pairs, df, config):
    # Get the email address and password for sender
    username = config['email']['username']
    with open(config['email']['password'], 'r') as stream:
        password = stream.read()

    # Make the email message for each pair
    for pair in pairs:
        # Get the email address for the recipient
        to = username
        # Create the email message content
        msg = EmailMessage()
        msg.set_content(
            f"Hey {pair[0]}, you have {pair[1]} for secret sock santa!")
        # Set the subject
        msg['Subject'] = 'Secret Sock Santa Assignment'
        msg['From'] = username
        msg['To'] = to
        # Create the email server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(username, password)
            smtp.send_message(msg)

    print("Emails sent!\n")


if __name__ == '__main__':

    # Read in a csv file as a pandas dataframe
    df = pd.read_csv('participants.csv')
    # Create a list of names from the dataframe
    names = df['Name'].tolist()
    # Read in the config file
    config = read_config('config.yml')
    # Create a list of excluded pairs
    exclusion_list = [tuple(l) for l in config['exclusion_list']]
    print(f"Excluding the following pairs: {exclusion_list}\n")
    # Make shuffled pairs until there is no pair in the exclusion list
    while True:
        # Shuffle the names
        names = shuffle_names(names)
        # Get the pairs
        pairs = get_pairs(names)
        # Check if the pairs are in the exclusion list
        if not contains_excluded_pairs(pairs, exclusion_list):
            # If the pairs are not in the exclusion list, break the loop
            break

    # Write the pairs to a text file
    with open('secret_pairs.txt', 'w') as f:
        for pair in pairs:
            f.write(f"{pair[0]} has {pair[1]}\n")

    # Send the emails
    send_emails_to_grace(pairs, df, config)

    print("Done! Secret Santa pairs have been emailed.\n Merry Christmas!")
