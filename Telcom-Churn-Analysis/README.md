# Telecom Customer Churn & Revenue Risk Analysis

## Project Overview

Customer churn is one of the most important challenges facing subscription-based businesses. When customers leave, companies lose recurring revenue and incur additional costs to acquire new customers.

This project analyzes customer churn behavior for a telecommunications company to identify key drivers of churn, quantify revenue impact, and provide actionable recommendations to improve customer retention.

The analysis combines SQL-based data exploration with an interactive Power BI dashboard to support business decision-making.

---

## Business Problem

The telecom company experienced customer attrition that could negatively affect long-term revenue growth and profitability.

Management wanted to understand:

* Which customers are most likely to churn
* Which customer segments contribute most to churn
* How churn affects revenue
* What actions could reduce customer attrition

---

## Project Objectives

This project aimed to answer the following questions:

1. What is the overall churn rate?
2. Which customer groups churn most frequently?
3. Which services are associated with higher churn?
4. How much revenue is being lost due to churn?
5. What business actions can improve retention?

---

## Tools & Technologies

* SQL
* Power BI
* Microsoft Excel

---

## Dataset

Source: IBM Telco Customer Churn Dataset

The dataset contains customer demographic information, subscription details, service usage, billing information, and churn status.

Key fields analyzed include:

* Customer Tenure
* Contract Type
* Internet Service
* Payment Method
* Monthly Charges
* Total Charges
* Churn Status

---

## Methodology

### 1. Data Preparation

* Imported customer data into SQL
* Validated data quality
* Reviewed missing values and inconsistencies
* Prepared data for analysis

### 2. KPI Development

Key performance indicators were developed, including:

* Total Customers
* Churn Rate
* Monthly Revenue
* Revenue Lost from Churn
* Average Revenue Per User (ARPU)

### 3. Customer Segmentation

Customers were segmented based on:

* Contract Type
* Internet Service
* Payment Method
* Tenure Group

Tenure groups used:

* 0–12 Months
* 13–24 Months
* 25–48 Months
* 49+ Months

### 4. Dashboard Development

An interactive Power BI dashboard was created to visualize churn patterns, revenue risk, and customer segments.

### 5. Business Recommendations

Findings were translated into practical recommendations aimed at improving customer retention and reducing revenue loss.

---

## Dashboard

### Executive Overview

Provides a high-level summary of:

* Total Customers
* Churn Rate
* Monthly Revenue
* Revenue Lost
* ARPU

### Churn Analysis

Analyzes churn across:

* Contract Types
* Internet Services
* Payment Methods
* Customer Tenure Groups

### Revenue Risk Analysis

Highlights:

* Revenue Lost Due to Churn


### Recommendations

Presents business actions based on analytical findings.

---

## Key Findings

* Month-to-month customers exhibited significantly higher churn rates than customers with longer contracts.
* Most churn occurred during the first year of customer tenure.
* Certain payment methods showed higher churn concentrations.
* Fiber optic customers demonstrated elevated churn levels compared to other internet service groups.
* Customer churn represented a substantial loss of recurring monthly revenue.

---

## Business Recommendations

### Encourage Long-Term Contracts

Introduce incentives that encourage customers to move from month-to-month plans to longer-term contracts.

### Improve First-Year Customer Experience

Strengthen onboarding and customer engagement efforts during the first twelve months of service.

### Review Payment Experience

Investigate customer friction points related to payment methods associated with higher churn.

### Improve Service Retention Efforts

Conduct further analysis of service-related dissatisfaction among high-churn customer groups.

---

## Project Structure

Telecom-Churn-Analysis/

├── data/

│   ├── raw/

│   └── cleaned/

│

├── sql/

│   ├── data_cleaning.sql

│   ├── business_metrics.sql

│   └── customer_segmentation.sql

│

├── dashboard/

│   └── telecom_dashboard.pbix

│

├── documentation/

│   ├── business_requirements.md

│   └── user_stories.md

│

├── presentation/

│   └── telecom_churn_presentation.pptx

│

│

└── README.md

---



## Project Outcome

This project demonstrates the application of business analysis, SQL querying, KPI development, customer segmentation, and dashboard design to address a real-world customer retention problem.

The resulting analysis provides a data-driven foundation for improving customer retention and protecting recurring revenue.
