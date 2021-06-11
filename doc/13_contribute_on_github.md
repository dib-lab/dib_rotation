# How to edit the lessons in this webpage:

Edit these lessons on [GitHub](https://github.com/dib-lab/dib_rotation)

If you can't fix an error or make an addition right now, file an issue with the doc that needs changing. Each doc (shows up as a tab or page on the website) is stored as a `.md` document within the `doc` folder.

### Creating a pull request:
+ `git clone https://github.com/dib-lab/dib_rotation.git` to clone the repo on to you computer
+ from inside that repo, make yourself a branch to work on: `git checkout -b my-awesome-branch`
+ make some changes in the markdown on your branch 
    + `git add changed_file.md` for each file you change
    + `git commit` to save changes
+ When you're satisfied with your changes, open a pull request to integrate these changes into the main branch:
    + `git push --set-upstream origin my-awesome-branch`
    + `git push` to upload updated files (all changes up to last commit)
    + when you open GitHub again in a browser, it will prompt you to open a pull request
        + if you are correcting a filed issue, its helpful to tag the issue number in the pull request (eg `fixes issue #1234`)
    + When integrated, your changes will automatically render on the training website.
    

### Add a new page (markdown document):
+ put the `.md` file in the `doc` folder
+ add the title and file name to `mkdocs.yml` 
    + under the `nav` section, formatted with the name and title like the other docs are
    + this allows a tab to render for your doc in the side bar on the webpage
    + place it in the list in the place you want it to appear on the webpage

### View the updated rendered website locally:
+ make a conda env 
    + `mamba create -n mkdocs mkdocs`  
        + if you dont have mamba, use `conda create -n mkdocs mkdocs`
    +  activate that environment: `conda activate mkdocs`
    + `pip install mkdocs-material` to install the "material" theme
+ `cd` to the repo (`dib-rotation-project`, or wherever `mkdocs.yml` is sitting) 
+ build the docs into a website: `mkdocs build`
+ serves the site to a local webserver: `mkdocs serve`
+ a browser window might open automatically, 
    + this may not work if you are using `wsl`
    + the address should also be visible on the terminal output if you need to input it manually.
        + the URL is short, looks something like `http://123.0.0.1:4000/`


