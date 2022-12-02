# Bloom Lab Sock Swap

This little python utility runs the Bloom Lab's annual Christmas Sock Swab BONANZA!

If the honor (and grave responsiblity) of hosting the Sock Swab is bestoed upon you, simply follow the instructions below and it'll all be okay.

## Instructions

To use this little application you need to do three things:

### 1. Setting up the form

First, you need to get a list of the participants. This should be in the form of a `csv` file with the columns `Name`, `Email`, and `Sock Size`. Make sure the names are exactly this. Once everyone fills out the form, download it into this directory.

### Setting up the email

After the form, set up the email account to send the messages. You can use the gmail account `jbloom.lab.sock.swap@gmail.com`. Ask Will Hannon for the password to the account. He can transfer the account over to you. Otherwise, set up your own email accout.

If you make a new email, make sure that you enable 2-factor identification. This should make it possible to use less secure apps like this one. To enable the script to send emails, add an `App Password` to your account. Then, when google provides you a password, add it to a file called `secret_password.txt`. Finally, go into the config file and add the new email username.

### Running the script

Finally, run the script to send the emails. To make sure the formatting and email notifications are correct, you can start with a 'dry run'. This will send all of the emails to the email that you set up above so that you can check them out.

```
python sock_swap.py --participants participants.csv --config config.yml --dry_run True
```

If everything looks good, just run the same command as above with `dry_run` set to `False`.

```
python sock_swap.py --participants participants.csv --config config.yml --dry_run False
```
