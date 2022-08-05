# Job Hunting Visualization

A simple python script for visualizing the job hunting status using a sankey diagram, and compare salary ranges visually.  

The code that generates the sankey diagram is adapted from https://medium.com/kenlok/how-to-create-sankey-diagrams-from-dataframes-in-python-e221c1b4d6b0 

## Inputs

### Data File

A CVS file containing the stages of each application, e.g.:

```
Date, Step 1, Step 2, Step 3, Step 4, Step 5, Status
13/06/2022, Applied, Technical Interview, , , , Reproved
22/06/2022, Applied, , , , , Reproved
30/06/2022, Applied, , , , , ?
05/07/2022, Applied, Technical Interview, Coding Test, Behaviour Interview, , ?
```

_Note: The original file has more information, not relevant for this diagram, e.g:_ 
```
Date,Company,Position,Salary Range,Location,Remote,Ref/Site,Link,Step 1,Step 2,Step 3,Step 4,Step 5,Status
```

### Exchange Rates

A JSON file containing the exchange rates, e.g.:

```JSON
{
  "success": true, 
  "timestamp": 1659704825, 
  "base": "USD", 
  "date": "2022-08-05", 
  "rates": {
    "BRL": 5.240938, 
    "CAD": 1.29553
  }
}
```

This file is updated via API Call to https://apilayer.com/marketplace/exchangerates_data-api, so an API key is required.
This API key must be obtained from the website and stored in the text file `data/api_key.txt`. 

## Output 
 
Sankey diagrams to visualize the status of job applications or a bar chart to assess the salaries of job offers.
