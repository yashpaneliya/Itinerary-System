# Travel Itinerary Planner
Project for the course "CS69201: Computing Lab"

## Description
This project is a travel itinerary planner. It takes in a list of cities, departure dates, preffered modes of transportation, days of stay and outputs a list of cities to visit in a given order. It also outputs the total cost of the trip.

## Directory Structure
```
├── README.md
├── auth
│   ├── auth.csv
├── it_data
│   ├── <USERNAME>.csv
├── payments
│   ├── transactions.csv
├── database
│   ├── bus.csv
│   ├── flight.csv
│   ├── train.csv
├── pages
│   ├── index.html
│   ├── auth.html
│   ├── itenary.html
│   ├── register.html
│   ├── profile.html
├── server.py
├── sockserver.py
├── server.ipynb
```

## How to run
1. Clone the repository

2. Now there are two different servers, one is built using sockets from scratch and other is built using http module of python. (Both serve same functionalities)
    1. To run the server built using sockets, run the following command:
    ```bash
    python sockserver.py
    ```
    2. To run the server built using http module, run the following command:
    ```bash
    python server.py
    ```
3. Open the browser and go to the following url:
    ```bash
    http://localhost:8080/
    ```
4. Now you can register and login to the website and use the services provided by the website.