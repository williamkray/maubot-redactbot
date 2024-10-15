# redactbot
A [maubot](https://github.com/maubot/maubot) that responds to files being posted and redacts/warns all but a set of whitelisted mime types.

i have forked this work from Sebastian Spaeth, original repository can be found here: https://gitlab.com/sspaeth/redactbot.
This repo is no longer being maintained, as this functionality has mostly been re-implemented in my communitybot plugin.
Please use that instead, and submit new features as required.

[Communitybot](https://github.com/williamkray/maubot-communitybot)

## Configuration
* The [base config](base-config.yaml) contains all requird configuration.

## Config format

The config file contains a list of rooms we are supposed to supervise, and a
list of whitelisted MIME types that are allowed. All other files being posted
in monitored rooms will be redacted immediately.

The bot will need room permissions to enable it to redact messages, typically
this is moderator (PL50) and higher.
