# RideOn
A ride sharing app developed as part of the UVA CS3240 curriculum

## Build Status
**Master**
![Master Build Status](https://travis-ci.com/uva-cs3240-f19/project-102-rideon.svg?token=6qzs2Kors1PzmyQsy5PA&branch=master)

**Develop**
![Develop Build Status](https://travis-ci.com/uva-cs3240-f19/project-102-rideon.svg?token=6qzs2Kors1PzmyQsy5PA&branch=develop)

## Features

1. Creating rides
	* Users can create a ride from a place to another place at a time. This is the thing that gets shared. Other users can request to join the ride.
2. Passenger management
	* The owner of a ride can see requests to join the ride and accept or reject them. They can see who is in the ride and remove them as they desire.
3. Waypoints
	* For some users, especially those who live many hours away, the idea of a "waypoint" is useful. This is a stop the driver makes during the ride and is requested by a passenger when they request to join a ride. Example: the drive is to Miami. Another student can request a waypoint in Savanna because it is not far out of the way.
4. Searching
	* There are powerful searching tools that can be used to find useful drives. They allow for searching by date, rating, cost, description, etc
5. Reviews
	* When a drive is completed, everyone in the drive has the opportunity to review eachother. This is found in the "My Rides" option of the profile menu dropdown. These reviews are then used to create the "Driver Rating" and "Rider Rating" on the Profile Page
6. Custom Profiles
	* Users can customize their profiles with usernames, descriptions, profile images, etc
7. Friends
	* This is analogous to the "follower" system on Twitter. A user can have friends which can then be used to search for rides. This allows users to find rides that have people they know and like in them.

## Test Accounts

Normal login must be done through OAuth with a UVA email account. However, for testing purposes it is useful to be able to use multiple accounts. Administrator accounts can still log on with a normal username and password by following these steps:

1. Go to `https://uva-ride-on.herokuapp.com/admin`
2. Enter the correct username and password
3. Go to `https://uva-ride-on.herokuapp.com/`

You are now logged in to an administrator account.

### Account Details

admin1 : Chiapet1

admin2 : Chiapet2

admin3 : Chiapet3