# ReaxFF_file_formatter
ReaxFF files are often provided as PDFs in papers. This script converts that to the standard format. It is based on [EZFF](https://github.com/arvk/EZFF), though simplified and updated. This script will likely not (often) be updated and is therefore not provided as packages but only as is.

## Usage
```ReaxFF_formatter``` takes either a path to a text file or the text as string. Copy the text from the PDF or other source into a text file and point the script to the file. Write it to a different file, or the same file to override it.
```python
from reaxff_formatter import ReaxFF_formatter

formatter = ReaxFF_formatter("in.txt")
formatter.write_formatted_forcefields("out.ff")
```
