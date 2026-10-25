# 🛒 E-Commerce Product & User Behavior Analytics

An end-to-end data analytics project focused on understanding e-commerce sales, product performance, customer behavior, conversion funnels, retention, and A/B testing using **Microsoft Excel, PostgreSQL, Python, and Power BI**.

> **Note:** This project uses simulated e-commerce data for educational and portfolio purposes. The findings do not represent the performance of a real company.

## 📌 Project Overview

The objective of this project is to transform raw e-commerce data into meaningful business insights. By analyzing user interactions, product sales, purchasing behavior, and customer retention, the project identifies potential opportunities to improve conversion rates, customer experience, and business performance.

## 🎯 Business Objectives

- Analyze sales and product performance.
- Understand customer purchasing behavior.
- Examine the e-commerce conversion funnel.
- Measure repeat purchases and customer retention.
- Explore customer cohorts and retention patterns.
- Compare conversion rates between A/B testing groups.
- Develop interactive Power BI dashboards.
- Provide data-driven business recommendations.

## 🛠️ Tools & Technologies

| Tool | Purpose |
|---|---|
| Microsoft Excel | Data cleaning, formulas, pivot tables, analysis, and summary dashboard |
| PostgreSQL | Data querying, aggregation, and business analysis |
| Python | Data cleaning, transformation, and exploratory data analysis |
| Pandas | Data manipulation and analysis |
| NumPy | Numerical calculations |
| Matplotlib & Seaborn | Data visualization |
| Power BI | Interactive dashboards and reporting |
| GitHub | Project documentation and version control |

## 📂 Project Structure

```text
Ecommerce-Product-Analytics/
│
├── data/
│   ├── raw/                 # Original simulated datasets
│   └── cleaned/             # Cleaned datasets
│
├── excel/                   # Excel analysis workbook
├── python/                  # Python analysis scripts
├── sql/                     # SQL analysis queries
├── powerbi/                 # Power BI dashboard
├── screenshots/             # Dashboard screenshots
├── results/                 # Analysis output files
├── reports/                 # PDF project report
├── demo/                    # Project demonstration
│
├── .gitignore
├── requirements.txt
└── README.md
```

## 📊 Datasets

The project uses five simulated datasets:

| Dataset | Description |
|---|---|
| `users.csv` | User information and acquisition channels |
| `events.csv` | User activities and product interactions |
| `products.csv` | Product information and categories |
| `orders.csv` | Order details, quantities, and revenue |
| `experiments.csv` | A/B testing assignments and conversion outcomes |

## 📈 Key Findings

### 1. Sales & Product Performance

| Metric | Result |
|---|---:|
| Total Orders | 2,884 |
| Total Quantity Sold | 5,717 |
| Total Revenue | ₹5,78,46,205 |
| Average Order Value | ₹20,049.31 |
| Products Analyzed | 50 |
| Best-Selling Product by Quantity | Product 030 |
| Highest Revenue from a Single Product | ₹23,83,944 |

**Business insight:** Product-level revenue and quantity analysis can help identify products to investigate for merchandising, promotion, and inventory planning.

### 2. Customer Analytics

| Metric | Result |
|---|---:|
| Registered Users | 10,000 |
| Purchasing Customers | 2,545 |
| Repeat Customers | 315 |
| Repeat-Purchase Rate Among Purchasing Customers | 12.38% |
| Average Revenue per Purchasing Customer | ₹22,729.35 |

**Business insight:** Customer purchasing and repeat-purchase patterns can help identify opportunities for retention campaigns and improved customer engagement.

### 3. Conversion Funnel Analysis

| Funnel Stage | Users |
|---|---:|
| Product Views | 10,000 |
| Add to Cart | 6,765 |
| Checkout | 4,786 |
| Purchases | 2,545 |

| Conversion Metric | Rate |
|---|---:|
| Add to Cart / Product Views | 67.65% |
| Checkout / Add to Cart | 70.75% |
| Purchases / Checkout | 53.18% |
| Purchases / Product Views | 25.45% |

**Business insight:** The observed counts suggest investigating checkout completion, including payment issues, unexpected costs, and usability barriers.

**Interpretation limitation:** These are aggregate stage-level counts. They should not be treated as a validated sequential conversion funnel until user-level event sequences and stage definitions have been checked.

### 4. A/B Testing Analysis

The Power BI dashboard displayed the following conversion rates:

| Experiment Group | Conversion Rate |
|---|---:|
| Control | 25.67% |
| Treatment | 25.55% |
| Difference | -0.12 percentage points |

**Business insight:** The treatment group had a slightly lower observed conversion rate than the control group.

**Important limitation:** This difference alone does not establish statistical significance or prove that the treatment caused a change. The experiment data, conversion definitions, and statistical test must be validated before making a product decision.

## 📉 Power BI Dashboard

The planned dashboard covers six analytical areas:

1. **Product Overview** — product and revenue performance.
2. **Conversion Funnel** — user activity across purchasing stages.
3. **Retention & Cohort Analysis** — customer retention patterns.
4. **A/B Testing Analysis** — comparison of experiment groups.
5. **Customer & Revenue Analytics** — purchasing and revenue metrics.
6. **Product Recommendations** — potential improvements based on analytical findings.

Dashboard screenshots and the `.pbix` file can be explored in the `screenshots/` and `powerbi/` folders when available.

## 💡 Business Recommendations

1. **Investigate checkout abandonment:** Examine payment failures, additional charges, and checkout usability.
2. **Improve customer retention:** Study repeat-purchase behavior and evaluate relevant loyalty offers or personalized communication.
3. **Optimize acquisition channels:** Compare channel-level purchasing conversion and revenue before reallocating marketing resources.
4. **Improve product merchandising:** Use product revenue and quantity sold to identify products worth featuring or investigating.
5. **Validate A/B tests:** Use a consistent conversion definition and appropriate statistical testing before implementing a product change.
6. **Monitor business performance:** Track revenue, average order value, purchasing customers, funnel conversion, and repeat-purchase rate over time.

These recommendations are analytical hypotheses based on simulated data, not verified business outcomes.

## 🧠 Skills Demonstrated

- Data cleaning and validation
- Exploratory data analysis
- Microsoft Excel formulas and reporting
- PostgreSQL and SQL queries
- Python data analysis with Pandas and NumPy
- Data visualization
- Product analytics
- Customer and revenue analytics
- Conversion funnel analysis
- Cohort and retention analysis
- A/B testing concepts
- Power BI dashboard development
- Business insight generation and communication

## ⚠️ Project Limitations

- All datasets are simulated.
- The aggregate funnel counts require event-sequence validation.
- A/B testing results require validated experiment data and statistical significance testing.
- Findings and recommendations are illustrative and should not be interpreted as real-company results.
- Dashboard screenshots, scripts, and reports should be considered available only if the corresponding files have been uploaded to the repository.

## 👨‍💻 About the Author

**Nikhil Kankatri**

Computer Science & Engineering Student  
Specialization: Internet of Things, Cybersecurity, and Blockchain

**Areas of Interest:** Data Analytics, Product Analytics, SQL, Python, Excel, and Power BI.

---

⭐ Thank you for visiting this project! Explore the repository to learn more about the datasets, analysis, and dashboards.
