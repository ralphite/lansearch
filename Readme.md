# LAN Search

Local Area Network Search for Windows shared files

### plan

- rich search language
    - multi field
    - AND OR
    - =
    - exact
    
- admin web UI
    - rich AJAX
    - detect machine and folders
    - scan folders with progress bar
    - update a single folder
    
- incremental crawl and update
- schedulers
- multi thread

### To do

- use manager script to manage
    - start/stop es
    - config es so that only local machine can access
    - drop prev index
    - create index
    - crawl folders
    - scan files
    - push data to ES
    - update ES with data change
    
- check if file already added to ES before adding
- `not_analyzed` search
- fix name to long bug (os.walk can do it)
- fix `check_machine_availability` (socket?)