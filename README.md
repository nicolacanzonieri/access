# ACCESS
## Automated Cataloging and Classification Engine for Storage and Search

> [!NOTE]
> ACCESS is not yet intended for widespread use. Its code is rough and not always precise. Please follow the `develop` branch for a better
> version of ACCESS (still a work in progress).

ACCESS is a tool that autonomously catalogs and classifies any type of txt file. To achieve this, ACCESS uses a dictionary of non-tag words (see `stop_words.txt`) and analyzes the document, adding the data to a local database.

Once the file is saved, ACCESS can retrieve the data by simply analyzing the user's prompt.

There are functions inside ACCESS that will help you use this software:
 - help
> Returns the list of ACCESS functions
 - learn
> Adds the `source.txt` to the database
 - train tags
> Displays the respective list of tags from a source in `source.txt` and allows you to edit it by selecting non-tag words one by one.
 - quick train tags
> Displays the respective list of tags from a source in `source.txt` and allows you to edit it by selecting multiple non-tag words at once.
