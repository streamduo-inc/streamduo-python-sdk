Feature: User Admin APIs

Scenario: Check Health
     Given we are logged in
     When we check health
     Then health is ok

Scenario Outline: Write to Stream
     Given we are logged in
     and a <Payload>
     When we create an organization alpha.io with user squirrel
     And we create an organization beta.io with user bear
     And we create a stream named SuperStream with Producer alpha.io and Consumer beta.io
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

