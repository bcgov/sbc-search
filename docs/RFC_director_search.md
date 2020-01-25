

## Use a real ORM

Currently, a custom ORM-like system is implemented. Standard naming (models.py), class methods for data services, and instances as rows are implemented. However, this fails to leverage the most important benefits of using an ORM.
  * Standardized implementation using SQLAlchemy's ORM would make onboarding new devs easier, and avoid mistakes due to not understanding a home-baked solution. There is a large developer pool of expertise that can be leveraged close to the domain problem. Granted, SQL expertise does exist, but the expertise to use SQL from code is rare and requires extra effort.
  * Code is portable directly to PostgreSQL when moving off Oracle, for "free". No rewriting SQL.
  * Rely on expert ORM developers to generate correct, optimized SQL. Writing your own ORM is like writing assembly instead of C. There may occasionally be reason to, but in most cases it's costly and unnecessary.
  * Many of the concerns with connecting to a database are handled automatically, such as error handling, transaction management, sanitization. It's easy to miss these things, and unnecessary to develop them from scratch.
  * The models can be re-used in other projects, and for other purposes since a generic interface is generated.
  * The existing code is already using SQLAlchemy, but not leveraging most of the benefits of this powerful library, since it's only being used to query via undifferentiated SQL directly. Using an the SQLAlchemy ORM wouldn't require any new libraries on its own.

Counter-arguments. This highly-voted SO answer lists Pros and Cons. https://stackoverflow.com/questions/1279613/what-is-an-orm-how-does-it-work-and-how-should-i-use-one

## Shared model layer

Currently legal-api and colin-api each have their own custom database interface built from scratch.

As discussed in "Use a real ORM", several of the benefits of an ORM rely on linking a given version of the code to a given version of the database, allowing designers to abstract away the database consistently in different contexts, manage migrations. This means sharing the model classes between different codebases that use the same database. Benefits:
  * Define a common database interface that can be tested in isolation, and test coverage can be reused.
  * Manage migrations automatically in the codebase. Even if migrations are rare, this allows the codebase to robustly handle any database changes, roll back changes in the event of a problem, and greatly reduces the cost of changing the database when you inevitably need to do so. This can only be done if a single codebase manages the database layer, however.
  * Easily perform other shared data management operations, such as generating test data using the ORM. This test data will always use the same version of the schema intended for production use, since the code rigorously defines this through migrations.
  * It will be easier to scale your system (in complexity, number of services) with a shared ORM because it has some guarantees all uses of the database assumes the same schema. You don't have to worry about all database code being in agreement about the schema. Any inconsistencies in database logic will be less common, and caught earlier.

