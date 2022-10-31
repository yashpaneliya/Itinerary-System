from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi
import os
import pandas as pd
from dateutil import parser

PORT = 8080

# Booking id
booking_id = 0
def generateBookingID():
    global booking_id
    booking_id += 1
    return booking_id

# file variables
csv_files = []
csv_file_names = ["train.csv", "flight.csv", "bus.csv"]

# Final iternary list of places
it_list = []
# convert train.xlsx, bus.xlsx, flight.xlsx to csv
def convertXLSXToCSV():
    csv_files.append(pd.read_csv("train.csv"))
    csv_files.append(pd.read_csv("flight.csv"))
    csv_files.append(pd.read_csv("bus.csv"))


# create a class PlaceData with members name,date,mode,days,status,cost
class PlaceData:
    def __init__(self, name, date, mode, days, status, cost):
        self.name = name
        self.date = date
        self.mode = mode
        self.days = days
        self.status = status
        self.cost = cost

    # setter for status and cost
    def setStatus(self, status):
        self.status = status

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


def extractAndSortFormData(form):
    print("form data: ")
    # print foem data
    for item in form.list:
        print(item)
    # Array of objecs of class PlaceData
    placeData = []
    # Extract p1,date1,days1 from form data and store it to object of PlaceData class
    p1 = form.getvalue("p1")
    # convert date1 to datetime object
    date1 = parser.parse(form.getvalue("date1"))
    days1 = form.getvalue("days1")
    mode1 = form.getvalue("mode1")
    placeData.append(PlaceData(p1, date1, mode1, days1, False, 0))
    # Extract p2,date2,days2 from form data and store it to object of PlaceData class
    p2 = form.getvalue("p2")
    # convert date2 to datetime object
    date2 = parser.parse(form.getvalue("date2"))
    days2 = form.getvalue("days2")
    mode2 = form.getvalue("mode2")
    placeData.append(PlaceData(p2, date2, mode2, days2, False, 0))
    # Extract p3,date3,days3 from form data and store it to object of PlaceData class
    p3 = form.getvalue("p3")
    # convert date3 to datetime object
    date3 = parser.parse(form.getvalue("date3"))
    days3 = form.getvalue("days3")
    mode3 = form.getvalue("mode3")
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
        print("i:", i)
        mIndex = getMode(places[i])
        df = csv_files[mIndex]
        print("df:", df.head())
        df = df[df["p1"] == places[i].name]
        print("df:", df)
        print(places[i + 1].name)
        df = df[df["p2"] == places[i + 1].name]
        print(df.head())
        print(df["tkt"].iloc[0])
        if int(df["tkt"].values[0]) > 0:
            places[i].setStatus(True)
            places[i].setCost(int(df["cost"].values[0]))
            it_list.append(places[i])
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
        mIndex = getMode(it_list[i])
        df = csv_files[mIndex]
        edf = csv_files[mIndex]
        df = df[df["p1"] == it_list[i].name]
        df = df[df["p2"] == it_list[i + 1].name]
        tk_count = int(df["tkt"].values[0])
        edf.loc[
            (edf["p1"] == it_list[i].name) & (edf["p2"] == it_list[i + 1].name),
            "tkt",
        ] = (
            tk_count - 1
        )
        edf.to_csv(csv_file_names[mIndex], index=False)
    # append it_list to file named as username.txt
    # create a new file if it does not exist
    if not os.path.exists("./it_data/" + username + ".csv"):
        f = open("./it_data/" + username + ".csv", "w")
        f.write("id,place1,place2,place3,date1,date2,date3,cost")
        f.write("\n")
        f.close()
    generateBookingID()
    # # append it_list to file named as username.txt
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

class reqHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        print(self.path)
        if self.path == "/itinerary":
            # read content of index.html
            with open("index.html", "r") as f:
                self.wfile.write(bytes(f.read(), "utf8"))
        elif self.path == "/":
            # read content of auth.html
            with open("auth.html", "r") as f:
                self.wfile.write(bytes(f.read(), "utf8"))
        elif self.path == "/register":
            # read content of register.html
            with open("register.html", "r") as f:
                self.wfile.write(bytes(f.read(), "utf8"))
        elif self.path == "/bus":
            df = pd.read_csv("bus.csv")
            print(df.columns.values.tolist())
            self.wfile.write(bytes(df.to_string(), "utf8"))
        elif self.path == "/images/japanback.jpg":
            self.send_header("Content-type", "image/jpeg")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            with open("images/japanback.jpg", "rb") as fout:
                self.wfile.write(fout.read())
        else:
            self.wfile.write(bytes("Route not defined!", "utf8"))
        return

    def do_POST(self):
        global it_list
        print("POST request received!")
        if self.path == "/book":
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={
                    "REQUEST_METHOD": "POST",
                    "CONTENT_TYPE": self.headers["Content-Type"],
                },
            )
            print("Your name is: %s" % form.getvalue("username"))
            confirmBooking(form.getvalue("username"))
            self.send_response(301)
            self.send_header("Location", "http://localhost:8080/itinerary")
            self.end_headers()
        elif self.path == "/auth":
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={
                    "REQUEST_METHOD": "POST",
                    "CONTENT_TYPE": self.headers["Content-Type"],
                },
            )
            print("Your name is: %s" % form.getvalue("username"))
            print("Your password is: %s" % form.getvalue("password"))
            # check if username and password are match with any of the uname and psd from ./auth/auth.csv
            df = pd.read_csv("./auth/auth.csv")
            df = df[df["uname"] == form.getvalue("username")]
            df = df[df["psd"] == form.getvalue("password")]
            if df.empty:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                res = """
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                    <meta charset="UTF-8">
                    <title>Authentication Failed!!</title>
                    <script>
                        localStorage.removeItem("username");
                    </script>
                    </head>
                    <body>
                    <h1>Authentication Failed</h1>
                    <a href="http://localhost:8080/">Try again</a>
                    </body>
                    </html>
                """
                self.wfile.write(bytes(res, "utf8"))
            else:
                # redirect to itinerary page
                self.send_response(301)
                self.send_header("Location", "http://localhost:8080/itinerary")
                self.end_headers()
        elif self.path == "/register":
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={
                    "REQUEST_METHOD": "POST",
                    "CONTENT_TYPE": self.headers["Content-Type"],
                },
            )
            print("Your name is: %s" % form.getvalue("username"))
            print("Your password is: %s" % form.getvalue("password"))
            # check if username and password are match with any of the uname and psd from ./auth/auth.csv
            df = pd.read_csv("./auth/auth.csv")
            df = df[df["uname"] == form.getvalue("username")]
            if df.empty:
                # append uname and psd to ./auth/auth.csv
                with open("./auth/auth.csv", "a") as f:
                    f.write(
                        form.getvalue("username")
                        + ","
                        + form.getvalue("password")
                        + ","
                        + form.getvalue("name")
                        + "\n"
                    )
                # redirect to itinerary page
                self.send_response(301)
                self.send_header("Location", "http://localhost:8080/")
                self.end_headers()
            else:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                res = """
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                    <meta charset="UTF-8">
                    <title>Username already exists!!</title>
                    <script>
                        localStorage.removeItem("username");
                    </script>
                    </head>
                    <body>
                    <h1>Username already exists</h1>
                    <a href="http://localhost:8080/register">Try again</a>
                    </body>
                    </html>
                """
                self.wfile.write(bytes(res, "utf8"))
        elif self.path == "/itinerary":
            # extract form data from POST request and save it
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={
                    "REQUEST_METHOD": "POST",
                    "CONTENT_TYPE": self.headers["Content-Type"],
                },
            )
            sortedPlaceData = extractAndSortFormData(form)
            convertXLSXToCSV()
            it_list = generateItenerary(sortedPlaceData)
            # compute final cost of itenary
            final_cost = 0
            for i in range(it_list.__len__()):
                final_cost += it_list[i].cost
            # print final cost
            print("Final cost: ", final_cost)
            res = ItineraryResponseHTMLText(it_list, final_cost)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(res, "utf8"))
        elif self.path == "/profile":
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={
                    "REQUEST_METHOD": "POST",
                    "CONTENT_TYPE": self.headers["Content-Type"],
                },
            )
            print("Your name is: %s" % form.getvalue("username"))
            username = form.getvalue("username")
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
                res = res.replace("DATA", itenaries)
            else:
                res = res.replace("DATA", "No itinerary found!")
            res=res.replace("username", name)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(res, "utf8"))
        return


def main():
    try:
        server = HTTPServer(("", PORT), reqHandler)
        print("Started httpserver on port 8080...")
        server.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down the web server")
        server.socket.close()


if __name__ == "__main__":
    main()
