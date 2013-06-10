Brevity. It's github+legos for lawyers.
#################

-----------------
------ API ------
-----------------

#########################

-----------------
----- MODEL -----
_________________
model.py
    Socket
    Node
    Document
    Amendment
    Agreement
    RandomDataGenerator
    SampleObjectFactory

Define and provide interface to data model. Ensure consistency.

------------------
------ VIEW ------
------------------
Web Presentation Layer
TEMPLATES

Construct view per controller's instructions. Display data using appropriate resources.

------------------
--- CONTROLLER ---
------------------
web_controller.py
    MainPage
    ViewPage
    EditPage
    CreatePage

CRUD data with Model. Tell view(s) what to display.

#################

-----------------
---- GAE::NDB ---- (MODEL)
-----------------

------------------
-- GAE::WEBAPP2 -- (CONTROLLER)
-----------------

---------------------
------JINJA2------- (VIEW)
-------------------
Desktop
Smartphone
:: iOS
:: Android
Tablet
;: iOS
:: Android

