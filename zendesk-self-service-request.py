#!/usr/bin/python2.7
import base64
import json
import sys
import syslog
import Tkinter
import urllib
import urllib2

### You can test this script by running it from the Terminal as such:
### $ /path/to/JAMFSW_VPP_Request.py 1 2 'user.name' 'App Name'

### The user name is passed to the policy when the user logs in to 
JSSUser = str(sys.argv[3]) + "@yourdomain.com"

### The requested app's name is passed by the JSS/Self Service (Parameter 4 in the Policy)
VPPAppName = str(sys.argv[4])

### This is the form ID for the Zendesk ticket that will be created
VPPRequestFormID = 111111

### These are the custom field IDs required in the ticket forms
### The 'VPP Request' ticket form requires the manager's name,
### the manager's email address and their department.
CFManager = 22222222
CFManagerEmail = 33333333
CFDepartment = 44444444

### This is the ID of the group the tickets should be assigned to
### Example: Desktop Services
ZenGroupID = 55555555

### This is the information for the Zendesk environment (token authentication)
ZenURL = 'https://yourdomain.zendesk.com/api/v2'
ZenAgent = 'agent-account'
ZenToken = 'agent-account-token'

### The 'syslog' class allows this app to write log entries into system.log
### The 'logger-tag' is the prefix for these log entries
syslog.openlog('logger-tag')

def log(msg):
    '''Global logging function to write to system.log and output to STDOUT'''
    syslog.syslog(syslog.LOG_ALERT, "VPPRequestTicket: " + str(msg))
    print(str(msg))

