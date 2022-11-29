import datetime
import os
import socket
import pandas as pd
from dateutil import parser

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# STEPS To RUN
# 1. Open terminal
# 2. install pandas (if not preinstalled) (Assuming python is preinstalled)
#    - "pip install pandas"
# 3. Run "py servery.py"
# 4. Open browser and go to "localhost:8080/"
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# DATASHEETS
# train.csv : STORE TRAIN TICKET DATA
# flight.csv : STORE FLIGHT TICKET DATA
# bus.csv : STORE BUS TICKET DATA
# transaction.csv : STORE BOOKING TRANSACTION DATA
# <USERNAME>.csv : STORE BOOKING HISTORY DATA
# auth.csv : STORE USER AUTHENTICATION DATA

LOCALHOST = "127.0.0.1"
PORT = 8080

# Booking id (unique id to each confirmed booking)
booking_id = 0


def generateBookingID():
    global booking_id
    # incrementing everytime a new booking os made
    booking_id += 1
    return booking_id


# file variables
# all the data will be fetched at the time of itenary generation and stored in these file variables
csv_files = []
csv_file_names = ["train.csv", "flight.csv", "bus.csv"]

# Final iternary list of places for a single user
it_list = []

# convert train.xlsx, bus.xlsx, flight.xlsx to csv
def convertXLSXToCSV():
    csv_files.append(pd.read_csv("train.csv"))
    csv_files.append(pd.read_csv("flight.csv"))
    csv_files.append(pd.read_csv("bus.csv"))


# create a class PlaceData with members name,date,mode,days,status,cost
# Each place of itenary is stored as this object
class PlaceData:
    def __init__(self, name, date, mode, days, status, cost):
        # name of place
        self.name = name
        # arrival date
        self.date = date
        # travel mode
        self.mode = mode
        # no. of staying days
        self.days = days
        # ticket confirmation status
        self.status = status
        # cost of one place to another
        self.cost = cost

    # setter for status and cost
    def setStatus(self, status):
        self.status = status

    # cost setter
    def setCost(self, cost):
        self.cost = cost


# check mode of transport for PlaceData object and return 0 for train, 1 for flight and 2 for bus
def getMode(placeData):
    if placeData.mode == "train":
        return 0
    elif placeData.mode == "flight":
        return 1
    else:
        return 2


# check available tickets and cost for train, flight and bus from the
def ItineraryResponseHTMLText(it_list, final_cost):
    p1 = it_list[0].name
    p2 = it_list[1].name
    p3 = it_list[2].name
    date1 = it_list[0].date
    date2 = it_list[1].date
    date3 = it_list[2].date
    mode1 = it_list[0].mode
    mode2 = it_list[1].mode
    mode3 = it_list[2].mode
    days1 = it_list[0].days
    days2 = it_list[1].days
    days3 = it_list[2].days
    cost1 = it_list[0].cost
    cost2 = it_list[1].cost
    cost3 = it_list[2].cost
    # if status is false then store "Not Available" in status
    status1 = (
        "Ticket Available"
        if it_list[0].status == True
        else "Tickets Not Available (Waiting)"
    )
    status2 = (
        "Ticket Available"
        if it_list[1].status == True
        else "Tickets Not Available (Waiting)"
    )
    status3 = (
        "Ticket Available"
        if it_list[2].status == True
        else "Tickets Not Available (Waiting)"
    )
    # final travel cost
    final_cost = final_cost
    # read iternary.html file and store it to html_text
    with open("./itenary.html", "r") as f:
        html_text = f.read()
    # replace the placeholders in html_text with the values
    html_text = html_text.replace("p1", p1.upper())
    html_text = html_text.replace("p2", p2.upper())
    html_text = html_text.replace("p3", p3.upper())
    html_text = html_text.replace("date1", str(date1))
    html_text = html_text.replace("date2", str(date2))
    html_text = html_text.replace("date3", str(date3))
    html_text = html_text.replace("mode1", mode1.upper())
    html_text = html_text.replace("mode2", mode2.upper())
    html_text = html_text.replace("mode3", "--")
    html_text = html_text.replace("days1", str(days1))
    html_text = html_text.replace("days2", str(days2))
    html_text = html_text.replace("days3", str(days3))
    html_text = html_text.replace("cost1", str(cost1))
    html_text = html_text.replace("cost2", str(cost2))
    html_text = html_text.replace("cost3", str(cost3))
    html_text = html_text.replace("status1", status1)
    html_text = html_text.replace("status2", status2)
    html_text = html_text.replace("status3", status3)
    html_text = html_text.replace("total", str(final_cost))
    return html_text


