## Usage

This silly python code will do a very basic match on preferences



It receives an smail CSV file as the input file, format:

```
Name, email, identifies as, searching for,allows imperfect matches
```

`Searching for` can have multiple items, separated by '|'
`allows imperfect matches` should be either 'true' or 'false'


Arguments are: CSV file and maximum number of dates per person
```
./matches.py test-files/file-3.csv 2
```
