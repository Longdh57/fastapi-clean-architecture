select c.id, c.code, c.product_code, c.status, c.paid_at, c.deleted_at,
       p.status as pay_status, p.response_code, p.response_desc,
       p.tx_id, p.transaction_id, p.created_at, p.updated_at
from contract c
left join payment_contract p on p.contract_id = c.id
where c.id = '0a29c074-8e0b-44c0-98e1-7d123a4fbf1e';