### This is an optional base64 encoded GIF file that can be embedded
### within the script to be displayed within the GUI.
gifBase = '''
R0lGODlhgACAAPcAAO3t7RZP7h1T7x9T7x9X7x9V7zFk71mB8AxL7RhV7xxX7x1b7x1Z7x9b7x9Z7yhi8EV38brK8QJK7hJU7xpe8Bta7x1d7x9h8R9f7x9d79Lb7+Lm7wlT7xFc7xVc8Bti8R1h8R1l8R1j8R9j
8R9l8Sxw8n2m9RFj8RZi8Rdm8R1n8R1p8SBp8SRu8TV28kuI82qa9Apg8Bdq8Rpu8h1v8x1v8R1r8R1t8R9x8x9x8R9t8T2C84y198nc/ANh8RJs8R118x1x8x1z8x9z8yB186DE+Qlq8RZy8xZ28x138x158x96
8x938yV88zCC89bn/Q108xd78xp+8x198x1/8x178yaB9DeN9Vid9a/S+wN28w588xWB9B2D9R2F9R2B8x+E9CCH9SuK9UKY9uDu/RqE9B2H9R2F8x6J9SyR9XG1+Lzc/Ofr7+vt7wV+8wuD9BKG9RqK9R2P9R2N
9R2L9SSP9RKL9ReO9heS9h2T9x2R9x2V9x2T9R2R9S+a9kam91mw9wWM9RCR9haW9x2Z9x2b9x2X9x2V9SWZ9jej94vK+vH5/wqW9xic9xub9xuf9xud9x2e9yql9wKW9hGd9xWj+Rah9xmg9xul+Ruj9xuh9yGi
98fo/Qug+BCm+Reo+Ril+Rup+Run+R2q+R6n+R2p9yKt+eb1/gKm+Qmo+RWr+Rur+Rut+Syx+Ti5+ke++lnD+RSx+Ru1+Ruy+R61+WzP+wy0+hq3+xu6+xu5+SS5+iy9+qHi/AS6+xW7+xu++yLB+zrJ+w7A+xbA
+xvF+xvC+yvJ/LXr/Nf0/gTE/BXH/BvN/RvK/RvJ+xvH+0TV/cvz/w7L/RbR/RbN/RjP/RvR/RvP/SLR/TDU/W7h/Irm/QTT/g/S/RPV/RjU/RnZ/xnX/RvZ/xvX/xvX/RvT/RvV/R7X/Vfi/uDt8A/d/xnd/xnb
/xnZ/Rvb/xvZ/R3d/wXc/xTe/xnj/xnf/xnh/xnd/Rvf/xvh/xvj/yfg/irl/z7k/tPt8R3l//8AAP///yH5BAEAAP8ALAAAAACAAIAAAAj/AAEIHEiwoEF0CLVpO3dun0N9ECNKnEixosWLGDM63JctmzZeCNEZ
HEmyZEl+/I5lcyhPHr5++Fzii9myps2bOHPq3MkzJ82XNh1mO4bSpNGjANAd05cvXs+nUKNK1UmTZ7x854gi3TowpT548uiJHUu2rNmzaNOqXct2bNiwZvvtOyaSq0l0vL7O28u3r9+/gAMLHky4sOG+8eDNbWN3
JL9s8OIdnky5suXK9hJr49d4YJtj+9JdHi04Xrx06UyTXt3XHryhnQHwgieaNenE8ODN0/dwXm7atkmny3fMbhteqYNbPq3unLZj0JBBm46s+rGF85Irpyya81bk8dSJ/x9Pvrz58+jNS86K7Hq2hhsdnvN4rP25
eabT69+/P1694kcdExl/BBaozjrpvDMXMtrsk887p6EmIWrx2JPPPtpId4466axj4IfpJciJUfyEts6JKKao4oostphiahgyuI86+fVnGobQ8LLPNx266OOPLqaTDRsloXNON0AmqeQ628SjzSm85NMhiAcOx8sp
2rQDzzdLdtkiPNowNhIv23hpZorwbLMPNKecE9mZKH6jmIbblAmnmfCMeBA463zj55+ABirooIT6uY05Tx7zzjaFNjooo1dqk8823Thq6aXfdDOkQWSC4+mnoIYq6qikgtPNNuecgswz23AzTqmwjv86zqnYsJlN
q7Hmmus34Gyj50BsmOONrsSW2mqi4zAqTrG6vroNOLwsog05zzJrraeaEinQcduMU8634IYr7rjkkovqdOe0as63so7jjTfdxCvvu+O8+mk5oJrDzTbP1JeuN+UGLDC54HjjXVLYDKywwt1w86Q22GwjDTkUV0yO
N9JIs2+r1WDj8T4eV7MxNxl7Y3HF3mxzzZO8aLzwy+R2o422/FwD883fprwmMudww001QAOdscbSPOMcdNWdovTS1eWoTTbPEJ1x0EBzE8050bEKMM4wY1MXL95QLfbYZJddjcbX8MIgNtFIE3TGPz+jDZuL1G13
3aoio/Tddp//ct0zZ08tdDTXZIMML9iQbPbijFdzDWdsZON245RT7fM51T0TTTTULLPMNNFMUzgyfLcHNTbXpK566tg8k43apWdzDejTeE4N6M+w2bPilVcuDS8CAd475Rpjk6E21oTuOejLyH03g+dgM03t01dv
/fXTYHMO7HZr88wyyn/OueG8POPz8I1LMyQ/2Hju/vvwxy8/+Fcjw8kzyTCjPzObPxNt3QzSXOimsb8CGvCA01BG/zJkt/IlIxrL2F80sFEfbVQDgvPLYAap8Yw2aKNzGgyh+6wxjWRg40rZSIYymNGMFiajcHZj
kDJU2MIa2vCGOMThDKfBwLrJLhk1ZEYJ/7PhN2w80BoiFCE1sBE5ECYxg9V4YDagcT8g1rCE/QKgNoxBwxx68Ys3VEYvVka6RRwDf8qwYTKCAR1tlBCJT9zgY+KYwRJeAxrSEkYyiMFHYoixFqeo2zGM0Qth9PGQ
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
'''

