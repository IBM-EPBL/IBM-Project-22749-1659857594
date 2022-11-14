# importing csv module for database
import csv
import qrcode 
import pyqrcode
import png
from pyqrcode import QRCode
  
  
# importing the qrcode library  
 
# three parent classes to follow SRP where all the changes are done in one place. (three reasons of changes, therefore three classes for change.)
class price_changes():
    def price_declare(self):
        #creating a dictionary with compartment names as keys and its prices as values.
        self.price = {'First_AC_Class' : 2000,
                 'Second_AC_Class': 1500,
                 'Third_AC_Class': 1000,
                 'Sleeper' : 500};
class seats_changes():
    def seats_declare(self):
        #creating a dictionary with compartment names as keys and its number of total seats as values.
        self.seats = {'First_AC_Class' : 50,
                 'Second_AC_Class': 100,
                 'Third_AC_Class': 150,
                 'Sleeper' : 200};
class refund_percent_changes():
    def refund_percent_declare(self):
        self.confirm_refund_percent = 5
        self.waiting_refund_percent = 10

        
#parent class
class reservation():
    
    # input function to input informations which is common to both child classes
    def input(self):
        #taking passengers information from user
        self.fname = input("Enter your first name: ");
        self.lname = input("Enter your last name: ");
        self.age = int(input("Enter your age: "));
        self.gender = input("Enter your gender: ");
    
    def choice(self):
        #asking for either to book or cancel a ticket. This line is executed before entering any child class.
        option = input("Enter 'book' to book a ticket, 'cancel' to cancel your ticket: ");

        #if we opt for booking a ticket: call book() child class
        if option == "book":
            b = book()
            #calling availablity function
            b.availablity();
            #calling the payment function
            b.payment();
            #calling the confirm function
            b.confirm();
            #calling the database function
            b.database();
            #calling the ticket_printing function
            b.booked_ticket_printing();

        #else if we choose to cancel : call cancel() child class
        elif option == "cancel": 
            c = cancel()
            #calling check() function, that internally calls refund function. Refund function calls update function
            c.check();
            
        else :
            print("Invalid option");
    # ticket_printing function to print all informations which is common to both child classes
    def ticket_printing(self):
        print("Passenger's first name:",self.fname)
        print("Passenger's last name:",self.lname)
        print("Passenger's age:",self.age)
        print("Passenger's gender:",self.gender)
    
    
# creating child class cancel for booking purpose
class book(reservation,price_changes,seats_changes,refund_percent_changes):
    #default constructor 
    def __init__(self):
        self.input() # call parent input function for input
        self.price_declare()
        self.seats_declare()
        self.refund_percent_declare()
        self.compartment = input("Enter choice of compartment to book: "); 
        self.coupon = ""
        self.availability = ""
        self.mode = ""
        self.completion = ""
        
    #creating three differrnt functions for checking availability, askig payemnt mode and completing the booking process
    #function for checking availability
    def availablity(self):
        #everytime before confirming, check if the seats are available i.e. >0 for a particular compartment
        if self.seats[self.compartment] > 0:
            print("Seats Available.");                
            self.availability = "Available"

            #for each seat booking, create a unique coupon that may be used if the user asks for cancelation.
            #coupon is created using "C" for confirm ticket followed by 1st 3 letters of first and last name + Gender + compartment
            self.coupon = 'C' + self.fname[0] + self.lname[0] + self.gender[0] + self.compartment
            print("Your booking code is",self.coupon, ".")

            #updating the number of seats available after a booking is made
            self.seats[self.compartment] -= 1

            #appending all the coupons in a list
            confirm_coupon.append(self.coupon);
        else:
            #if no confirmed seat available
            print("Waiting list.");
            self.availability = "Waiting"

            #generate coupon in same way as for confirmed ticket(replace "C" with "W")
            self.coupon = 'W' + self.fname[0] + self.lname[0] + self.gender[0] + self.compartment

            print("Your booking code is",self.coupon,".")

            #append the waiting list
            waiting_coupon.append(self.coupon);

    #function for accepting payment
    def payment(self):
        print("You have to pay",self.price[self.compartment],"rupees.");
        #ask for mode of payment
        self.mode = input("Payment Mode : Cash or Card or Internet Banking?")

    #function for completion of the ticket booking process
    def confirm(self):
        self.completion = "Process completed"
        
    # function for update of the booked ticket in database
    def database(self):
        with open('bookings.csv', 'a', newline = '') as file:
            writer = csv.writer(file)
            writer.writerow([self.coupon,self.fname,self.lname,self.age,self.gender,self.compartment,self.availability,self.price[self.compartment],self.mode,self.completion])
        file.close()

    # printing of the full ticket after completion of the booking process
    def booked_ticket_printing(self):
        print()
        print("DEMAND FOR BOOKING TICKET");
        self.ticket_printing(); #calling function of the parent class
        print("Booked in compartment:",self.compartment)
        print("Availability of compartment:",self.availability)
        print("You have to pay",self.price[self.compartment],"rupees.");
        print("Payment mode:",self.mode)
        print("Your Coupon Code:",self.coupon)
        print("Process completed.");
        print()
        # Extra information for the user to read.
        print("There is a refund on cancellation of your ticket.")
        print("For confirmed ticket -" ,self.confirm_refund_percent,"% of ticket price refund.")
        print("For waiting ticket -", self.waiting_refund_percent,"% of ticket price refund.")
        print("You just have to remember the Coupon Code.")
        qr_img = qrcode.make("Dwarakeswaran")  
        qr_img.save("qr-img.jpg")
        
