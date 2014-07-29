# Zendesk Tickets via Self Service
This script is an old example of a Self Service VPP request.  It displays a GUI for a user to enter their department and approving manager's information.  The user's name and email address is populated by a lookup against their existing user record in Zendesk using the Self Service username.

_**Example command line syntax:** /path/to/zendesk-self-service-request.py 1 2 username appname_

+ Parameter 3 is the username used to log into Self Service
+ Parameter 4 is the name of the app to display in the title bar and insert into the JSON for the POST

## About this script
The concept of this script can be improved and further automated (to the point of not requiring user interaction) by replacing the Zendesk user lookup with LDAP lookups if the capability in your environment exists.

The purpose of sharing this script is to provide an example of working with the Zendesk API using Python and JSON (performing a GET, parsing the response, and POST JSON data) as well as demonstrating how to use Python for multi-field user inputs with validation, which is a limitation of an Apple dialog prompt which can only have one text input field at a time.
