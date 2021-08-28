# JSON ARRAY FILE

Simple and memory-efficient JSON to file writer.

## USAGE

* context manager

```
with JsonArrayFileWriter('output.json', indent=4) as f:
    f.write_dict({"id": 1, "first_name": "Peter", "last_name": "Sveter", "age": 86, "height": "50 CM",
                  "grades": {"Math": "A", "History": "B+", "Programming": "F-"}})
    f.write_dict({"id": 2, "first_name": "Donald", "last_name": "Donaldson", "age": 9, "height": "150 CM",
                  "grades": {"Math": "C", "History": "B", "Programming": "A"}})
```

* object

```
# instantiate the writer

writer = JsonArrayFileWriter('output.json', indent=4)

# open the writer

writer.open()

# write entries

writer.write_dict({"id": 1, "first_name": "Peter", "last_name": "Sveter", "age": 86, "height": "50 CM",
                   "grades": {"Math": "A", "History": "B+", "Programming": "F-"}})
                   
writer.write_dict({"id": 2, "first_name": "Donald", "last_name": "Donaldson", "age": 9, "height": "150 CM",
                   "grades": {"Math": "C", "History": "B", "Programming": "A"}})

# close the writer

writer.close()
```

```
[
{
    "id": 1,
    "first_name": "Peter",
    "last_name": "Sveter",
    "age": 86,
    "height": "50 CM",
    "grades": {
        "Math": "A",
        "History": "B+",
        "Programming": "F-"
    }
},
{
    "id": 1,
    "first_name": "Peter",
    "last_name": "Sveter",
    "Age": 86,
    "Height": "50 CM",
    "Grades": {
        "Math": "A",
        "History": "B+",
        "Programming": "F-"
    }
}
]
```
