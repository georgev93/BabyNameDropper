# Baby Names

What a pain. I say I like a name, then my wife says she hates that name. I
think she's just mad because I said I didn't like a name that she liked...
We've been through like... a thousand names! There has to be a better way!

The baby name workflow in this repo looks like this:

1. Use the BabyNameDropper script to enumerate a "voting sheet". Call it with
   `python BabyNameDropper.py --sex M` or `python BabyNameDropper.py --sex F`
depending on the sex of your baby. You can add `--limit 1000` to limit the list
to the 1000 most popular names (or any number you choose). If you omit the
limit option, it will give you a list of every name that was used more than 5
times during the most recent year of data (probably in the tens of thousands of
names!)
2. The script will reach out to the Social Security Administration's website
and pull down a list of names. It can be limited by the `--limit XXXX` option
passed into the script as described in the previous step. It will pull from the
most recent year of data that the SSA has to offer. It will spit out a
`namelist.csv` file.
3. Both parents get a copy of the namelist.csv file. Name it something
different. Like "Dave.csv" and "Sam.csv".
4. Both parents should **independently** mark up their respective spreadsheets
by placing a character (any character, like `x`) in the **3rd** column of a row
(the "yes" column) if they really like the name in that row. Alternatively,
they can mark a character (any character) in the **2nd** column of that row
(the "maybe" column) of that row if they would consider the name, but they're
not in love with it. This can be done from the comfort of their favorite
device, potentially by treating the csv as a spreadsheet in Google Sheets and
marking it up from their phone while on an beach in Australia. See the
[below section](#filling-out-the-voting-sheet) on how to fill out this "voting
sheet".
5. Once both parents have filled out their respective voting sheets, you can
"score" them by using the `BabyNameVoteMerger.py` script like so: `python
BabyNameVoteMerger.py sam.csv dave.csv`. If the files are not in the current
directory, feel free to use absolute file paths
(`C:\\Users\\Bob\\Documents\\mySheet.csv`) or relative file paths
(`./someDirectory/subDirectory/mySheet.csv`). This will print out a "Merge" (or
"scoring") of the two voting sheets. See the
[below section](#interpreting-the-results) on interpreting the results.
6. Name that baby. Don't tell anyone that name. As a wise couple told my wife
and I on our Australian baby-moon vacation: "It's always a great idea not to
tell anyone your baby name before the baby is born. If you do tell someone
before the baby is born, they'll tell you all the reasons why you shouldn't
like that name and ruin it for you. If the same person hears that name after
the baby is born, they just say 'What a nice name!'"

## Invoking the Script

From a command prompt (CMD or Powershell on Windows) or your favorite terminal
emulator on any other OS (I use Arch, btw), you can use `python [NAME OF
SCRIPT] ...` to invoke the script (the `...` are arguments you pass to the
script such as filenames or optional arguments). However, you need
[python](https://python.org) installed to do that.

## Filling Out the Voting Sheet

Open up the *.csv file in your favorite spreadsheet editor (Excel, Google
Sheets, LibreOffice Calc, etc.).

The voting sheet will look like this:

| Name | Maybe | Yes |
|------|-------|-----|
|Elijah|       |     |
|James |       |     |
|Liam  |       |     |
|Noah  |       |     |
|Oliver|       |     |

For instance, if you wanted to mark that you like the names Oliver and Liam,
you'd consider the name Noah, but you don't like the names James or Elijah,
fill out the table like so:

| Name | Maybe | Yes |
|------|-------|-----|
|Elijah|       |     |
|James |       |     |
|Liam  |       |  x  |
|Noah  |   x   |     |
|Oliver|       |  x  |

You can literally type the letter `x` into the cell, or any letter/character
you like. `A`, `b`, `8`, `.`, etc.

Lastly **BE SURE TO SAVE THE FILE AS A CSV**. Not some fancy newer spreadsheet
format, as the other script in this repo won't be able to process it

## Interpreting the Results

Consider the following example.

`example/dave.csv`:

| Name | Maybe | Yes |
|------|-------|-----|
|Elijah|       |  x  |
|James |       |  x  |
|Liam  |   x   |     |
|Noah  |   x   |     |
|Oliver|       |  x  |

`example/sam.csv`

| Name | Maybe | Yes |
|------|-------|-----|
|Elijah|       |  x  |
|James |       |     |
|Liam  |       |  x  |
|Noah  |   x   |     |
|Oliver|   x   |     |

The voting results would be:

```
❯ python ./src/BabyNameVoteMerger.py example/sam.csv example/dave.csv                                                                                                                                     ─╯
============================
        BOTH LIKED:

Elijah

============================
     TO BE CONSIDERED:

       sam (BOTH MAYBE) dave
Liam    X
Noah            X
Oliver                   X
```

Note that the name "James" wasn't considered because `sam` did not categorize
this as a "Yes" or "Maybe," implying that this name is not one that she would
consider
