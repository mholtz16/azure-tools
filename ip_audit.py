import csv
import ipaddress


with open("FirewallRules.csv", "r") as file: 
    data = list(csv.reader(file))

for row in data:
    if row[3] != row[4]:
        print(row[3],row[4])

