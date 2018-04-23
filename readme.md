[![Build Status](https://travis-ci.com/emmafass/CioYardSale.svg?token=U3FKwpr9HPvU3J7Stytp&branch=master)](https://travis-ci.com/emmafass/CioYardSale)

## Start Working on the Project

docker start mysql

docker start web

docker attach web

OR

docker-compose up

*run the `docker-compose up` command in the normal terminal window in the same directory as docker-compose.yml You do not need to start web but make sure mysql is running.*


## General Debugging
Check to make sure you spelled Authenticator correctly / the way it is spelled in the model.

## Using Postman

### Create

#### Commodity

Use the parameters in the BODY section. Format the parameters like so.

![image](https://github.com/emmafass/CioYardSale/blob/master/images/postman_create_commodity.png)

Even though it says there was an error, if you check readAll the item is created.

## During Demo

Ask about the time field in the create commodity function - getting a strange response. (See pic above)

Ask about how to run the tests in the web container

The new User model
  * Added a myUser app to the CioYardSale project (the models layer)
