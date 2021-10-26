Feature: User Admin APIs

Scenario: Check Health
     Given we are logged in
     When we check health
     Then health is ok

Scenario Outline: Write to Stream and get single record
     Given we are logged in
     When we create an organization alpha.io with user squirrel
     And we create an organization beta.io with user bear
     And we create a stream named SuperStream
     Then stream SuperStream exists when queried
     When we ADD clientId client_id_1 on stream SuperStream as PRODUCER
     And we ADD clientId client_id_2 on stream SuperStream as CONSUMER
     Then clientId client_id_1 exists in stream SuperStream as PRODUCER
     And clientId client_id_2 exists in stream SuperStream as CONSUMER
     When we write <RecordName> with payload <Payload> to stream SuperStream
     Then we query the record <RecordName> in stream SuperStream and readStatus is FALSE
     And we query the record <RecordName> in stream SuperStream and readStatus is TRUE

     Examples: Input Variables
          |RecordName |Payload                   |
          |record01   |{"name": "Fred", "age":2} |
          |record02   |{"name": "Reggie", "stats": {"rbi": 75, "home runs": 32, "team": "New York"}}|

Scenario: Write to Stream and get all unread
     Given we are logged in
     When we create an organization alpha.io with user squirrel
     And we create an organization beta.io with user bear
     And we create a stream named SuperStream
     And we ADD clientId client_id_1 on stream SuperStream as PRODUCER
     And we ADD clientId client_id_2 on stream SuperStream as CONSUMER
     And we write record01 with payload {"name": "Fred", "age":2} to stream SuperStream
     And we write record02 with payload {"name": "John", "age":3} to stream SuperStream
     And we write record03 with payload {"name": "Ted", "age":4} to stream SuperStream
     Then we query the record record01 in stream SuperStream and readStatus is FALSE
     And we query the record record01 in stream SuperStream and readStatus is TRUE
     When we query all unread records in stream SuperStream
     Then length of resultSet is 2
     And record record02 is in resultSet
     And record record03 is in resultSet
     And record record01 is not in resultSet
     When we query all unread records in stream SuperStream
     Then length of resultSet is 0

