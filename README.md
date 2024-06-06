# Scheduler

Thoughts on my approach (before beginning):

* Create a ScheduleVisit model, include the fields in the request:
```json
{
    "start_date_time": "2023-06-26T23:00:00.000Z",
    "end_date_time": "2023-06-27T22:59:59.999Z",
    "client": 1,
    "carer": 1
}
```
* Add a revision field to the model to track the latest revision

## API Routes

* `GET /schedule/latest` - Return the latest schedule, we just need to query for the maximum value of the "revision" field
* `POST /schedule` - Create a new schedule
* `PUT /schedule/visit/{id}` - Update a schedule, if the schedule already exists we need to increment the revision field
* `DELETE /schedule/{id}` - Delete a schedule, this is a "soft" delete, so we need to set a delete flag in the model, we can copy the last
schedule visit for now and increment the revision + set delete. Delete should return an empty response
* `GET /schedule/{revision}` - Get a schedule by its revision, we can use this to get a specific revision of a schedule


## To run

`python manage.py runserver`

