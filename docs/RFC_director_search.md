

# RFC: BCROS Search Architecture

## Goals


  * Consider PostgreSQL ts_vector for text search in general.


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


## Sharing Vue Components

The monorepo pattern should facilitate this, but it still presents some level of packaging challenge to share components between separate front-end builds because NPM isnt aware of files outside the root directory it runs within, paricularly when containerized. One solution is to consolidate the front-end into a single, common subtree of `lear`
