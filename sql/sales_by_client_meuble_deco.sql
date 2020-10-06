-- MySQL compatible

SELECT
        client_id,
        ventes_meuble,
        ventes_deco
FROM
    TRANSACTION AS t
    -- compute ventes_meuble by client_id
    JOIN
        (SELECT
            SUM(prod_price) AS ventes_meuble,
            client_id AS client_id_meuble
        FROM
            TRANSACTION t INNER JOIN product_nomenclature
                ON product_nomenclature.product_id = t.prop_id
                AND t.client_id = client_id
        WHERE
            product_nomenclature.product_type = 'MEUBLE'
        GROUP BY
            client_id
        ) AS table_meuble
    ON t.client_id = table_meuble.client_id_meuble
    -- compute ventes_deco by client_id
    JOIN
        (SELECT
            SUM(prod_price) AS ventes_deco,
            client_id AS client_id_deco
        FROM
            TRANSACTION t INNER JOIN product_nomenclature
                ON product_nomenclature.product_id = t.prop_id
                AND t.client_id = client_id
        WHERE
            product_nomenclature.product_type = 'DECO'
        GROUP BY
            client_id_deco
        ) AS table_deco
    ON t.client_id = table_deco.client_id_deco
    WHERE
        t.date BETWEEN "2019-01-01" AND "2019-12-31"
    GROUP BY
        client_id
;
