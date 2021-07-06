-- Get query to get tenant names
DROP FUNCTION IF EXISTS fn_tenant_names_array;
CREATE FUNCTION fn_tenant_names_array
(
    p_user_id INTEGER
)
RETURNS TABLE
(
    tenancy_id INTEGER,
    tenant_name_array VARCHAR []
)
AS $$
BEGIN
    RETURN QUERY SELECT
        tenancy.id,
        ARRAY_AGG(tenant.name)
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
    WHERE
        users.id = p_user_id
    GROUP BY
        tenancy.id;
END; $$

LANGUAGE 'plpgsql';
