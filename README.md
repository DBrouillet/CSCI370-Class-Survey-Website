Collaborative Feedback Site

Built for Dr. Sid Saleh, CSM Economics Dept.

Programming team: Sean Little, Daniel Brouillet, Wenxi Zhao

Site coded using Django version 2.2.7, running SQLite3 locally and PostgreSQL when deployed

Project Structure:
    -csmsaleh:
The csmsaleh directory contains all .py setup files. settings.py contains all relevant Django deploy and run settings. The urls.py file contains general site structure and interfaces with the evaulations/urls.py file. The wsgi.py file contains necessary project settings for host servers to read from when deployed.
    -evaluation:

        -migrations: This folder contains all historical changes to the database structure for Django to read from

        -static: The static folder contains all CSS stylesheets and background images for the evaluation site

        -templates: The templates for each page view within the evaluation site are stored here, in HTML format.

        -templatetags: The templatetags folder contains .py files adding custom templates for filtering evaluations by the logged-in user

        The evaluation folder contains all .py files used to generate site content that pertains to the database models

        Admin.py customizes options and views for the administration site.

        Apps.py contains a necessary config line for the evalution app. This file would contain more if adding sub-sites to the website

        Models.py contains the database structure in Django formatting. This file converts to either SQLite or PostgreSQL when launched on a server.

        Tests.py contains unit tests for back-end functionality. This was used only minimally when creating the site.

        Urls.py contains all url paths for the evaluation site tree.

        Views.py contains functions that control behavior when a user clicks a link or interacts with a particular page (view). This currently contains all functionality for saving to the database and loggin users out, as well as appropriate redirect links when functions run. 

    -Include: This folder is essential to the Django framework's operation, but should not be modified unless making changes to the Django codebase itself. If you find yourself here, something is probably seriously wrong.

    -Lib: The Lib folder contains default Django site behavior files. Look here if you're very curious about the way the Django default site behaves, but general wisdom holds that these files not be modified. 

    -Scripts: The Scripts folder contains files used to deploy virtual environments and format Python and PIP operations. These files should not be directly modified when coding

    -tcl: More Django behavioral code here, should not be modified when modifying site operations.

    -templates: The templates folder contains general site templates, such as the login page for users and the general base sites that other templates extend from. Change these in order to change the default site look. 

    The .env file contains a variable used by Django locally to point the site at the local SQLite database. This file is ignored by Git as live deployment should not be using SQLite installs. 

    The .gitignore file should be modified as needed when adding project files to keep from including binary files or files that are dynamically generated when deploying the site. Currently, the .gitignore does not ignore the db.sqlite3 file, which is a mistake we made when creating the site (it would be prudent to fix this before working on the site). 

    The db.sqlite3 file is modified every time the site deploys and changes are made to the database. This should never be directly modified by the programmer and contains binary not generally readable by IDEs.

    The Procfile points the Heroku deploy at the gunicorn install and the wsgi.py file in the csmsaleh folder in order to link the Django install to a hosting server deployment. 

    The requirements.txt file contains all necessary packages for running the site. Be sure to install all packages in this file before attempting to deploy, or errors will occur.



If you're reading this, there's a very good chance you're a CSCI370 student that's working on expanding this project. If so, good luck! Here's some thoughts that we've compiled to try to guide you on your way:

General Recommendations:

READ THE DJANGO TUTORIAL! Not only was it a good introduction to Django, it's quite literally the setup to this project. We created this by starting at the tutorial and expanding and modifying it from there because the built-in stuff was almost exactly what we needed. Look up video tutorials about it - you're going to learn more faster on Youtube than you will by poking around the code yourself.

Familiarize yourself with evaluation/models.py and evaluation/admin.py, as those two files dictate the database structure and contain a lot of what creates things on the admin side of the site, respectively. Understanding those files will be an excellent starting point

Create a virtual environment before making modifications to packages or files, and before deploying. This tends to save on headaches due to extra packages being installed on the local machine when attempting to run

Do not attempt to use SQLite for anything but local test deployments. Most hosting services do not support SQLite, and Django's built-in SQLite database is not intended for any sustained load or usage. 

SQLite interacts very poorly with git, it might be worthwhile to exclude it from git and have it get recreated on your local machines each time.

Areas of Caution and General Notes:

The detail.html file in evaluation/templates/evaluation uses forms that are not linked up to a forms.py file and are hardcoded. This turned out to be inflexible for later additions to the codebase, but was discovered late into development time.

In settings.py, a couple of password validators have been commented out in order to satisfy Dr. Saleh's request for easier logins. This enables passwords to be entirely numeric and the same as the username for any user.

The Mines logo banner found in base_site.html and login.html doesn't scale appropriately to mobile views, which we were unable to fix during our time developing the site. 

The submitAnswers function in evaluation/views.py uses a rather hacky method of iterating through the question sets, due in large part to the lack of generated forms. We highly recommend implementing a forms.py file and dynamically generating forms instead of hardcoding them if possible. 


Best of luck coding, and apologies in advance for our slightly hacky methods used while learning the Django framework
