# redactbot
A [maubot](https://github.com/maubot/maubot) that responds to files being posted and redacts/warns all but a set of whitelisted mime types.

## Configuration
* The [base config](base-config.yaml) contains all requird configuration.

## Config format

The config file contains a list of rooms we are supposed to supervise, and a
list of whitelisted MIME types that are allowed. All other files being posted
in monitored rooms will be redacted immediately.

The bot will not automatically join rooms, and it needs moderator permission
in the rooms it is supposed to supervise.
