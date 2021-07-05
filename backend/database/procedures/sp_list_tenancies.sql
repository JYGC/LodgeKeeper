-- Get tenancy display rows
DROP PROCEDURE IF EXISTS sp_list_tenancies;
CREATE PROCEDURE sp_list_tenancies
(
    p_user_id INTEGER
)
LANGUAGE SQL
AS $$
    SELECT
        ROW_TO_JSON(tenancy.*) AS tenancy,
        tenant_names.tenant_names,
        payment_terms.value AS payment_terms,
        rent_type.value AS rent_type,
        next_payment.next_payment_due_date,
        tenancy_status.value AS tenancy_status
    FROM
        users
    LEFT OUTER JOIN
        tenancy
    ON
        users.account_id = tenancy.account_id
    LEFT OUTER JOIN
    (
        SELECT
            tenancy_id,
            tenant_names
        FROM
            fn_tenant_names_array(p_user_id)
    ) AS tenant_names
    ON
        tenancy.id = tenant_names.tenancy_id
    LEFT OUTER JOIN
        payment_terms
    ON
        tenancy.payment_terms_id = payment_terms.id
    LEFT OUTER JOIN
        rent_type
    ON
        tenancy.rent_type_id = rent_type.id
    LEFT OUTER JOIN LATERAL
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
        tenancy.is_deleted = false;
$$;
