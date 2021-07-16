-- Get tenancy display rows
DROP FUNCTION IF EXISTS sp_list_tenancies;
CREATE FUNCTION sp_list_tenancies
(
    p_user_id INTEGER
)
RETURNS TABLE
(
    tenancy JSON,
    tenant_names VARCHAR [],
    payment_terms VARCHAR,
    rent_type VARCHAR,
    next_payment TIMESTAMP,
    tenancy_status VARCHAR
)
AS $$
BEGIN
    RETURN QUERY SELECT
        tenancy_details.*
    FROM
    (
        SELECT
            ROW_TO_JSON(tenancy.*) AS tenancy,
            ARRAY_AGG(tenant.name) AS tenant_names,
            payment_terms.value AS payment_terms,
            rent_type.value AS rent_type,
            next_payment.next_payment_due_date AS next_payment,
            tenancy_status.value AS tenancy_status
        FROM
            users
        LEFT OUTER JOIN
            tenancy
        ON
            users.account_id = tenancy.account_id
        LEFT OUTER JOIN
            tenant
        ON
            tenancy.id = tenant.tenancy_id
        LEFT OUTER JOIN
            payment_terms
        ON
            tenancy.payment_terms_id = payment_terms.id
        LEFT OUTER JOIN
            rent_type
        ON
            tenancy.rent_type_id = rent_type.id
        LEFT OUTER JOIN
        (
            SELECT
                tenancy_id,
                next_payment_due_date
            FROM
                fn_all_next_payment_duedates(p_user_id)
        ) AS next_payment
        ON
            tenancy.id = next_payment.tenancy_id
        LEFT OUTER JOIN
            tenancy_status
        ON
            tenancy.tenancy_status_id = tenancy_status.id
        WHERE
            users.id = p_user_id
        AND
            tenancy.is_deleted = false
        GROUP BY
            tenancy.id,
            payment_terms,
            rent_type,
            next_payment,
            tenancy_status
    ) AS tenancy_details;
END; $$

LANGUAGE 'plpgsql';
