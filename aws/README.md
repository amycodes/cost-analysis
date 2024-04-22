# AUTOMATING YOUR CLOUD COST ANALYSIS

Let me introduce myself again. My name is Amy Arambulo Negrette and I’ve been an Application Developer for fifteen years. Today we’re going to talk about automating cloud cost analysis. We’re going to go into what it is, why it is important, and how to do it. 

##  Cloud Cost Analysis - Definition
So what is Cloud Cost Analysis? It also gets called FinOps or Cloud Economics, but whatever name you use, at the core it is the practice to understand how architecture derived from business and design decisions becomes money spent. Because all of the money we spend - or don’t - it’s the result of the things that we build. 

##  Programming Starts at Design

Programming starts at design. It always has. We all know what it looks like when you go hands to keyboard with only a vague idea of what it is you want to do.

It’s a mess.

So let’s connect the dots. I said everything starts at design, so we’ll start there. Just as an example, we’ll build an ETL. Real simple. We’ll need some kind of front-end, throw some computes in it to do the transformation, provision a database, and dump things in there. Perfect. 

Architecture and implementation is when we start putting hands to keyboard, provisioning our resources and checking in our code. 

And the spend is what we get at the beginning of the month in that list of receipts. Now we look at our bill, and say ‘ooph that doesn’t look right what can we do?’ then it’s back to the drawing board. We look at our design and start to optimize. Then we build. Then we get another bill. And on and on. That’s the Real Life Billing Cycle. 

##  Metrics

Now, monitoring and observability is very important but I truly believe you cannot just go looking for numbers. There are questions that you need to answer. They’re the same questions that we ask when trying to measure the performance of an application or its hardware. 

What is it doing? Is it taking too long? Are there drop offs? Those types of insights that are great for development. They also turn into costs or savings depending on how well you’re doing with it.

##  Cost as a Metric

Now to record cost as a metric, we need to know what we’re measuring, usually referring to a resource or a service. The usage of those resources and resources. The retail rate or how much we should be paying. And the amount charged or what we actually paid. Those are the numbers that will answer questions we will have later.

##  Cost as an Insight
Once we have our numbers, we can use our cost as an insight. We can see changes month over month and year over year. We can see services that had the most or least growth. Maybe we notice a service is handling more requests resulting in more spend, or track the progress of a cost optimization project or sunsetting of some resources. Or we can see if scaling broke pricing tiers. I’m a big proponent of serverless, but if you are using them at maximum thresholds all of the time, you may be better off shifting back to a cheaper VM. 

##  Building the Billing ETL
Now I built a lightweight example. For the purposes of this demo, I’ll be connecting to AWS using the PHP SDK and storing each grouping of results in MongoDB. Later we can write the reports to be more specific to the situation but for now this will save our invoices. 

##  DEMO
Here’s just a note that while we will be going over code, don’t worry about being able to read the text, all resources will be in the repository below and the slides are public. 

The ETL is built in two steps: Fetching the invoice and loading the database. 

## FETCH INVOICE
When fetching the invoice, you will have the option for Monthly, Daily, and Hourly granularity, a collection of cost and usage metrics, and the time period. For these sorts of reports, I suggest using the Daily option by month as well as grouping by service and usage type. Beyond that, you will be relying on annotated resources to get even more detail for your spend.

## FETCH INVOICE - RESULT
When the fetch is complete, you should get a list of results that include the time period, the Dimensions, in this case Service and usage Type, as well as our list of costs.

## Write to DB
Now what we want to do is bulk write all of the rows we received to our database. Here we’ll use the MongoDB client, select our database table, and insert our results. 

This particular result will print out the number of successful insertions s well as the IDs in case we wanted to pass them through a secondary validation. That result will read something like this.

## Next Steps!
As you’ll notice, this script was pretty short and lightweight. This works great as a deployed function that runs once a month. You can then use the database of invoice lines as a datasource for Excel and Tableau, though you’ll want to make sure your data is modeled in a way that’s specific to your particular use case. And finally, if you are running either multi-cloud or you have other services, you can normalize this data so you can compare how it’s performing or see a more high-level overview of what your spend looks like. 

##  Cloud Billing Options - AWS

As I said, this is running in AWS. I would use Lambda to fetch the CUR, load it into a database either like MongoDB or Aurora, and use those as a datasource for either Tableau or Quicksight.

##  Cloud Billing Options - GCP

If you’re using GCP, you can use a very similar build with BigQuery.

##  Cloud Billing Options - Azure

Finally, for Azure, you can run Power BI using their Power Platform and connect it with Azure DevOps. 

##  But Why?

Building an ETL like this answers a lot of questions, such as what would scaling look like? What would you need to improve. If you’re part of an enterprise organization, this information isn’t just useful but it’s required as part of any type of enterprise contracting. And if you’re part of a smaller organization, this is extremely useful data to have on hand when looking for funding. If you’re an IC, you may not exactly have access to this level of reporting, but knowing this is how spend is profiled should give you insight on what to look for and how to build more efficiently.

Just like any developer should care about the efficiencies of their application and their architecture, you absolutely should care about this.


##  THANKS
