#!python3.12

# Source: https://tomlkit.readthedocs.io/en/latest/quickstart/

from datetime import datetime, UTC
from tomlkit import (
    comment, dump, dumps, load, nl, table
)

# Get the contents of a file.
with open('input.toml', 'r') as i:
    toml_doc = load(i)

# Prove the content is saved in a tomlkit.toml_document.TOMLDocument object.
print(type(toml_doc))

# Add an empty line.
toml_doc.add(nl())

# Add comments.
toml_doc.add(comment("This enriches a TOML document."))

# Add key-value pairs.
toml_doc.add("another key", "another value")
toml_doc['yet-another-key'] = "yet another value"
toml_doc.append('appendedKey', 'appendedValue')
toml_doc.add('theAnswer', 42)

# Add objects.
owner = table()
owner.add("name", "Tom Preston-Werner")
owner.add("organization", "GitHub")
owner.add("bio", "GitHub Cofounder & CEO\nLikes tater tots and beer.")
owner.add("dob", datetime(1979, 5, 27, 7, 32, tzinfo=UTC))
owner["dob"].comment("First class dates? Why not?")
toml_doc.add("owner", owner)
database = table()
database["server"] = "192.168.1.1"
database["ports"] = [8001, 8001, 8002]
database["connection_max"] = 5000
database["enabled"] = True
toml_doc["database"] = database

# Print out the new content.
print(dumps(toml_doc))
with open('output.toml', 'w') as o:
    dump(toml_doc, o)
