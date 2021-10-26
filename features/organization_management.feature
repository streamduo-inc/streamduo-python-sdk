Feature: User Admin APIs

Scenario: Check Health
     Given we are logged in
     When we check health
     Then health is ok

Scenario: Create Organization and Manage Users
     Given we are logged in
     When we create an organization alpha.io with user squirrel
     And we add a user bird to organization alpha.io
     Then the new org alpha.io exists when queried
     And user bird has been added to organization alpha.io
     And user squirrel has been added to organization alpha.io
     When we delete organization alpha.io
     Then the organization alpha.io does not exist when queried

Scenario: Create Organization and Manage Streams
     Given we are logged in
     When we create an organization alpha.io with user squirrel
     And we create an organization beta.io with user bear
     And we create a stream named SuperStream
     Then stream SuperStream exists when queried
     When we ADD clientId client_id_1 on stream SuperStream as PRODUCER
     And we ADD clientId client_id_2 on stream SuperStream as CONSUMER
     And we ADD clientId client_id_3 on stream SuperStream as CONSUMER
     Then clientId client_id_1 exists in stream SuperStream as PRODUCER
     And clientId client_id_2 exists in stream SuperStream as CONSUMER
     And clientId client_id_3 exists in stream SuperStream as CONSUMER
     When we REMOVE clientId client_id_2 on stream SuperStream as CONSUMER
     Then clientId client_id_2 does not exist in stream SuperStream as CONSUMER
     And clientId client_id_3 exists in stream SuperStream as CONSUMER
     When we delete stream SuperStream
     And we delete organization alpha.io
     And we delete organization beta.io
     Then the organization alpha.io does not exist when queried
     And the organization beta.io does not exist when queried
     And the stream SuperStream does not exist when queried