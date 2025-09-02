# What-Can-We-Cook (ITIS-3300 Project)
Group information available in the [GROUP-INFO](./GROUP-INFO) file.

## Repository Structure
|-- `src/` - Source code for the project.  
|-- `documents/` - Documentation files and resources.  
|-- `reports/` - Reports and write-ups related to the project.  
|-- `summaries/` - Summaries of meetings, tasks, and progress.


### Installing necessary packages:  
* `pip install fastapi`
* `pip install "uvicorn[standard]"`  
* `pip install httpx`  
* `pip install firebase-admin`
* `pip install fastapi uvicorn pytest firebase-admin`

### Run the server:
`uvicorn api.main:app --reload`

### Test API by built-in docs:
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)