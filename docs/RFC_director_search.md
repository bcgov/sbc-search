

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

## MonoRepo Pattern

Arguably, the `lear` repo already observes and is benfitting from the MonoRepo pattern. The suggestion is to continue to do this consciously so we can continue to benefit.

The request here is to merge `sbc-search` into the `lear` repo. In addition, to encourage more code sharing between API services (see "Shared model layer"). It may be advisable to consider merging other repositories such as `sbc-auth` in the future as well. The recommendation from this pattern is to have a strong bias towards reducing the number of managed repositories which have a substantial dependency between them. This doesn't mean using one repo for every single project, but rather to avoid fragmenting into too many small repositories.

A great deal of project structure convention, boilerplate and other non-domain code is costly to repeat and will be increasingly difficult to keep in-sync as the applicaton's complexity increases.

There is a powerful pattern available to teams, so long as their work is reasonably connected, to greatly simplify project administration, standardization, and dependency management - the MonoRepo pattern. This pattern is used by Google on its' core search product by thousands of team members, nullifying the main counter-argument that it doesn't scale.

Benefits:
  * Release management and dependency management are two of the most challenging parts of managing a software project. MonoRepo eliminates all internal release management and dependency management effort. This is, in most projects, the majority of all such management effort. Only a single release to external stakeholders needs to be managed.
  * All interacting components are constantly tested together by all teams during development, so issues are more likely to be found before a a later, dedicated test phase (later found bugs are always more costly).
  * It's much simpler to maintain standards across multiple teams' work, since linters and other quality configurations and conventions are automatically shared right in the monorepo.

Downsides:
  * Can encoruage unnecessary coupling between componenents.
  * It's harder for teams from being able to release without communicating and trusting one antoher. We rely on a coordinated agreement on stable branches in order to release. A simple convention to avoid this issue is to keep one branch always in a "releasable state" (as advocated for Continuous Deployment). Then, any team may test others' code integrated on this stable branch and cut a release.

