# Automate Tweets with Twitter API v2

This GitHub repository hosts a Python script that enables automated daily tweeting on X (formely Twitter). The script uses the Tweepy library to access the Twitter API v2. It allows users to schedule daily (or any desired frequency) tweets, which you compiled before.

## Usage

1. Clone or download the repository.
2. Add your Twitter API credentials and quotes to the script.
3. Change the csv file to add your content
4. Set up a scheduler (as below) to run the script at your desired time each day.

## Setting up the scheduler

### Linux server
1. Set `user_name` and change path variables at `systemctl_scripts/automate_tweet.service` accordingly.
2. Copy `automate_tweet.service` file and `automate_tweet.timer` file to `/etc/systemd/system/` 
    i.e run `$ sudo cp systemctl_scripts/automate_tweet.* /etc/systemd/system/`
3. Reload the systemctl daemon `sudo systemctl daemon-reload`
4. Start the timer `sudo systemctl enable automate_tweet.timer --now`

If you need to see the status, you can check it using `sudo systemctl status automate_tweet.timer` or `sudo systemctl status automate_tweet.service`
In case you need to stop the service, use `sudo systemctl stop automate_tweet.timer`
If you need to see the logs, use `journalctl -f -u automate_tweet.service --since '2024-02-14'`

### Using C-panel

1. Set up a `Python App` called `tweet_app` with `python3.8`. For URL also you can add `tweet_app`, or any other appropriate name. Remember the path of the new app (usually it looks like `/home/<user_name>/virtualenv/tweet_app/3.8/bin/python3`).
2. Add a `Cron Job` to run each day (or any other frequency you need) with `/home/<user_name>/virtualenv/tweet_app/3.8/bin/python3 /home/<user_name>/tweet_app/send_tweet.py` as the command (the first part is the path to the Python app we created above and the second part is the path to our python script). 
For example, the final command will look like this `0 0 * * * /home/<user_name>/virtualenv/tweet_app/3.8/bin/python3 /home/<user_name>/tweet_app/send_tweet.py`
To understand more about Cron Jobs, [read this](https://en.wikipedia.org/wiki/Cron).

## Live Demo

For a live demo, please check my profile [We Choose Joy](https://twitter.com/WeChoooseJoy).

Enjoy!