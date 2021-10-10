Using SoapUi opensource version there is no features to -
1. Archive the test results.
2. Analyze how the system is performing with respect to the previous builds.
3. Dashboard with graphical representation to show the performance of the system over time and Load.

Here is the solution which I came across to overcome this limitations.

* Since we know a .csv file is generated with the statistics when we run the load test from the command prompt.

>I used `Python` with `Pandas` to filter out the unwanted data and archive the results in the database by creating dataframes using `pymssql`.

* Now, I've my results archived in the database, I used the `Dash` and `plotly` to create the dashboard which can be host any server and accessible to the stakeholders.

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/htfnc90kb0pya7t9o4en.png)
  
[Link](https://dev.to/akshayca/soapui-load-test-reporting-dashboard-2mn2) to my Blog.




