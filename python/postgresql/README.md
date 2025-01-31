# Using Python with PostgreSQL

1. [TL;DR](#tldr)
1. [Further readings](#further-readings)

## TL;DR

Leverage the [Psycopg] module.

[Differences between Psycopg2 and Psycopg3].

<details>
  <summary>Setup</summary>

```sh
pip install 'psycopg2-binary'  # psycopg2
pip install 'psycopg[binary]'  # psycopg3
```

</details>

<details>
  <summary>Usage</summary>

1. Create a new database session by using `connect()`.
1. Create new cursor instances using `cursor()` to execute commands and queries.
1. Terminate transactions using `commit()` or `rollback()`.

  <details style="padding-left: 1em">
    <summary>Psycopg2</summary>

```py
import psycopg2

# Connect to existing Postgres DBs
conn = psycopg2.connect("dbname=test user=postgres")

# Perform database operations through Cursors
with conn.cursor() as cur:

    # Execute commands
    cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data text)")
    cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def"))
    cur.execute(
        """
        INSERT INTO some_table (an_int, a_date, another_date, a_string)
        VALUES (%(int)s, %(date)s, %(date)s, %(str)s);
        """,
        {'int': 10, 'str': "O'Reilly", 'date': datetime.date(2005, 11, 18)}
    )

    # Retrieve query results
    # Data is obtained as Python objects
    cur.execute("SELECT * FROM test")
    one_result = cur.fetchone()
    all_results = cur.fetchall()

    # Make changes to the DB persistent on demand
    conn.commit()
```

  </details>
  <details style="padding-left: 1em">
    <summary>Psycopg3</summary>

```py
import psycopg

# Connect to existing Postgres DBs
# When this block is exited, any open transaction will be committed
# If any exception is raised within the block, the transaction is rolled back
with psycopg.connect("dbname=test user=postgres") as conn:

    # Perform database operations through Cursors
    with conn.cursor() as cur:

        # Execute commands
        cur.execute(
            """
            CREATE TABLE test (
                id serial PRIMARY KEY,
                num integer,
                data text
            )
            """
        )
        cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def"))
        cur.execute(
            """
            INSERT INTO some_table (an_int, a_date, another_date, a_string)
            VALUES (%(int)s, %(date)s, %(date)s, %(str)s);
            """,
            {'int': 10, 'str': "O'Reilly", 'date': datetime.date(2005, 11, 18)}
        )

        # Load data from iterables
        with cur.copy("COPY test (num, data) FROM STDIN") as copy:
            for record in [(10, "hello"), (40, "world")]:
                copy.write_row(record)

        # Retrieve query results
        # Data is obtained as Python objects
        cur.execute("SELECT * FROM test")
        one_result = cur.fetchone()
        all_results = cur.fetchall()

        # Make changes to the DB persistent on demand
        conn.commit()
```

  </details>

</details>

## Further readings

- [Psycopg]
- [Psycopg2 documentation]
- [Psycopg3 documentation]
- [Differences between Psycopg2 and Psycopg3]

<!--
  Reference
  ═╬═Time══
  -->

<!-- Upstream -->
[differences between psycopg2 and psycopg3]: https://www.psycopg.org/psycopg3/docs/basic/from_pg2.html#from-psycopg2
[psycopg]: https://www.psycopg.org/
[psycopg2 documentation]: https://www.psycopg.org/docs/
[psycopg3 documentation]: https://www.psycopg.org/psycopg3/docs/
