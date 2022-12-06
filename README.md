# Bloom Lab Sock Swap

This little python utility runs the Bloom Lab's annual Christmas Sock Swab BONANZA!

If the honor (and grave responsiblity) of hosting the Sock Swab is bestoed upon you, simply follow the instructions below and it'll all be okay.

## Instructions

To use this little application you need to do three things:

### 1. Set up the form

First, you need to get a list of the participants. This should be in the form of a `.csv` file with the columns `Name`, `Email`, and `Sock Size`. Make sure the names are exactly this. Once everyone fills out a form that makes this `.csv` file, download it into this directory.

### 2. Set up the email account

After the form is done, set up the email account to send the messages. You can use the gmail account `jbloom.lab.sock.swap@gmail.com`. Ask Will Hannon for the password to the account. He can transfer the account over to you. Otherwise, set up your own email accout.

If you make a new email, I reccomend that you use gmail with 2-factor identification enabled. This will make it possible to use 'less secure apps'(like this one) to send emails. To enable the script to send emails, add an `App Password` to your gmail account. Then, when google provides you a password, add it to a file called `secret_password.txt`. Finally, go into the config file and add the new email username.

### 3. Run the script

Finally, run the script to send the emails. To make sure the formatting and email notifications are correct, you should start with a 'dry run'. This will send all of the emails to youself so you can check that they're formatted correctly.

```
python sock_swap.py --participants participants.csv --config config.yml --dry_run
```

If everything looks good, just run the same command as above without the `dry_run` flag.

```
python sock_swap.py --participants participants.csv --config config.yml
```

The script will make a file called `secret_pairs.txt` that contain all the pairs. These are for your reference, but if you're participating, don't look at them! You can optionally share this with an independent party before sending the emails if you want to confirm that nothing went wrong.

### Ideas for Improving

If so inclined, I have a few ideas for making this better. First, I think the command-line-interface a little more festive. Maybe print some Christmas themed ASCII art? Also, the emails are pretty boring. Making a festive HTML template for the emails would really make this utility cooler.
