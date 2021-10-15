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

Scenario: Create Organization and Manage Streams
     Given we are logged in
     When we create an organization alpha.io with user squirrel
     And we create an organization beta.io with user bear
     And we create a stream named SuperStream with Producer alpha.io and Consumer beta.io
     Then stream SuperStream exists when queried