CREATE OR REPLACE TABLE SLEEKMART_OMS.TRAINING.profit_uk AS (
    SELECT 
        sales_date, 
        SUM(quantity_sold * unit_sell_price) AS total_revenue,
        SUM(quantity_sold * unit_purchase_cost) AS total_cost,
        SUM(quantity_sold * unit_sell_price) - SUM(quantity_sold * unit_purchase_cost) AS total_profit
    FROM 
        SLEEKMART_OMS.TRAINING.sales_uk
    WHERE
        sales_date BETWEEN '{{ var.json.process_interval.start_date }}' AND '{{ var.json.process_interval.end_date }}'
    GROUP BY 
        sales_date
)