# Extract data from POST request and sort the places according to dates
def extractAndSortFormData(bodyDict):
    # extract data from bodyDict
    p1 = bodyDict["p1"]
    p2 = bodyDict["p2"]
    p3 = bodyDict["p3"]
    date1 = parser.parse(bodyDict["date1"])
    date2 = parser.parse(bodyDict["date2"])
    date3 = parser.parse(bodyDict["date3"])
    mode1 = bodyDict["mode1"]
    mode2 = bodyDict["mode2"]
    mode3 = bodyDict["mode3"]
    days1 = bodyDict["days1"]
    days2 = bodyDict["days2"]
    days3 = bodyDict["days3"]
    # Array of objects of class PlaceData
    placeData = []
    placeData.append(PlaceData(p1, date1, mode1, days1, False, 0))
    placeData.append(PlaceData(p2, date2, mode2, days2, False, 0))
    placeData.append(PlaceData(p3, date3, mode3, days3, False, 0))
    # Print the objects of PlaceData class
    print("Before sorting")
    for i in range(3):
        print(
            placeData[i].name,
            placeData[i].date,
            placeData[i].mode,
            placeData[i].days,
            placeData[i].status,
            placeData[i].cost,
        )
    # sort the objects of PlaceData class based on date
    placeData.sort(key=lambda x: x.date)
    # Print the objects of PlaceData class
    print("After sorting")
    for i in range(3):
        print(
            placeData[i].name,
            placeData[i].date,
            placeData[i].mode,
            placeData[i].days,
            placeData[i].status,
            placeData[i].cost,
        )
    return placeData


# Final cost of the itinerary
def generateItenerary(places):
    global it_list
    # resetting the list to empty for storing new itinerary
    it_list = []
    for i in range(places.__len__() - 1):
        # get travel mode
        mIndex = getMode(places[i])
        # fetch ticket database according to travel mode
        df = csv_files[mIndex]
        print("df:", df.head())
        # find ebtries with first place as p1
        df = df[df["p1"] == places[i].name]
        print("df:", df)
        # find entries with second place as p2
        print(places[i + 1].name)
        df = df[df["p2"] == places[i + 1].name]
        print(df.head())
        # check whether tickets are available or not
        print(df["tkt"].iloc[0])
        # if available set status to true
        if int(df["tkt"].values[0]) > 0:
            places[i].setStatus(True)
            places[i].setCost(int(df["cost"].values[0]))
            it_list.append(places[i])
        # else set status to false and update the cost
        else:
            places[i].setStatus(False)
            places[i].setCost(int(df["cost"].values[0]))
            it_list.append(places[i])
    it_list.append(places[places.__len__() - 1])
    # print it_list
    for i in range(it_list.__len__()):
        print(
            it_list[i].name,
            it_list[i].date,
            it_list[i].mode,
            it_list[i].days,
            it_list[i].status,
            it_list[i].cost,
        )
    return it_list


