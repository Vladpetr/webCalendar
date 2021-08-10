# webCalendar
A web application that will save all your events to the database.

**webCalendar** is a simple REST service with the Flask framework. It works with a database using the Flask-SQLAlchemy extension and creates resources using the Flask-RESTful extension.

The following operations were performed:
* [x] Handle GET and POST requests from the client and parse arguments from the request body.
* [x] Create a database and save all the events in it.
* [x] Process and delete events by ID. 
* [x] Add an ability to get information about events in a specific date range.

## Technologies used

- python - version 3.8
- flask - version 1.1.4


## License

    Copyright [2021] [Vladyslav Petrenko]

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
