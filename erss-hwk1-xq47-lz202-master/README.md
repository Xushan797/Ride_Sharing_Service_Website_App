Django Web-App: Ride Sharing Service    

Xushan Qing: xq47  
Lanxin Zhang: lz202  

Here are some instructions for the details of the function in the requirement:  
1. Login with a valid user account  
(1) When creating account, user need to use unique username and email  

2. Handle login failure with an an invalid user account  

3. Logout from a user session  
    (1) The user will always login as long as session has its information, unless logout  

4. User should be able to register as a driver by entering their personal & vehicle info  
    (1) the max passenger that a driver can have is between 1 - 10  
    (2) speicial vehicle info is optional, other fields are required  
    (3) if no special info, leave it blank  
    (4) former input shows the information in the database  
    (5) None means no information  
    (6) once save the user driver information, it would become a driver  
    (7) driver name field is different from the username  

5. User should be able to view and edit their driver status as well as personal & vehicle info  

6. User should be able to submit a ride request by specifying the required and any combination of the optional info  
    (1) if no special info or type, leave it blank  
    (2) order max passenger is between 1 - 10  
    (3) the order timefield only valid later than the present time  
    (4) vehicle type and info is optional  

7. User should be able to make a selection to view any non-complete ride they belong to  
    (1) in the my_rides_detail link in the mainpage. mainpage only shows the open orders  
    (2) user can see their order as driver, sharer and owner in  the my_rides_detail link  

8. User should be able to make a selection to edit any open ride they belong to  
    (1) order owner can edit destination, arrival-time, add passenger, vehicle type and info  
    (2) order driver can confirm or complete the order  
    (3) order sharer can only edit add passenger  
    (4) once owner change the destination and arrival-time, sharer of the order would automatically quit and be informed  
    (5) user can choose to become driver as long as registered as driver before, or become sharer  

9. A ride owner should be able to edit the requested attributes of a ride until that ride is confirmed  
    (1) once user become a driver of the order, the order is confirmed and cannot edit  

10. User should be able to view all ride details for any open ride they belong to  
    (1) mainpage show all the open ride  

11. User should be able to view all ride details + driver and vehicle details for any confirmed ride they belong to  
12. User should be able to search for sharable, open ride requests (by destination, arrival window, and # of passengers)  
    (1) # of passengers means how many open seat left that can acommodate. Max passenger for a order is 10  
13. User should be able to join a ride returned in a search as described in requirement #13  
    (1) click view/edit to join  
    (2) sharer can only edit the add passenger button after save as a sharer  
14. A registered driver should be able to search for open ride requests (filtered by the driver's vehicle capacity and type / special info, if applicable)
    (1) the input capacity can only less or equal than driver max_passenger  
    (2) only the order required type exactly matches driver vehicle type and order with no required type can be searched  
    (3) can search order with no special info  
    (4) if order have special info, only the order special info exactly matches driver special info can be searched  
15. A registered driver should be able to mark a selected ride (returned from a search as described in requirement #15) as confirmed (thus claiming and starting the ride)  
    (1) once a user become a driver of an order, the order is confirmed  
16. An email should be sent to the owner and any sharers of a ride once it is confirmed by a driver  

17. A driver should be able to see a list of their confirmed rides  
    (1) in the my_rides_detail link  
18. A driver should be able to select a confirmed ride and view all of the ride details  
    (1)  in the my_rides_detail link  
19. A driver should be able to edit a confirmed ride for the purpose of marking it complete after the ride is over  
