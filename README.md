## The context

Curry Company is a technology company that has created an app connecting restaurants, delivery personnel, and customers. Through this app, it's possible to order a meal from any registered restaurant and have it delivered to your home by a registered delivery person. The company conducts business among restaurants, delivery personnel, and customers, generating a wealth of data on deliveries, types of orders, weather conditions, delivery ratings, etc. 

## Business Problem:

Despite growing in terms of deliveries, the CEO lacks complete visibility of the company's growth KPIs.
You have been hired as a Data Scientist to create data solutions for delivery. Before training algorithms, the company needs to have its key strategic KPIs organized in a single tool for the CEO to consult and make simple yet important decisions. Curry Company operates a business model called Marketplace, which intermediates between three main clients: restaurants, delivery personnel, and customers. To track the growth of these businesses, the CEO would like to see the following growth metrics:

**From the company's perspective:**

1. Number of orders per day.
2. Number of orders per week.
3. Distribution of orders by type of traffic.
4. Comparison of order volumes by city and traffic type.
5. Number of orders per delivery person per week.
6. Central location of each city by traffic type.

**From the delivery person's perspective:**

1. The youngest and oldest ages of delivery personnel.
2. The worst and best vehicle conditions.
3. The average rating per delivery person.
4. The average rating and standard deviation by traffic type.
5. The average rating and standard deviation by weather conditions.
6. The top 10 fastest delivery people per city.
7. The top 10 slowest delivery people per city.

**From the restaurant's perspective:**

1. The number of unique delivery personnel.
2. The average distance between restaurants and delivery locations.
3. The average and standard deviation of delivery times by city.
4. The average and standard deviation of delivery times by city and type of order.
5. The average and standard deviation of delivery times by city and traffic type.
6. The average delivery time during Festivals.

The goal of this project is to create a set of charts and/or tables that display these metrics in the best possible way for the CEO.

## Assumptions Made for the Analysis

The analysis was conducted with data from 02/11/2022 to 04/06/2022.
Marketplace was the assumed business model.
The three main business perspectives were:  orders view, restaurant view, and delivery personnel view.

## Solution Strategy

The strategic dashboard was developed using metrics that reflect the three main views of the company's business model:

- Company Growth View
- Restaurant Growth View
- Delivery Personnel Growth View
Each view is represented by the following set of metrics:

**Company Growth View**

a. Orders per day

b. Percentage of orders by traffic conditions

c. Number of orders by type and city

d. Orders per week

e. Number of orders by type of delivery

f. Number of orders by traffic conditions and city type

**Restaurant Growth View**

a. Number of unique orders

b. Average travel distance

c. Average delivery time during festivals and normal days

d. Standard deviation of delivery time during festivals and normal days

e. Average delivery time by city

f. Distribution of average delivery time by city

g. Average delivery time by type of order

**Delivery Personnel Growth View**

a. Age of the oldest and youngest delivery person

b. Rating of the best and worst vehicle

c. Average rating per delivery person

d. Average rating by traffic conditions

e. Average rating by weather conditions

f. Average time of the fastest delivery person

g. Average time of the fastest delivery person by city

## Top 3 Data Insights

**The seasonality of the number of orders is daily.**
There is a variation of approximately 10% in the number of orders on sequential days. 

**Semi-Urban type cities do not have low traffic conditions.**

**The greatest variations in delivery time occur during sunny weather.**

##  Final Product of the Project

An *online dashboard*, hosted on a Cloud, and accessible on any internet-connected device.
The dashboard can be accessed through this link: [Curry Company Dashboard](https://am-currycompanydash.streamlit.app/)

##  Conclusion

From the Company's perspective, we can conclude that the number of orders grew between weeks 6 and 13 of the year 2022.


##  Next Steps

- Reduce the number of metrics.
- Create new filters.
- Add new business views.