# creating child class cancel for cancellation purpose
class cancel(reservation,price_changes,seats_changes,refund_percent_changes):
    def __init__(self):
        # taking passengers information with coupon number created at the time of booking
        self.input()
        self.price_declare()
        self.seats_declare()
        self.refund_percent_declare()
        self.coupon = input("Enter your booking coupon: ");
        self.re =0;
        
    #function for authenticating the coupon number
    def check(self):

        #check the first word of coupon number
        if self.coupon[0] == 'W':

            #if coupon number is present in waiting coupon list call the refund function
            if self.coupon in waiting_coupon:
                self.refund();
            else :
                print("You entered wrong code.")

        #check the first word of coupon number
        elif self.coupon[0] == 'C':

            #if coupon number is present in confirm coupon list call the refund function
            if self.coupon in confirm_coupon:
                self.refund();
            else :
                print("You entered wrong code.")
        else:
            print("You entered wrong code.")

    #calling the child refund function
    def refund(self):
        if self.coupon[0] == 'C':

            ##if ticket is confirmed then look for compartment from coupon and return the 50% of the price of ticket
            self.re = self.price[self.coupon[4:]] - self.price[self.coupon[4:]]*(self.confirm_refund_percent/100);
        elif self.coupon[0] == 'W':

            #if ticket is in waiting list then look for compartment from coupon and deduct the 10% of the price of ticket
            self.re = self.price[self.coupon[4:]] - self.price[self.coupon[4:]]*(self.waiting_refund_percent/100);
            
        print("Your refund is",self.re,"rupees.");

        #call update function
        self.update();

    #after making the cancelation and refund, we need to update the number of seats.
    def update(self):

        #check for confirm or waitlist category: if confirm
        if self.coupon[0] == 'C':

            #increment the number of seats by 1 particularly in the compartment booking was made
            self.seats[self.coupon[4:]] += 1;

            #using remove function to delete the coupon from list so as to avoid repetative refund
            confirm_coupon.remove(self.coupon);

            #if cancellation is from confirmed list then it will move the first entry of waiting list in confiremd category
            if len(waiting_coupon) > 0:
                confirm_coupon.append(waiting_coupon[0]);
                waiting_coupon.remove(0)
        elif self.coupon[0] == 'W':

            #remove the waiting coupon from the list
            waiting_coupon.remove(self.coupon);

        # this will delete the whole row containing the coupon code entered by user for cancelling the ticket
        updatelist=[]
        with open("bookings.csv",newline="") as f:
            reader=csv.reader(f)
            for row in reader: # loop through every row in the file

                if row[0]!=self.coupon: # as long as the username is not in the row 
                    updatelist.append(row) # adding each row, one line after the other, into a list called 'udpatelist'
        f.close()
        with open("bookings.csv","w",newline="") as f:
            Writer=csv.writer(f)
            Writer.writerows(updatelist)
        f.close()
        
        self.cancelled_ticket_printing() # calling own function for printing
    
    # printing of the full ticket after completion of the cancelltion process
    def cancelled_ticket_printing(self):
        print()
        print("DEMAND FOR CANELLING TICKET");
        self.ticket_printing(); #calling function of the parent class
        print("Your Coupon Code:",self.coupon)
        print("Your refund is",self.re,"rupees.");
        print("You saved (",self.price[self.coupon[4:]],"-",self.re,") =",self.price[self.coupon[4:]]-self.re,"rupees.")
        print("Process completed.");        
        print()

# Main Function
#initializing 2 empty list for string unique confirm and waiting list coupons respectively used in the function
confirm_coupon = []     
waiting_coupon = []

#infinite loop unless the user terminates 
#computer first and foremost moves it's control here before executing any other function
while(True):
    
    #calling the parent function which internally calls different child function depending upon the choice user makes
    r = reservation(); 
    r.choice();
    
    #user enter 0, the while infinite loop terminatesfir
    if int(input("Enter 1 continue with railway reservations, 0 to stop: ")) != 1:
 

       break;
