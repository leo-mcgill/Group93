[33mcommit 71786e59808240714e619effc79b4d1869e16fe1[m[33m ([m[1;36mHEAD[m[33m -> [m[1;32mmain[m[33m, [m[1;31morigin/seperate_view_ui_and_stylesheets[m[33m, [m[1;32mseperate_view_ui_and_stylesheets[m[33m)[m
Author: Dex <lebicahl@gmail.com>
Date:   Thu Apr 10 19:48:35 2025 +0800

    Adding UI to each view. Adding seperate stylesheets for each view.

[33mcommit ea85225cc05303e1a2134e457e4f603e3fa92b12[m[33m ([m[1;31morigin/main[m[33m, [m[1;31morigin/HEAD[m[33m)[m
Author: leo-mcgill <168700366+leo-mcgill@users.noreply.github.com>
Date:   Thu Apr 10 13:10:20 2025 +0800

    Delete venv directory
    
    Deleted venv directory

[33mcommit df341939d21f28062ae3d0338a0ef3765bde7a42[m
Author: leo-mcgill <leomcgill1@icloud.com>
Date:   Thu Apr 10 13:04:40 2025 +0800

    deleted my venv my pycache and my instance

[33mcommit 8e6b140236a90f80d90c9556984de456a572e4e6[m
Author: leo-mcgill <leomcgill1@icloud.com>
Date:   Thu Apr 10 12:54:56 2025 +0800

    removed my venv from main. hopefully .gitignore works

[33mcommit 51350a720dd9ea438ff3ec4ec370262cea244d13[m
Merge: f8ae329 c25d26b
Author: leo-mcgill <168700366+leo-mcgill@users.noreply.github.com>
Date:   Thu Apr 10 12:51:43 2025 +0800

    Merge pull request #6 from leo-mcgill/DB_scripts
    
    Created scripts for DB. Added signup/login page.

[33mcommit c25d26b874247d522de6e9f4b48f47d2501d4acc[m[33m ([m[1;31morigin/DB_scripts[m[33m)[m
Author: leo-mcgill <leomcgill1@icloud.com>
Date:   Thu Apr 10 12:49:19 2025 +0800

    Created scripts to initialise, clear, and populate the DB. Added a signup/login page

[33mcommit f8ae3294f45048a65937e6a2a382e7a2f0f62219[m
Merge: 49cf83e 77f0f21
Author: leo-mcgill <168700366+leo-mcgill@users.noreply.github.com>
Date:   Thu Apr 10 11:51:51 2025 +0800

    Merge pull request #4 from leo-mcgill/creating_login_signup_page
    
    login/signup template and routes. Also made base.html

[33mcommit 77f0f216f0ebdfc322f81fd1a5f9dcf01c2379e4[m[33m ([m[1;31morigin/creating_login_signup_page[m[33m)[m
Author: leo-mcgill <leomcgill1@icloud.com>
Date:   Thu Apr 10 11:49:42 2025 +0800

    Created base.html that only contains navbar, all other templates extend from base.html to prevent us from rewriting navbar code for every template. Added some login/signup routes in app.py and also a login/signup page (currently non-functional as DB is not initialised yet). Will get DB up and running so we can add users and add movies

[33mcommit 49cf83ec509de5415fc0731fc6d3e3691c8937d6[m
Author: leo-mcgill <leomcgill1@icloud.com>
Date:   Wed Apr 9 18:54:17 2025 +0800

    Added some more info to README.md and some more requirements

[33mcommit 1acc021dc007fef10aef2bfadb05b7202d1d7e3c[m
Merge: 6b07b5c 4c84d12
Author: leo-mcgill <168700366+leo-mcgill@users.noreply.github.com>
Date:   Wed Apr 9 17:55:26 2025 +0800

    Merge pull request #3 from leo-mcgill/py_models
    
    Basic db models created

[33mcommit 4c84d12d49b3bc4d5dca92f18b8f897456bc54f5[m[33m ([m[1;31morigin/py_models[m[33m)[m
Author: leo-mcgill <leomcgill1@icloud.com>
Date:   Wed Apr 9 17:54:16 2025 +0800

    created two tables, one for a user and one for movies. passwords in user table are hashed as per usual

[33mcommit 6b07b5c9a25ad2040761cc0616a8197ef85fef0a[m
Merge: 29c5021 b3199b1
Author: leo-mcgill <168700366+leo-mcgill@users.noreply.github.com>
Date:   Wed Apr 9 17:31:09 2025 +0800

    Merge pull request #2 from leo-mcgill/upload_data_html
    
    Simple upload movie form (No functionality yet)

[33mcommit b3199b13e0efad33652b526b097a38b9ce0dcfc0[m[33m ([m[1;31morigin/upload_data_html[m[33m)[m
Author: leo-mcgill <leomcgill1@icloud.com>
Date:   Wed Apr 9 17:22:12 2025 +0800

    added simple form for movie upload and a temporary rating system. Would like to have a star rating system where users can click on stars to give a rating instead of a text box. Not necessary right now though.

[33mcommit 29c5021ba9739e1d0aa11b6151341799c20ba7e0[m
Author: leo-mcgill <leomcgill1@icloud.com>
Date:   Wed Apr 9 15:47:08 2025 +0800

    Created a Flask file structure. All html pages must go into /templates and all js or css must go into /static. Also created app.py to run the flask appliation and defined some routes within app.py. Made some changes to README.md to give some intsruction on how to run the Flask application.

[33mcommit 0b70cfc728cf869525427f638e39a1ae949e1524[m
Merge: f02f194 9df5563
Author: leo-mcgill <168700366+leo-mcgill@users.noreply.github.com>
Date:   Tue Apr 8 14:19:36 2025 +0800

    Merge pull request #1 from leo-mcgill/introductory_view_ui
    
    Introductory view UI

[33mcommit 9df55631c4ece594d87c0c5fbcc4951d899848a1[m[33m ([m[1;31morigin/introductory_view_ui[m[33m)[m
Author: Dex <lebicahl@gmail.com>
Date:   Tue Apr 8 12:40:55 2025 +0800

    adding comments to introductory view and updating link to css style sheet

[33mcommit a7ac020f4e5922c701eb5fbb057a75a4d5386dcc[m
Author: Dex <lebicahl@gmail.com>
Date:   Tue Apr 8 12:38:44 2025 +0800

    moving css files to folder named css_styles

[33mcommit 5cc32ca6622f3af5607bd730d6280d6a5492119f[m
Author: Dex <lebicahl@gmail.com>
Date:   Tue Apr 8 12:36:36 2025 +0800

    created simple UI for introductory view

[33mcommit f02f194c24bedcff3f155b28f44f3d526a8413fe[m
Author: leo-mcgill <168700366+leo-mcgill@users.noreply.github.com>
Date:   Wed Apr 2 15:57:12 2025 +0800

    Initial commit
