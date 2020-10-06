-- MySQL compatible
SELECT
        CAST( DATE AS DATE ) AS DATE,
        SUM(prod_qty * prod_price) AS ventes
FROM
    TRANSACTION INNER JOIN product_nomenclature
        ON product_nomenclature.product_id = transaction.prop_id
WHERE
    transaction.date BETWEEN "2019-01-01" AND "2019-12-31"
GROUP BY
    DATE
ORDER BY
    DATE
;
