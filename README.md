# News Board
A news board service that contains : 

### User Access Service
  1. Register API
     - `127.0.0.1;8000/register`
     - Parameters : *(username, password)*
  2. Log In API
     - `127.0.0.1;8000/login`
     - Parameters : *(username, password)*
  3. Log Out API
     - `127.0.0.1;8000/logout` 
     - Parameters : *none*

### News Access Service 
  1. Get All News
     - `127.0.0.1:8000/getall`
     - Parameters : *none*
  2. Get News 
     - `127.0.0.1:8000/getbyid`
     - Parameters : *(news-id)*
  3. Download News
     - `127.0.0.1:8000/download`
     - Parameters : *(news-id)*
#### [Log In Required]
  4. Add News
     - `127.0.0.1:8000/add`
     - Parameters : *(title, content, image)*
  5. Edit News
     - `127.0.0.1:8000/edit`
     - Parameters : *(news-id, title, content, image)*
  6. Delete News
     - `127.0.0.1:8000/delete`
     - Parameters : *(news-id)*

## Requirements for running the service
  This service uses *python*, *nameko*, *redis*, and *mySQL*.
  
## Steps
  1. Clone this repository
  2. Import the *.sql* inside `sql` folder into your local mySQL database.
  3. Open 2 CMDs
  4. On both CMDs, type `cd session` to move into the `session` directory
  5. On the first CMD, type `nameko run service` to run the gateway.
  6. On the second CMD, type `nameko run news_service` to run the news service.
  7. To test the API using *Postman*, import the *.postman_collection* file inside `postman` folder into your *Postman*.
