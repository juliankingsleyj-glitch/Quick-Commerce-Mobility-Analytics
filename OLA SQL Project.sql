Select * From Ride_Data

--1. Retrieve all successful bookings:

Select * From ride_data
Where booking_status = 'Success';

SELECT * FROM Ques1;


--2. Find the average ride distance for each vehicle type:

Select Vehicle_Type, 
Round(Avg(Ride_Distance)::numeric,2) as avg_distance 
From ride_data
Group By Vehicle_Type;

Select * from Ques2;


--3. Get the total number of cancelled rides by customers:

Select Count(*) From ride_data
Where Booking_Status = 'Cancelled by Customer';

Select * from Ques3;


--4. List the top 5 customers who booked the highest number of rides:

Select Customer_ID, Count(Booking_ID) as total_rides
From ride_data
Group By Customer_ID
Order By total_rides DESC Limit 5;

Select * from Ques4;


--5. Get the number of rides cancelled by drivers due to personal and car-related issues:

Select Count(*) from ride_data
Where Reason_for_cancelling_by_Driver = 'Personal & Car related issues';

Select * from Ques5;

--6. Find the maximum and minimum driver ratings for Prime Sedan bookings:

Select 
  Max(Driver_Ratings) As Max_Rating,
  Min(Driver_Ratings) As Min_Rating
From ride_data
Where 
  Vehicle_Type = 'Prime Sedan' 
  And Driver_Ratings Is Not Null;

Select * from Ques6;  

--7. Find the average customer rating per vehicle type:

Select Vehicle_Type, 
Round(Avg(Customer_Rating)::numeric, 2) As Avg_Customer_Rating
From ride_data
Where Customer_Rating Is Not Null
Group By Vehicle_Type;

Select * from Ques7;

--8. Calculate the total booking value of rides completed successfully: 

Select
  Round(Sum(Booking_Value)::numeric, 2) As Total_Booking_Value
From 
  ride_data
Where 
  booking_status = 'Success';

Select * from Q8;

--9. List all incomplete rides along with the reason

Select Booking_Id, Incomplete_Rides_Reason
From ride_data
Where Incomplete_Rides = '1'

Select * from Q9;
