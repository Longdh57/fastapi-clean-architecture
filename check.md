select c.id, c.code, c.product_code, c.status, c.paid_at, c.deleted_at,
       p.status as pay_status, p.response_code, p.response_desc,
       p.tx_id, p.transaction_id, p.created_at, p.updated_at
from contract c
left join payment_contract p on p.contract_id = c.id
where c.id = '0a29c074-8e0b-44c0-98e1-7d123a4fbf1e';




BEGIN;
update contract
set code='DSX.260000035' where id='92daeaa6-41e1-456f-b437-43ea67a23f18';

update contract
set code='DSX.260000036' where id='0a29c074-8e0b-44c0-98e1-7d123a4fbf1e';
UPDATE contract SET code = 'XM.260000818' WHERE id = 'ea7c1481-2671-4fac-82b5-c27adf5056d4' AND code IS NULL; -- 2026-06-11 04:31
UPDATE contract SET code = 'XM.260000819' WHERE id = '621ef6c2-ccb4-4fd7-8e02-06d50e998546' AND code IS NULL; -- 2026-06-11 12:22
UPDATE contract SET code = 'XM.260000820' WHERE id = '17c926ec-e1e8-4c36-bd8a-ad974ac97f4c' AND code IS NULL; -- 2026-06-11 12:25
UPDATE contract SET code = 'XM.260000821' WHERE id = 'ce89cca5-9eb4-450b-ae36-21bd0531b35f' AND code IS NULL; -- 2026-06-11 12:30
UPDATE contract SET code = 'XM.260000822' WHERE id = 'fc5309a1-5ff2-4987-8293-1129192741a6' AND code IS NULL; -- 2026-06-12 03:20
UPDATE contract SET code = 'XM.260000823' WHERE id = 'c2b4f535-718b-4e7c-95ba-5aaf416530f7' AND code IS NULL; -- 2026-06-12 03:25
UPDATE contract SET code = 'XM.260000824' WHERE id = 'aca19365-c9d0-4f97-b5bc-bd9e8e9e92b5' AND code IS NULL; -- 2026-06-12 03:27
UPDATE contract SET code = 'XM.260000825' WHERE id = '8e48ea6c-1532-4055-82f2-b988fcf5cb63' AND code IS NULL; -- 2026-06-13 13:31
UPDATE contract SET code = 'XM.260000826' WHERE id = 'f551f6db-3fb2-4e61-a1c2-fa5f9a40bfc7' AND code IS NULL; -- 2026-06-16 02:24
UPDATE contract SET code = 'XM.260000827' WHERE id = '75e84895-eb30-460b-a7e9-8ab2af80e491' AND code IS NULL; -- 2026-06-16 02:32
UPDATE contract SET code = 'XM.260000828' WHERE id = 'c6353e68-dfe4-4ab1-9fc4-9826779af61f' AND code IS NULL; -- 2026-06-18 03:27
UPDATE contract SET code = 'XM.260000829' WHERE id = '900ab800-08ca-4645-b9b8-27f81584d55a' AND code IS NULL; -- 2026-06-18 03:38
UPDATE contract SET code = 'XM.260000830' WHERE id = '95b88649-e950-4316-8085-c0da54c3858b' AND code IS NULL; -- 2026-06-18 03:54
UPDATE contract SET code = 'XM.260000831' WHERE id = 'bbed53f9-30b5-4097-a989-430ae7b17829' AND code IS NULL; -- 2026-06-18 04:10
UPDATE contract SET code = 'XM.260000832' WHERE id = 'd7e1df25-cc16-4da3-8b56-f4700079eb46' AND code IS NULL; -- 2026-06-18 04:20
UPDATE contract SET code = 'XM.260000833' WHERE id = '38bc6074-3474-40ef-a4aa-b185d48bb74f' AND code IS NULL; -- 2026-06-19 01:45
UPDATE contract SET code = 'XM.260000834' WHERE id = '1a321d2c-fe05-4ad3-b823-c0e8cdd069ad' AND code IS NULL; -- 2026-06-19 15:10
UPDATE contract SET code = 'XM.260000835' WHERE id = 'b945a632-d694-4500-8c3e-329a596a19d5' AND code IS NULL; -- 2026-06-20 13:29
UPDATE contract SET code = 'XM.260000836' WHERE id = '57402630-d2aa-48db-8c2f-081dc52b8701' AND code IS NULL; -- 2026-06-20 13:35
UPDATE contract SET code = 'XM.260000837' WHERE id = 'a3cfcdaa-12c9-447c-a180-cb2a1400f70a' AND code IS NULL; -- 2026-06-20 13:39
UPDATE contract SET code = 'XM.260000838' WHERE id = '5a7be857-2049-4415-bbad-d1a23c0707bd' AND code IS NULL; -- 2026-06-21 13:18
UPDATE contract SET code = 'XM.260000839' WHERE id = '4747dcbf-a21b-45c3-a9c2-cc520226a7c2' AND code IS NULL; -- 2026-06-22 03:40
UPDATE contract SET code = 'XM.260000840' WHERE id = '756354f4-4f4f-43ab-b078-adc145aa972f' AND code IS NULL; -- 2026-06-22 03:44
UPDATE contract SET code = 'XM.260000841' WHERE id = '92af43fa-2b28-4859-8e4d-b3ff20f5c649' AND code IS NULL; -- 2026-06-22 04:18
UPDATE contract SET code = 'XM.260000842' WHERE id = '4fad001e-8d41-4fd2-bbbf-864090a2df9e' AND code IS NULL; -- 2026-06-22 09:04
UPDATE contract SET code = 'XM.260000843' WHERE id = 'd9628001-2688-48d5-ac83-db2d4ca512c1' AND code IS NULL; -- 2026-06-22 09:09
UPDATE contract SET code = 'XM.260000844' WHERE id = 'ee0f4277-0c7c-453b-b80a-aadd99edec8b' AND code IS NULL; -- 2026-06-22 09:14
UPDATE contract SET code = 'XM.260000845' WHERE id = '0a18f34f-f975-426d-afe5-71f5d7282384' AND code IS NULL; -- 2026-06-26 05:06
UPDATE contract SET code = 'XM.260000846' WHERE id = '7e56d19d-c0e4-4b17-8a51-149868168b35' AND code IS NULL; -- 2026-06-29 09:01

-- COMMIT;
-- ROLLBACK;
