## Usage

This silly python code will do a very basic match on preferences



It receives an smail CSV file as the input file, format:

```
Name, email, allows imperfect matches, identifies as, searching for
```

`identifies as` and `Searching for` can have multiple items, separated by '|'


`allows imperfect matches` should be either 'true' or 'false'


Arguments are: CSV file and maximum number of dates per person
```
python matches.py test-files/file-3.csv 2
```


Output files are created in `out` folder. 
For each 'round', a file will be created:

```
Pre-assign Room Name,Email Address
red,person2@email.com
red,person5@email.com
orange,person1@email.com
orange,person4@email.com

```