class App:
    """Creates the GUI and defines button actions"""
    def __init__(self):
        self.submitted = False
        
        log("Retrieving user information from Zendesk.")
        self.user = FindUser(JSSUser)
        
    	self.root = Tkinter.Tk()
    	### Background color
        bgColor = "#EDEDED"
        self.root.configure(bg = bgColor)
        
        ### Creates the window and positions it in the center of the screen
        winX = 450
        winY = 330
        xPos = (int(self.root.winfo_screenwidth()) / 2) - (int(winX) / 2)
        yPos = (int(self.root.winfo_screenheight()) / 3) - (int(winY) / 2)
        self.root.geometry("%sx%s+%s+%s" % (winX, winY, xPos, yPos))
        self.root.resizable(False,False)
        self.root.call('wm', 'attributes', '.', '-topmost', True)
        self.root.title("VPP Request for %s" % VPPAppName)
        
        ### The following code will arrange the objects in the GUI
        ### These include labels, text entry boxes and buttons
        frame = Tkinter.Frame(self.root)
        frame.pack(side = Tkinter.LEFT, fill = Tkinter.X)
        gif = Tkinter.PhotoImage(data = gifBase)
        displayGif = Tkinter.Label(frame, image = gif, borderwidth = 15, bg = bgColor).pack(side = Tkinter.TOP)
        
        RequestorNameLabel = Tkinter.Label(self.root, text="Requestor's Name:", \
        justify = 'left', font=("Helvetica Neue Bold", 14), bg = bgColor).pack(padx = 10, pady = (10,0))
        RequestorNameDisplay = Tkinter.Label(self.root, text="%s" % self.user.name, \
        justify = 'left', width = 30, font=("Helvetica Neue", 14), bg = bgColor, borderwidth = 1, relief = 'sunken').pack(padx = 10)
        
        RequestorEmailLabel = Tkinter.Label(self.root, text="Requestor's Email:", \
        justify = 'left', font=("Helvetica Neue Bold", 14), bg = bgColor).pack(padx = 10)
        RequestorNameDisplay = Tkinter.Label(self.root, text="%s" % self.user.email, \
        justify = 'left', width = 30, font=("Helvetica Neue", 14), bg = bgColor, borderwidth = 1, relief = 'sunken').pack(padx = 10)
        
        ### The options for the 'Department' drop-down list match the available options in Zendesk
        DeptLabel = Tkinter.Label(self.root, text = "Department:", \
        justify = 'left', width = 30, font=("Helvetica Neue Bold", 14), bg = bgColor).pack(padx = 10)
        self.deptchoices = {'Culture': 'culture', 'Development': 'development', 'Education Services': 'education_services',
        'Finance': 'finance', 'Information Technology': 'information_technology', 'Marketing': 'marketing', 'Online Services': 'online_services',
        'Professional Services': 'professional_services', 'Sales': 'sales', 'Support': 'support'}
        self.dept = Tkinter.StringVar(self.root)
        DeptSelection = Tkinter.OptionMenu(self.root, self.dept, *self.deptchoices)
        DeptSelection.config(bg = bgColor, width = 30)
        DeptSelection.pack(padx = 10)
        
        ApproverName = Tkinter.Label(self.root, text="Approving Manager's Name:", \
        justify = 'left', font=("Helvetica Neue Bold", 14), bg = bgColor).pack(padx = 10)
        self.approvername = Tkinter.StringVar(self.root)
        ApproverNameInput = Tkinter.Entry(self.root, textvariable = self.approvername, \
        justify = 'left', width = 30, font=("Helvetica Neue", 14), highlightbackground = bgColor).pack(padx = 10)
        
        ApproverEmail = Tkinter.Label(self.root, text="Approving Manager's Email:", \
        justify = 'left', font=("Helvetica Neue Bold", 14), bg = bgColor).pack(padx = 10)
        self.approveremail = Tkinter.StringVar(self.root)
        ApproverEmailInput = Tkinter.Entry(self.root, textvariable = self.approveremail, \
        justify = 'left', width = 30, font=("Helvetica Neue", 14), highlightbackground = bgColor).pack(padx = 10)
        
        ### This 'feedback' label is initially blank but can be updated by actions below to display
        ### a message the user in case they omitted information or if there was an error
        self.feedback = Tkinter.StringVar()
        self.feedback.set("")
        self.feedbackcolor = Tkinter.StringVar()
        self.feedbackcolor.set('black')
        self.feedbackmessage = Tkinter.Label(self.root, textvariable = self.feedback, wraplength = 200, font = ("Helvetica Neue", 12, "italic"), fg = self.feedbackcolor.get(), bg = bgColor)
        self.feedbackmessage.pack(padx = 10)
        
        self.buttonSubmit = Tkinter.Button(self.root, text = "Submit Request", highlightbackground = bgColor, command = self.SubmitReq)
        self.buttonSubmit.place(relx = 1, rely = 1, x = -5, y = -5, anchor = "se")
        
        buttonExit =  Tkinter.Button(self.root, text = "Exit", highlightbackground = bgColor, command = self.Exit)
        buttonExit.place(relx = 1, rely = 1, x = -130, y = -5, anchor = "se")
        
        menuBar = Tkinter.Menu(self.root)
        self.root.config(menu=menuBar)
        
        if not self.user.id:
            self.feedbackcolor.set('red')
            self.feedbackmessage.config(fg = self.feedbackcolor.get())
            self.feedback.set("Unable to communicate with Zendesk. Please check your connection.")
            log("Unable to communicate with Zendesk. Please check your connection.")
            self.buttonSubmit['state'] = 'disabled'
        
        self.root.mainloop()
        
    def SubmitReq(self):
        ### The user is required to fill out all fields
        ### If a field is left blank the submission is cancelled with a message displayed
        if not self.dept.get():
            self.feedbackcolor.set('red')
            self.feedbackmessage.config(fg = self.feedbackcolor.get())
            self.feedback.set("You need to select your department from the drop-down menu!")
            return
            
        if not self.approvername.get():
            self.feedbackcolor.set('red')
            self.feedbackmessage.configure(fg = self.feedbackcolor.get())
            self.feedback.set("You need to enter your approving manager's name!")
            return
            
        if not self.approveremail.get():
            self.feedbackcolor.set('red')
            self.feedbackmessage.configure(fg = self.feedbackcolor.get())
            self.feedback.set("You need to enter your approving manager's email address!")
            return
        
        ### The approving manager's email address must match the company domain
        if not self.approveremail.get().endswith("@yourdomain.com"):
            self.feedbackcolor.set('red')
            self.feedbackmessage.configure(fg = self.feedbackcolor.get())
            self.feedback.set("You need to enter a valid email address!")
            return
        
        ### This is the JSON to create the VPP Request ticket
        VPPRequest = {
            "ticket": {
            "requester": {"name": str(self.user.name), "email": str(self.user.email)},
            "submitter_id": self.user.id,
            "group_id": ZenGroupID,
            "ticket_form_id": VPPRequestFormID,
            "subject": "VPP Request: " + str(VPPAppName),
            "comment": {"public": "true", "body": \
            "Hello " + str(self.user.name) + ",\n\nYou have made a request for a redeemable VPP code for the app: " + str(VPPAppName) +\
            "\n\nYour approving manager has been copied on this request.\n\n" + str(self.approvername.get()) + ", please review their request and reply to this ticket."},
            "tags": self.user.tags + ["vpp_request"],
            "custom_fields": [{"id": CFManager, "value": str(self.approvername.get())}, {"id": CFManagerEmail, "value": str(self.approveremail.get())}, {"id": CFDepartment, "value": str(self.deptchoices[self.dept.get()])}],
            "type": "question",
            "priority": "normal",
            "status": "pending",
            "collaborators": [{ "name": str(self.approvername.get()), "email": str(self.approveremail.get())}]
            }
        }
        
        log("Creating the VPP Request ticket.")
        RequestTicket = CreateTicket(VPPRequest)
        
        ### This is the JSON for the Agent note added to the created ticket
        VPPRequestAgentNote = {
            "ticket": {
                "comment": {"public": "false", "body": "### This is a private note containing instructions for other agents.\n\
                ### The below message is generated for an agent to copy-and-paste into a public reply.\n\
                Hello " + str(self.user.name) + ",\n\nYou requested a VPP code for the app: " + str(VPPAppName) +\
                ".\n\nYour request was approved!  Please use the code provided below on your Mac to redeem your copy from the Mac App Store.  \
                Please respond to this ticket letting us know you've redeemed the code or if you encounter any issues doing so.\n\n\
                Thank you!\n\VPP Code: <<REDEMPTION CODE GOES HERE>>"}
            }
        }
        log("Adding Agent Note to the VPP Request ticket.")
        RequestTicket.update(VPPRequestAgentNote)
        
        self.feedbackcolor.set('blue')
        self.feedbackmessage.config(fg = self.feedbackcolor.get())
        self.feedback.set("Your request has been submitted. You will receive an email notification shortly.")
        self.buttonSubmit['state'] = 'disabled'
        self.submitted = True


    def Exit(self):
        ### The exit status is determined by whether or not a request was submitted
        self.root.destroy()
        if self.submitted:
            log("Exit 0: VPP Request submitted")
            sys.exit(0)
        else:
            log("Exit 1: VPP Request not submitted")
            sys.exit(1)


