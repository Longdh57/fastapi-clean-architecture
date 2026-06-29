select c.id, c.code, c.product_code, c.status, c.paid_at, c.deleted_at,
       p.status as pay_status, p.response_code, p.response_desc,
       p.tx_id, p.transaction_id, p.created_at, p.updated_at
from contract c
left join payment_contract p on p.contract_id = c.id
where c.id = '0a29c074-8e0b-44c0-98e1-7d123a4fbf1e';




BEGIN;

-- 1) Đơn 92daeaa6...: trạng thái "Mới tạo" (status = 0) + start_at = 01/07/2026 (giờ VN)
UPDATE contract
SET    status     = 0,
       start_at   = '2026-06-30 17:00:00+00',   -- = 2026-07-01 00:00:00 giờ VN (UTC+7)
       updated_at = now()
WHERE  id = '92daeaa6-41e1-456f-b437-43ea67a23f18';

-- 2) Xóa email của customer gắn với đơn này
UPDATE customer
SET    email = NULL
WHERE  id = (SELECT customer_id
             FROM   contract
             WHERE  id = '92daeaa6-41e1-456f-b437-43ea67a23f18');

-- Kiểm tra (kỳ vọng mỗi câu UPDATE 1) rồi:
-- COMMIT;
