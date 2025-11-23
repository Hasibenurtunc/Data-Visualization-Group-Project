# Shopping Trends Analysis Dashboard

This project is an interactive data visualization dashboard built with Streamlit and Python to analyze customer shopping behavior and trends. Users can apply real-time filters, click on chart elements to refine results, and explore purchasing patterns in detail.

**Course:** CEN445 Introduction to Data Visualization | 2025-26  
**Team Members:**
- 2021556046 - Habibe Ceren Korkmaz
- 2021556049 - Gülse Ogultegin
- 2021556067 - Hasibe Nur Tunç

---

## Project Overview

The dashboard presents nine different visualizations that examine shopping behavior. Three of these visualizations are basic, while six are advanced. All charts support click-to-filter interaction, and every action triggers real-time updates. Users can filter data through the sidebar or directly by interacting with the charts.

---

## Dataset

Source: https://www.kaggle.com/datasets/brandmustafa/shopping-trends
The dataset used in this project is named `Shopping_behavior_updated.csv` and contains 3,900 rows and 18 columns. It includes customer information such as age, gender, product categories, purchase amounts, payment methods, shipping preferences, and customer ratings.

---

## Visualizations

### Basic Visualizations

1. **Bar Chart:** Top 10 most purchased items
2. **Line Chart:** Average purchase amount by age group
3. **Pie Chart:** Sales distribution by product category

### Advanced Visualizations

4. **Treemap:** Hierarchical view of category and item-based sales
5. **Sankey Diagram:** Flow between category, payment method, and shipping preference
6. **Parallel Coordinates:** Multi-dimensional customer segmentation
7. **Sunburst Chart:** Seasonal and category-based breakdown
8. **3D Scatter Plot:** Relationship between age, purchase amount, and rating
9. **Correlation Heatmap:** Relationship strength between numerical variables

---

## Interactive Features

- The sidebar includes filters for gender, season, category, age range, and purchase amount.
- All visualizations support click-based filtering.
- Users can select specific age groups, categories, or items through checkbox lists.
- Key metrics such as total customers, average purchase, average rating, and total revenue update instantly based on the applied filters.
- A reset button allows users to clear all active filters.

---

## Installation

To run this application, Python 3.8 or higher is required. Necessary packages include:

- `streamlit` 1.28.0 or higher
- `pandas` 2.0.0 or higher
- `plotly` 5.17.0 or higher
- `seaborn` 0.12.0 or higher
- `matplotlib` 3.7.0 or higher

### Installation Steps
```bash
pip install streamlit pandas plotly seaborn matplotlib
streamlit run app.py
```

---

## Usage

After launching the application, users can apply filters from the sidebar. Clicking on elements inside the visualizations will automatically apply corresponding filters. Users can also narrow down the data by selecting specific categories, age groups, or items through the checkbox panels. The **Reset All Filters** option clears all selections. The **View Insights** sections provide brief explanations and business-related interpretations for each chart.

---

## Team Contributions

- **Habibe Ceren Korkmaz:** Line Chart, Parallel Coordinates Plot, Sunburst Chart
- **Gülse Ogultegin:** Bar Chart, Sankey Diagram, 3D Scatter Plot
- **Hasibe Nur Tunç:** Pie Chart, Treemap, Correlation Heatmap

- **Readme, main control panel, data preprocessing file, and report generation have been prepared and committed together.**

---

