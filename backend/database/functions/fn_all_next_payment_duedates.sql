-- Get query to get tenant bills
DROP FUNCTION IF EXISTS fn_all_next_payment_duedates;
CREATE FUNCTION fn_all_next_payment_duedates
(
    p_user_id INTEGER
)
RETURNS TABLE
(
    tenancy_id INTEGER,
    next_payment_due_date TIMESTAMP
)
AS $$
BEGIN
    RETURN QUERY SELECT
        tenancy.id,
        MIN(tenant_bill.due_date)
    FROM
        users
    LEFT OUTER JOIN
        tenancy
    ON
        users.account_id = tenancy.account_id
    LEFT OUTER JOIN
        tenant_bill_status
    ON
        tenant_bill_status.value = 'unpaid'
    LEFT OUTER JOIN
        tenant_bill
    ON
        tenant_bill_status.id = tenant_bill.tenant_bill_status_id
    AND
        tenancy.id = tenant_bill.tenancy_id
    WHERE
        users.id = p_user_id
    GROUP BY
        tenancy.id;
END; $$

LANGUAGE 'plpgsql';