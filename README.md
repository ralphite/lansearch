# LAN Search
> Index and search files shared in the Local Area Network

----

## Features

1. Keyword searching
2. Wildcard matching
3. Regular Expressions!
4. Easy copy and paste


## Deployment

#### Get the Repository

Download and install [git](http://git-scm.com/). Open `git bash` and execute the
following command to get the repository.

> `git clone https://github.com/yadongwen/lansearch.git`

#### ElasticSearch

Download [ElasticSearch](http://www.elasticsearch.org/) and start an instance. To
start an instance, decompress the file and execute `bin/elasticsearch.bat`

#### Python Environment

Download and install [python2.7](https://www.python.org/downloads/),
[pip](https://pip.pypa.io/en/latest/installing.html) and 
[virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/).

In `git bash` go to the repository folder and create a Python virtual environment
with `virtualenv venv`, then activate it with `. venv/source/activate`. 

In venv execute `pip install -r requirements.txt` to download and install the dependencies.

`pywin32` is also required to run this app which cannot be installed automatically 
with `pip`. Please manually [download](http://sourceforge.net/projects/pywin32/files/pywin32/) 
and install it.

#### Crawl Data

`lansearch.py` provides a few commands for data crawling. Please refer to the 
command reference below.

```
$ python lansearch.py
usage: lansearch.py [-?]

                    {create_index,shell,drop_index,retrieve_shared_folder_list,
                    retrieve_machine_list,runserver,filter_shared_folders,test,
                    filter_machines,recreate_tables,crawl}
                    ...

positional arguments:
  {create_index,shell,drop_index,retrieve_shared_folder_list,
  retrieve_machine_list,runserver,filter_shared_folders,test,
  filter_machines,recreate_tables,crawl}
    create_index        create file index
    shell               Runs a Python shell inside Flask application context.
    drop_index          drop file index
    retrieve_shared_folder_list
                        retrieve list of shared folders and save to DB.
    retrieve_machine_list
                        retrieve machine list in the current domain. result
                        will be saved to machines table in data/machines.db
    runserver           Runs the Flask development server i.e. app.run()
    filter_shared_folders
    test                Run unit tests
    filter_machines
    recreate_tables     dangerous
    crawl               crawl list of shared files and push to ES.

optional arguments:
  -?, --help            show this help message and exit
```

#### Start App

Finally you may start **LAN Search** with `python lansearch.py runserver -h 0.0.0.0`.

Enjoy!
