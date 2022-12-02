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

# Function to send test emails to grace


def send_emails(pairs, df, config, dry_run=False):

    # Get the email address and password for sender account
    username = config['email']['username']
    with open(config['email']['password'], 'r') as stream:
        password = stream.read()

    # Make the email message for each pair
    for pair in pairs:

        # Get the email address for the recipient (unless it's a dry run)
        if dry_run:
            to = username
        else:
            to = df.query('Name == @pair[0]')['Email'].values[0]

        # Get the sock size for the recipient
        sock_size = df.query('Name == @pair[1]')['Sock Size'].values[0]

        # Create the email message content
        msg = EmailMessage()
        msg.set_content(
            f"Hi {pair[0]},\n\n\tYour secret Bloom Lab sock swap assignment is {pair[1]}! Their sock size is {sock_size}.\n\nHappy Holidays!")
        # Set the subject
        msg['Subject'] = 'Secret Sock Swap Assignment'
        msg['From'] = username
        msg['To'] = to
        # Create the email server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(username, password)
            smtp.send_message(msg)

    print("Emails sent!\n")


if __name__ == '__main__':

    # Create the argument parser
    parser = argparse.ArgumentParser()
    # Add the argument for the participants file
    parser.add_argument('--participants', type=str,
                        default='participants.csv', help='Path to the participants file')
    # Add the argument for the config file
    parser.add_argument('--config', type=str, default='config.yaml',
                        help='Path to the config file')
    # Add the argument for dry run, true or false
    parser.add_argument('--dry_run', type=bool, default=False,
                        help='Dry run, send test emails to yourself')
    # Parse the arguments
    args = parser.parse_args()

    print("\nWelcome to the Bloom Lab sock swap!\n")

    # Read in a csv file as a pandas dataframe
    df = pd.read_csv(args.participants)
    # Create a list of names from the dataframe
    names = df['Name'].tolist()

    # Read in the config file
    config = read_config(args.config)
    # Create a list of excluded pairs
    exclusion_list = [tuple(l) for l in config['exclusion_list']]
    # Make sure that the names in the exclusion list are in the participants list
    for pair in exclusion_list:
        if pair[0] not in names or pair[1] not in names:
            raise ValueError(
                f"Names in exclusion list must be in participants list: {pair}")
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
    print("Wrote emails to secret_pairs.txt\n")

    # Get user input to send emails
    send = input("Send emails? (y/n): ")
    # Check if the user wants to send emails
    if send == 'y':
        print("Attempting to send emails...\n")
        # Check if dry run
        if args.dry_run:
            # Send emails to yourself as a test
            send_emails(pairs, df, config, dry_run=True)
        else:
            # Send the emails
            send_emails(pairs, df, config)
        print("Done! Secret Santa pairs have been emailed. Merry Christmas!")
    else:
        print("Not sending emails. Program Aborted.\n")
