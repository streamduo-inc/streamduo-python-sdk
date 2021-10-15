Feature: User Admin APIs

Scenario: Check Health
     Given we are logged in
     When we check health
     Then health is ok

Scenario: Create Organization and Manage Users
     Given we are logged in
     When we create an organization alpha.io with user squirrel
     Then the new org alpha.io exists when queried
     When we add a user bird to organization alpha.io
     Then user bird has been added to organization alpha.io
     And user squirrel has been added to organization alpha.io