# Confirm itenary bookings and append it to file named as username.
def confirmBooking(username):
    print("Booking tickets")
    # print it_list
    for i in range(it_list.__len__()):
        print(
            it_list[i].name,
            it_list[i].date,
            it_list[i].mode,
            it_list[i].days,
            it_list[i].status,
            it_list[i].cost,
        )
    # edit csv files content based on it_list
    for i in range(it_list.__len__() - 1):
        # get travel mode
        mIndex = getMode(it_list[i])
        # fetch ticket database according to travel mode
        df = csv_files[mIndex]
        edf = csv_files[mIndex]
        # find entries with first place as p1
        df = df[df["p1"] == it_list[i].name]
        # find entries with second place as p2
        df = df[df["p2"] == it_list[i + 1].name]
        # update the ticket count
        tk_count = int(df["tkt"].values[0])
        edf.loc[
            (edf["p1"] == it_list[i].name) & (edf["p2"] == it_list[i + 1].name),
            "tkt",
        ] = (
            tk_count - 1
        )
        # write the updated content to csv file
        edf.to_csv(csv_file_names[mIndex], index=False)
    # append it_list to file named as username.txt
    # create a new file if it does not exist
    if not os.path.exists("./it_data/" + username + ".csv"):
        f = open("./it_data/" + username + ".csv", "w")
        f.write("id,place1,place2,place3,date1,date2,date3,cost")
        f.write("\n")
        f.close()
    # generate id for the itinerary
    generateBookingID()
    # append transaction data to file
    f = open("./payments/transactions.csv", "a")
    f.write(
        username
        + ","
        + str(booking_id)
        + ","
        + str(it_list[0].cost + it_list[1].cost + it_list[2].cost)
        + ","
        + str(datetime.datetime.now())
        + "\n"
    )
    # append it_list to file named as username.txt
    with open("./it_data/" + username + ".csv", "a") as f:
        f.write(
            str(booking_id)
            + ","
            + it_list[0].name
            + ","
            + it_list[1].name
            + ","
            + it_list[2].name
            + ","
            + str(it_list[0].date)
            + ","
            + str(it_list[1].date)
            + ","
            + str(it_list[2].date)
            + ","
            + str(it_list[0].cost + it_list[1].cost + it_list[2].cost)
            + "\n"
        )


# Initial request parser
class HTTPParser:
    def __init__(self, reqString):
        self.reqString = reqString
        self.reqType = ""

    # Parse the request string and return the request type
    def parser(self):
        reqSplits = self.reqString.split()
        self.reqType = reqSplits[0]


# GET Request Handler
class GETRequest:
    def __init__(self, fname):
        self.filename = fname

    def reqHandler(self, clientConnection):
        clientConnection.sendall(str.encode("HTTP/1.0 200 OK\n", "iso-8859-1"))
        clientConnection.sendall(str.encode("Content-Type: text/html\n", "iso-8859-1"))
        clientConnection.send(str.encode("\r\n"))
        # GET request for itinerary
        if self.filename == "/itinerary":
            # read content of index.html
            with open("index.html", "r") as f:
                clientConnection.send(bytes(f.read(), "UTF8"))
        # GET login page
        elif self.filename == "/":
            # read content of auth.html
            with open("auth.html", "r") as f:
                clientConnection.send(bytes(f.read(), "UTF8"))
        # GET register page
        elif self.filename == "/register":
            # read content of register.html
            with open("register.html", "r") as f:
                clientConnection.send(bytes(f.read(), "UTF8"))
        # GET bus tickets data
        elif self.filename == "/bus":
            df = pd.read_csv("bus.csv")
            clientConnection.send(bytes(df.to_html(), "UTF8"))
        # GET train tickets data
        elif self.filename == "/train":
            df = pd.read_csv("train.csv")
            clientConnection.send(bytes(df.to_html(), "UTF8"))
        # GET flight tickets data
        elif self.filename == "/flight":
            df = pd.read_csv("flight.csv")
            clientConnection.send(bytes(df.to_html(), "UTF8"))
        # GET transactions data
        elif self.filename == "/transactions":
            df = pd.read_csv("payments/transactions.csv")
            clientConnection.send(bytes(df.to_html(), "UTF8"))
        # default case for any false GET requests
        else:
            clientConnection.send(bytes("Route not defined!", "UTF8"))
        return


