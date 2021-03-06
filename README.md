# Unicorn matcher


This is a python script that can be used to generate zoom breakout rooms CSV files 
for speed dating events based on preferences. 

Most configuration is added via a CSV file.

This application is still pretty rough around the corners, so it will mostly give bad error messages 
if the input is not expected. 

This might not be the _perfect_ dating set, but it's usually good enough. 
There's a little bit of randomness added, so running it multiple times might yield 
slightly different results.  


### Requirements


Ensure you have `python3` command available from your command line/terminal. 

Download the code from this repository and unzip it.  


### Invocation

You should pass as arguments the CSV file location and number of dates required. Input file defined below:



```
# python3 matches.py --file <input_file.csv> --min-rounds <minimum number of dates> --max-rounds <max number of dates>

# e.g.
# If you are on Mac or Linux:
python3 matches.py --file test-files/file-3.csv --min-dates 1 --max-rounds 2

# if you are on Windows:
py matches.py --file test-files/file-3.csv --min-dates 1 --max-rounds 2
```

The total number of dates will be between the minimum and maximum. 
The script will attempt to generate a number of dates that will allocate most high compatibility matches. 


### Input file


The input file is a CSV file should have the following format:

```
Name, Email, Minimum Compatibility, [matching fields]
```

For example:

```
Name, Email, Minimum Compatibilitys, Gender|100%
Person 1, person1@email.com, 100%, MN@WM|WM|NB|TM
Person 2, person2@email.com, 100%, WM@WM|NB|WM
Person 3, person3@email.com, 0%, TM@WM|MN
Person 4, person4@email.com, 100%, WM@WM|TM|NB
Person 5, person5@email.com, 0%, NB@NB|WM
```


Email needs to be unique, and it's used as the main identifier for a person. 
Failing to do that will lead to very unusual behaviour and it's not supported. 

Field `Minimum Compatibility` should be a percentage a person would allow in a date.  



### Matching fields

You can have as many matching fields as desired. 
The header of a matching field should have the name of the field and the percentage/weight this field
should have when calculating compatibility (e.g. `Gender|100%`) .
All fields combined should add up exactly 100%.  Only integers (from 1 to 100) are allowed. 

Each matching field has two sections: `I am` and `Looking for`, separated by a `@`. 
Multiple values are possible using within each section can use `|` as a separator. 

For example, assume I am a transfemme (`TF`) and non-binary person (`NB`) and I'm looking for non-binary people (`NB`) and men (`MN`). The field `Gender|100%` would be populated as `TF|NB@NB|MB`. 
Order within each section isn't important. 

The exact strings used to describe the matching field is not important, but the identifier `I am` side has to the exactly the same as `Looking for`. They shouldn't have `,`, `|` or `@`. 
It's strongly recommended to keep the strings short to avoid having long lines in the input file. 

It's highly recommend to choose a single field to the be the main one;
it should have a weight that is bigger than all other fields combined. 
This way dates with matches on the main matching field will be prioritised over other dates.   
Failing to do that will yield what looks like random results. 


### How dates are selected

First, the script attempts to discover all potential dates that can happen. 

Then it will separate dates between `high compatibility` and `low compatibility`. 
`High compatibility` is when both sides have prefered matches to _at least_ the main/biggest matching field. 

The system will start allocating `high compatibility` dates, 
ordered by people who had the least amount of dates (and dates for a person ordered by highest preferences compability). 
It will randomly select the rounds to allocated those dates. 

The system will move to `low compatibility` dates, ordered the same way. There will less logs for these dates. 

The system might not be able to allocate a date because the people are busy, 
the rounds is full or because there's an odd number of people. 


### Result files


Output files are created in `out` folder. 
Each run will have a subfolder with the a different timestamp

For each 'round', a file will be created:

```
Pre-assign Room Name,Email Address
red,person2@email.com
red,person5@email.com
orange,person1@email.com
orange,person4@email.com
```

If you don't like the room names, go to `config.py` and change to whatever you prefer. 
Rerun the software and you should have all you need. 