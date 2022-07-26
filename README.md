# Job Hunting Visualization

A simple python script for visualizing the job hunting status using a sankey diagram.

The code that generates the diagram is from https://medium.com/kenlok/how-to-create-sankey-diagrams-from-dataframes-in-python-e221c1b4d6b0 

## Input

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

## Output 

A sankey diagram to visualize the job applications stages.