# POST request handler
class POSTRequest:
    def __init__(self, reqString):
        self.reqString = reqString
        self.path = ""
        self.body = ""

    # Parse request path and body
    def parser(self):
        reqSplits = self.reqString.split()
        self.path = reqSplits[1]
        self.body = reqSplits[-1]

    def reqHandler(self, clientConnection):
        global it_list
        print(self.body)
        # Handle login request
        # Check if username and password are correct
        # Redirect to itinerary page if correct
        # Redirect to login page if incorrect
        if self.path == "/auth":
            # split the body to get username and password
            bodySplits = self.body.split("&")
            username = bodySplits[0].split("=")[1]
            password = bodySplits[1].split("=")[1]
            # check if username and password are match with any of the uname and psd from ./auth/auth.csv
            df = pd.read_csv("./auth/auth.csv")
            df = df[df["uname"] == username]
            df = df[df["psd"] == password]
            # if username and password are not found correct
            if df.empty:
                # An alert is displayed on the login page and
                # the user is redirected to the login page
                res = """
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                    <meta charset="UTF-8">
                    <title>Travel Auth</title>
                    <script>
                        localStorage.removeItem("username");
                        alert("Username Not found! Please try again!");
                        window.location.href = "http://localhost:8080/";
                    </script>
                    </head>
                    <body>
                    </body>
                    </html>
                """
                clientConnection.sendall(str.encode("HTTP/1.0 200 OK\n", "iso-8859-1"))
                clientConnection.sendall(
                    str.encode("Content-Type: text/html\n", "iso-8859-1")
                )
                clientConnection.send(str.encode("\r\n"))
                clientConnection.send(bytes(res, "UTF8"))
            else:
                # redirect to itinerary page on successful login
                clientConnection.sendall(str.encode("HTTP/1.0 200 OK\n", "iso-8859-1"))
                clientConnection.sendall(
                    str.encode("Content-Type: text/html\n", "iso-8859-1")
                )
                clientConnection.send(str.encode("\r\n"))
                with open("index.html", "r") as f:
                    clientConnection.send(bytes(f.read(), "UTF8"))
        # Handle register request
        # Append the username and password to auth.csv
        # Redirect to login page
        elif self.path == "/register":
            # split body to get username, password and name
            bodySplits = self.body.split("&")
            username = bodySplits[0].split("=")[1]
            password = bodySplits[1].split("=")[1]
            name = bodySplits[2].split("=")[1]
            # check if username and password are match with any of the uname and psd from ./auth/auth.csv
            df = pd.read_csv("./auth/auth.csv")
            df = df[df["uname"] == username]
            if df.empty:
                # append uname, psd and name to ./auth/auth.csv
                with open("./auth/auth.csv", "a") as f:
                    f.write(f"{username},{password},{name}")
                # redirect to itinerary page
                clientConnection.sendall(str.encode("HTTP/1.0 301 OK\n", "iso-8859-1"))
                clientConnection.sendall(
                    str.encode("Content-Type: text/html\n", "iso-8859-1")
                )
                clientConnection.sendall(
                    str.encode("Location: http://localhost:8080/\n", "iso-8859-1")
                )
                clientConnection.send(str.encode("\r\n"))
            else:
                # An alert is displayed on the register page and the user is redirected to the register page
                res = """
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                    <meta charset="UTF-8">
                    <title>Travel Auth</title>
                    <script>
                        localStorage.removeItem("username");
                        alert("Username already exists!");
                        window.location.href = "http://localhost:8080/register";
                    </script>
                    </head>
                    <body>
                    </body>
                    </html>
                """
                clientConnection.sendall(str.encode("HTTP/1.0 200 OK\n", "iso-8859-1"))
                clientConnection.sendall(
                    str.encode("Content-Type: text/html\n", "iso-8859-1")
                )
                clientConnection.send(str.encode("\r\n"))
                clientConnection.send(bytes(res, "UTF8"))
        # Handle booking confirmation request
        # Append the booking details with transaction details to transactions.csv
        # Append the booking details to username.csv
        # Update the ticket count in the respective csv files
        elif self.path == "/book":
            # split body to get username, password and name
            bodySplits = self.body.split("&")
            username = bodySplits[0].split("=")[1]
            confirmBooking(username)
            clientConnection.sendall(str.encode("HTTP/1.0 301 OK\n", "iso-8859-1"))
            clientConnection.sendall(
                str.encode("Location: http://localhost:8080/itinerary\n", "iso-8859-1")
            )
        # Handle itinerary request
        # Append the itinerary details to itinerary.csv
        # Redirect to itinerary page
        elif self.path == "/itinerary":
            convertXLSXToCSV()
            # split body at every '&' to get the data and convert it to a dictionary
            bodySplits = self.body.split("&")
            bodyDict = {}
            for i in bodySplits:
                bodyDict[i.split("=")[0]] = i.split("=")[1]
            # sort places according to arrival dates
            sortedPlaceData = extractAndSortFormData(bodyDict)
            # generate itinerary and store it to global object
            it_list = generateItenerary(sortedPlaceData)
            # compute final cost of itenary
            final_cost = 0
            for i in range(it_list.__len__()):
                final_cost += it_list[i].cost
            # print final cost
            print("Final cost: ", final_cost)
            # generate html response which replaces the placeholders with actual data
            res = ItineraryResponseHTMLText(it_list, final_cost)
            clientConnection.sendall(str.encode("HTTP/1.0 200 OK\n", "iso-8859-1"))
            clientConnection.sendall(
                str.encode("Content-Type: text/html\n", "iso-8859-1")
            )
            clientConnection.send(str.encode("\r\n"))
            clientConnection.send(bytes(res, "UTF8"))
        # Handle profile request
        # Redirect to profile page
        elif self.path == "/profile":
            # split body to get username
            bodySplits = self.body.split("&")
            username = bodySplits[0].split("=")[1]
            # get name from auth.csv using username
            df = pd.read_csv("./auth/auth.csv")
            df = df[df["uname"] == username]
            name = df["name"].values[0]
            # read content of profile.html
            with open("profile.html", "r") as f:
                res = f.read()
            itenaries = ""
            # read content of username.csv
            if os.path.exists("./it_data/" + username + ".csv"):
                df = pd.read_csv("./it_data/" + username + ".csv")
                # generate html for each itenary data read from username.csv
                for i in range(df.shape[0]):
                    itenaries += """
                        <li>
                            <div class="itPlaces">
                                <span>{p1} - {p2} - {p3}</span>
                                <span class="date" >From: {date1} To: {date3}</span>
                            </div>
                            <div class="cost">Rs. {cost}</div>
                        </li>
                    """.format(
                        p1=df.iloc[i]["place1"].upper(),
                        p2=df.iloc[i]["place2"].upper(),
                        p3=df.iloc[i]["place3"].upper(),
                        date1=df.iloc[i]["date1"].split(" ")[0],
                        date3=df.iloc[i]["date3"].split(" ")[0],
                        cost=df.iloc[i]["cost"],
                    )
                # replace placeholders with actual data
                res = res.replace("DATA", itenaries)
            else:
                res = res.replace("DATA", "No itinerary found!")
            # replace placeholders with actual data
            res = res.replace("username", name)
            clientConnection.sendall(str.encode("HTTP/1.0 200 OK\n", "iso-8859-1"))
            clientConnection.sendall(
                str.encode("Content-Type: text/html\n", "iso-8859-1")
            )
            clientConnection.send(str.encode("\r\n"))
            clientConnection.send(bytes(res, "UTF8"))
        return


# Main function
def main():
    # Create a TCP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to the port
    server.bind((LOCALHOST, PORT))
    # Listen for incoming connections (server mode) with one connection at a time
    server.listen(5)
    print("Server started")
    print("Waiting for client request..")
    while True:
        # clientConnection: socket object
        # clientAddress: socket address
        clientConnection, clientAddress = server.accept()
        print("Connected clinet :", clientAddress)
        # receive request data from client
        data = clientConnection.recv(2048)
        # parsing the request string to extract request METHOD
        hp = HTTPParser(data.decode())
        hp.parser()
        # fork a new process to handle the request (Works only on Linux)
        # pid = os.fork()
        # if pid == 0:
        if hp.reqType == "GET":
            fname = hp.reqString.split()[1]
            gReq = GETRequest(fname)
            gReq.reqHandler(clientConnection)
        elif hp.reqType == "POST":
            pReq = POSTRequest(hp.reqString)
            pReq.parser()
            pReq.reqHandler(clientConnection)
        else:
            print("Invalid request type!!")
        clientConnection.close()
            # os._exit(0)
        # else:
        #     clientConnection.close()


# Driver code
if __name__ == "__main__":
    main()
