# uppsalaBibliotekTvSpelScraper

> A scraper that identifies when new games are added to the library and emails that list to a list of email addresses.

*I enjoy videogames, but I hanker for the old days when I didn't need to take out a mortgage just to afford a disc that inevitably pesters me to buy new skins and DLC anyway. Luckily, our local library keeps a stock of games, including newly-released titles. Unluckily, it usually only has one or two of each title, and I am not the only visitor to the library who doesn't like paying for games. With the help of this scraper, **I am now at the front of the queue** each time a new game comes into stock!*

#### Can be set to track any media type (i.e., books, games, CDs, etc) using the appropriate web address.

The script outputs the list of titles to a text file named `Library.txt`. It then compares the data with the previous
version and emails the changes to a list of users specified in the `contacts.txt` file.

This project uses chromedriver as the web driver, but any other browser (i.e., firefox) will work with some appropriate
changes in the code. See **1.3** at this link for information about choosing and setting up the web driver:*
`https://selenium-python.readthedocs.io/installation.html`

#### Usage

* Specify a loading interval between pagination with the following argument: `-T`, `--time` + integer
  * e.g: `$ ./sendemails.py -T 5` to use a 5-second wait period.
* Development mode can be enabled to give the opportunity to end the scrape prematurely: `-D`, `--dev`
  * e.g: `$ ./sendemails.py -D`
* You can provide an alternative link to scrape. **The link must be enclosed in double quotes**. Naturally, this will
  only work with Uppsala Bibliotek links: `-L`, `--link` + "string"
  * e.g: `$ ./sendemails.py -L "https://anotherlink.com"`

###### Current todos and problems include:

- [x] Doesn't differentiate between removed titles and added titles. User is emailed about a 'new title' even if the
  title in question has actually been removed from the library
- [x] ~~Web address is hard-coded and should be extrapolated to make the script more flexible~~
- [x] Credentials are not stored securely - could be read directly from the *macOS Keychain* instead
- [x] Need to research how best to normally add a project to GitHub that uses private credentials
- [x] ~~Need to add a secondary alert email if no new changes at the library were detected~~
- [x] ~~Time-limit is currently hard-coded as 10 seconds - this could be lowered if you have a fast and stable internet
  connection. Could be provided as an argument in the command line~~
- [ ] Need to talk to Marc about how best to break apart a script like this: it's a long script, but also a very
  specific script
- [ ] Want to add tests for different scenarios - content added, content removed, content renamed, etc…
- [ ] Break out code into separate functions to allow easier testing: **Ask Marc for help in identifying what to break
  out or not**
  - [ ] Compare two files
