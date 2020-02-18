- Start Date: 2020-01-31
- Target Major Version:
- Reference Issues: 
- Implementation PR: pending

# Summary

This RFC was developed as part of the Director Search. Underlying goals include:
  * Allows re-use of search components for other search functions (assets / ppr?)
  * Promotes a scalable and robust BCROS.
  * Effectively manage technial debt, keep the codebase simple for new developers to onboard, and to make it easier to developers to avoid certain classes of bugs in the future where possible.

The SQLAlchemy ORM is not currently in use by CPRD clients (repos include sbc-auth, lear, entity), which are instead using raw SQL and have implemented partial ORM-like data service classes.

This leads to verbose, complicated code wich is not reusable, just to perform simple queries. The lack of reuse of the model layer will encourage drifting components that do note
respect the interface imposed by the data layer.

Other Registries codebases use the SQLAlchemy ORM already, such as sbc-auth, for a different database (postgres)

# Basic example

Current example:
```
class Address:  # pylint: disable=too-many-instance-attributes; need all these fields
    """Class to contain all model-like functions such as getting and setting from database."""

    province = None
    country = None
    ...

    def __init__(self):
        """Initialize with all values None."""

    def as_dict(self):
        """Return dict version of self."""
        return {
            ...
        }

    @classmethod
    def get_by_address_id(cls, address_id: str = None):
        """Return single address associated with given addr_id."""
        if not address_id:
            return None

        try:
            cursor = DB.connection.cursor()
            cursor.execute("""
                select addr_id, addr_line_1, addr_line_2, addr_line_3, city, province, COUNTRY_TYPE.full_desc,
                postal_cd, delivery_instructions
                from ADDRESS
                join COUNTRY_TYPE on ADDRESS.country_typ_cd = COUNTRY_TYPE.country_typ_cd
                where addr_id=:address_id
                """,
                           address_id=address_id
                           )

            address = cursor.fetchone()
            address = dict(zip([x[0].lower() for x in cursor.description], address))
            address_obj = cls._build_address_obj(address)
            return address_obj

        except Exception as err:
            current_app.logger.error(err.with_traceback(None))
            raise AddressNotFoundException(address_id=address_id)

    @classmethod
    def create_new_address(cls, cursor, address_info: dict = None):
        ...
            cursor.execute("""
                            INSERT INTO address (addr_id, province, country_typ_cd, postal_cd, addr_line_1, addr_line_2,
                             city, delivery_instructions)
                            VALUES (:addr_id, :province, :country_typ_cd, :postal_cd, :addr_line_1, :addr_line_2, :city,
                                :delivery_instructions)
                            """,
```

Suggested:
```

class Address(db.Model):
    __tablename__ = "ADDRESS"
    addr_id = db.Column(db.Integer, primary_key=True)
    province = db.Column(db.String(2))
    country_typ_cd = db.Column(db.String(2))
    COUNTRY = relationship("Country", backref="addresses")
    ...

class AddressSchema(Schema):
    province = fields.String()
    country = fields.Nested(CountrySchema())

```

# Motivation

Currently, a custom ORM-like system of custom classes is implemented. This follows typical model naming conventions, class methods for data services, and instances-as-rows pattern. However, this fails to leverage the most important benefits of using an ORM.
  * Standardized implementation using SQLAlchemy's ORM would make onboarding new devs easier, and avoid mistakes due to not understanding a home-baked solution. There is a large developer pool of expertise that can be leveraged close to the domain problem. Granted, SQL expertise does exist, but the expertise to use SQL from code is rare and requires extra effort.
  * Code is portable directly to PostgreSQL when moving off Oracle, for "free". No rewriting SQL.
  * Rely on expert ORM developers to generate correct, optimized SQL. Writing your own ORM is like writing assembly instead of C. There may occasionally be reason to, but in most cases it's costly and unnecessary.
  * Many of the concerns with connecting to a database are handled automatically, such as error handling, transaction management, sanitization. It's easy to miss these things, and unnecessary to develop them from scratch.
  * The models can be re-used in other projects, and for other purposes since a generic interface is generated.
  * The existing code is already using SQLAlchemy, but not leveraging most of the benefits of this powerful library, since it's only being used to query via undifferentiated SQL directly. Using an the SQLAlchemy ORM wouldn't require any new libraries on its own.


# Detailed design

Currently legal-api and colin-api each have their own custom database interface built from scratch, for the same database

Several of the benefits of an ORM rely on linking a given version of the code to a given version of the database, allowing designers to abstract away the database consistently in different contexts, manage migrations. This means sharing the model classes between different codebases that use the same database. Benefits:
  * Define a common database interface that can be tested in isolation, and test coverage can be reused.
  * Manage migrations automatically in the codebase. Even if migrations are rare, this allows the codebase to robustly handle any database changes, roll back changes in the event of a problem, and greatly reduces the cost of changing the database when you inevitably need to do so. This can only be done if a single codebase manages the database layer, however.
  * Easily perform other shared data management operations, such as generating test data using the ORM. This test data will always use the same version of the schema intended for production use, since the code rigorously defines this through migrations.
  * It will be easier to scale your system (in complexity, number of services) with a shared ORM because it has some guarantees all uses of the database assumes the same schema. You don't have to worry about all database code being in agreement about the schema. Any inconsistencies in database logic will be less common, and caught earlier.


# Drawbacks

"Like any powerful tool, it can rip your arm off, or make life easier and tasks can be completed faster and more efficiently." --entities feature flags RFC :)

Counter-arguments. This highly-voted SO answer lists Pros and Cons. https://stackoverflow.com/questions/1279613/what-is-an-orm-how-does-it-work-and-how-should-i-use-one

It comes down to whether you want to add an abstraction layer. However, in this use case I propose an ORM is a net win overall.

# Alternatives

## Use another ORM
PeeWee is an example of another Python ORM.

## Do nothing
Just keep using SQL directly.

## Not doing this
Deploying features would require more extensive SCM branch management, more advanced deployment / rollback and canary testing environments.

# Adoption strategy

For director search: We are using the ORM right away.
For other code: Perhaps during PostgreSQL port since some DB code will need touched anyway.

# Unresolved questions

1. Is there a good reason the existing CPRD interface is done without an ORM?
1. Will SQLAlchemy's ORM work seamlessly with CPRD? We have only tried Postgres as a test database.

# Thanks

This template is heavily based on the Vue, Golang, React, and other RFC templates. Thanks to those groups for allowing us to stand on their shoulders.
