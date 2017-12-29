# Allow to setup a test environment. It's dirty and I don't like it, but
#  it works.
# Used to avoid error like too many requests for Telegram webhook check etc.
# Executed before tests in this particular module,
from yellowbot.globalbag import GlobalBag
GlobalBag.TEST_ENVIRONMENT = True

