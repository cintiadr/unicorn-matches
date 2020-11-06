## Description

This code will receive a list of people as an input CSV file, 
and generate a list of possible zoom breakout rooms for speed dating events
based on preferences.  


The input file should have the following format:

```
Name, email, Imperfect Matches, [matching fields]
```

Email needs to be unique, and it's used as the main identifier for a person. 

Field `Imperfect Matches` should be either `true` or `false`. 
In case it's `true`, only perfect matches (100%) will become dates. 
Keeping it as `false` will return more dates. 


You can have as many matching fields as desired. 
The header of a matching field should have the name of the field and the percentage/weight (e.g. `Gender|100%`).
All fields combined should add up exactly 100%.  Only integers (from 1 to 100) are allowed. 

Each matching field has two sections: `I am` and `Looking for`, separated by a `@`. 
Multiple values are possible using within each section can use `|` as a separator. 

For example, assume I am a transfemme (`TF`) and non-binary person (`NB`) and I'm looking for non-binary people (`NB`) and men (`MN`). The field `Gender|100%` would be populated as `TF|NB@NB|MB`. 
Order within each section isn't important. 

The exact strings used to describe the matching field is not important to the system, but the idenfier on `I am` has to the exactly the same as `Looking for`. They shouldn't have `,`, `|` or `@`. 


So, an example file would be:

```
Name, Email, Imperfect Matches, Gender|100%
Person 1, person1@email.com, true, MN@WM|WM|NB|TM
Person 2, person2@email.com, true, WM@WM|NB|WM
Person 3, person3@email.com, true, TM@WM|MN
Person 4, person4@email.com, true, WM@WM|TM|NB
Person 5, person5@email.com, true, NB@NB|WM

```

A file that isn't properly formatted will cause exceptions from `read_input_file`. 


## Usage

You should pass as arguments the CSV file location and number of dates required. 

```
# python matches.py <file> <number of dates/rounds>

# e.g.
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

If you don't like the room names, go to `config.py` and change to whatever you prefer. 
Rerun the software and you should have all you need. 