class FindUser:
    """Queries ZenDesk for the user's email address and parses data"""
    def __init__(self, email):
        request = urllib2.Request(str(ZenURL) + '/users/search.json?' + urllib.urlencode({'query': str(email)}))
        request.add_header('Authorization', 'Basic ' + base64.b64encode(str(ZenAgent) + ':' + str(ZenToken)))
        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError as e:
            print("API GET error: " + str(e.code))
            self.id = None
            self.name = None
            self.email = None
        except urllib2.URLError as e:
            print("API GET error: " + str(e.args))
            self.id = None
            self.name = None
            self.email = None
        else:
            print("API GET request successful: " + str(response.getcode()))
            data = json.load(response)
        
        try:
            self.id = data['users'][0]['id']
            self.name = data['users'][0]['name']
            self.tags = data['users'][0]['tags']
            self.email = email
            self.data = data
        except:
            self.id = None
            self.name = None
            self.email = None


class CreateTicket:
    """Generates a Zendesk ticket and provides the ability to add updates"""
    def __init__(self, d):
        request = urllib2.Request(str(ZenURL) + '/tickets.json')
        request.add_header('Authorization', 'Basic ' + base64.b64encode(str(ZenAgent) + ':' + str(ZenToken)))
        request.add_header('Content-Type', 'application/json')
        postdata = json.dumps(d)
        try:
            response = urllib2.urlopen(request, postdata)
        except urllib2.HTTPError, e:
            print("API POST error: " + str(e.code))
        except urllib2.URLError, e:
            print("API POST error: " + str(e.args))
        else:
            print("API POST request successful: " + str(response.getcode()))
            data = json.loads(response.read())
        self.id = data['ticket']['id']
        self.url = data['ticket']['url']
        self.data = data
    def update(self, u):
        request = urllib2.Request(str(self.url))
        request.add_header('Authorization', 'Basic ' + base64.b64encode(str(ZenAgent) + ':' + str(ZenToken)))
        request.add_header('Content-Type', 'application/json')
        request.get_method = lambda: 'PUT'
        putdata = json.dumps(u)
        try:
            response = urllib2.urlopen(request, putdata)
        except urllib2.HTTPError as e:
            print("API PUT error: " + str(e.code))
        except urllib2.URLError as e:
            print("API PUT error: " + str(e.args))
        else:
            print("API PUT request successful: " + str(response.getcode()))


if __name__ == '__main__':
    App()