## Description

This code will receive a list of people as an input CSV file, 
and generate a list of possible zoom breakout rooms for speed dating events
based on preferences.  


The input file should have the following format:

```
Name, email, Allows Imperfect Matches, identifies as, searching for
```

So, an example file would be:

```
Name, Email, Allows Imperfect Matches, identifies as, searching for
Person 1, person1@email.com, false, MN,WM|WM|NB|TM
Person 2, person2@email.com, false, WM,WM|NB|WM
Person 3, person3@email.com, false, TM,WM|MN
Person 4, person4@email.com, false, WM,WM|TM|NB
Person 5, person5@email.com, false, NB,NB|WM

```

Field `Allows Imperfect Matches` should be either `true` or `false`. 
In case it's `true`, only perfect matches will become dates. 
Keeping it as `false` will return more dates. 


Fields `identifies as` and `Searching for` can have multiple items, separated by '|'



## Usage


You should pass as arguments the CSV file and number of dates required. 

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
