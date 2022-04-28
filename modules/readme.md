# everything here is optional 
## except `__init__.py` 
### lol


***

you can delete anything you dont want, also add other modules from different developers

filenames starting with `__filename` will be ignored for loading

filenames starting with `_filename` are considered runnable background scripts, they will just run in bg when the bot starts

normal files with same-named-functions are modules you can use in chat, eg: .ping, .id etc (same filename, same function name)


***

the only files you need to get the bot up and running is 
- main.py
- modules/\_\_init\_\_.py

yes, thats it, 2 files

env vars stay on system, so .env is optional

requirements.txt is useless after installing them

also, requirements.txt is formatted with the modules and dependencies, so if you dont need a module...
just delete the module and its dependencies from requirements.txt