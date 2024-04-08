# A.C.C.E.S.S.

## Automated Cataloging and Classification Engine for Storage and Search

### What is ACCESS?
ACCESS is a powerful software that automatically stores and classifies any type of data.

This project started as a personal hobby and is not yet intended for widespread use, however it is likely that a public version of ACCESS will be released in future

### What is the idea behind ACCESS?
The idea behind ACCESS is really simple: you provide a piece of data and it will automatically catalog this resource in a database. Whenever you ask ACCESS something, it will try to understand and give you the best answer.

### How can I use ACCESS?
> *At the moment ACCESS tags identifier algorithm need to be "trained", for this reason read [How to train ACCESS tags identifier algorithm](https://github.com/nicolacanzonieri/access#how-to-train-access-tags-identifier-algorithm) before reading this chapter*

Fill the `source.txt` file with a **Title** in the first row of the file and use the other rows to add the **Body** of your data.

Than run ACCESS and insert the command `learn`.

Now you can ask ACCESS about that data and it will show the **Title** and the **Body** of your data

### How to train ACCESS tags identifier algorithm
ACCESS use a complex algorithm to understeand the tags of a specific data, for this reason is important to update the **stop words database** regularly. You can do this by downloading the `stop_words_en.txt` everytime once in a while and placing it inside your `database` folder inside ACCESS, or you can train ACCESS with a **personal stop_words database**. To do this fill the `source.txt` file with the following pattern: use the first row of the file to place the **Title** of your data and than use the rows belows to add the **Body** of your data. 

Now run ACCESS and insert the `train tags` command and follow the instructions on screen.

Do this every time you want to update the stop words database!
