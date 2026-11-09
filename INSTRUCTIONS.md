# Git Commands

## To Push your changes:

1) `git add .`
2) `git commit -m "message"` 
3) `git push `

- The 'git add .' command adds all files that have been modified to your "stage". This makes them ready to be pushed when you do git push ( Think of it as a container that got filled with your files ready to be shipped across the sea ).

- However, if for whatever reason you don't want to push a file yet, you can add individual files to the stage by doing 'git add {filename}' instead. 

- TIP: Feel free to write something funny in commit messages, we are not writing enterprise level software.
However, it should give some kind of idea as to what change was made.

## To Pull changes:

1) `git pull`
- yeah that's it

# Virtual Environment (venv)

Most code we write requires libaries and packages that don't come with python by default.

These have to be installed with pip ( or any other package manager )

Installing packages globally can cause version conflicts if you are working on many projects at once.

It is better to create a virtual environment per project.

This isolates every project's requirements. venv folders are NEVER pushed to github, as they are large in size.

You will create your own.

## Steps

1) Open a terminal in the root of the project directory.
2) Run `python -m venv venv`

This will create a venv folder.
All the libraries we install will be listed in the requirements.txt file.

To install those for yourself so the project runs on your machine, run these commands:

1) `.\venv\Scripts\activate`
2) `pip install -r requirements.txt`

- TIP: In your terminal, simply type venv, Then hit the TAB key, then type S and hit the TAB key, Then type a and hit the TAB key. This will autofill the command for you making it far easier to type.

That will do it.

Whenever you wish to run code, always activate the venv first, by doing the earlier mentioned command:

`source venv/Scripts/Activate`

