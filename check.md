select c.id, c.code, c.product_code, c.status, c.paid_at, c.deleted_at,
       p.status as pay_status, p.response_code, p.response_desc,
       p.tx_id, p.transaction_id, p.created_at, p.updated_at
from contract c
left join payment_contract p on p.contract_id = c.id
where c.id = '0a29c074-8e0b-44c0-98e1-7d123a4fbf1e';


Xem nhanh trạng thái & member:
docker exec -it mobifone-kafka kafka-consumer-groups --bootstrap-server localhost:9092 \
  --describe --group production_group-contract_supplier_core --state --members
STATE = Stable + có member ⇒ consumer đang sống. Empty/Dead ⇒ không có ai consume.

Check 2 — Message có thực sự nằm trên topic không? (phân biệt lỗi producer vs consumer)

LAG = 0 mơ hồ: có thể "đã consume rồi return sớm", cũng có thể "producer chưa từng ghi". Đọc thẳng topic để tìm contractId của đơn:

# thay <productCode> đúng loại đơn: motor/car/electricial/house
docker exec -it mobifone-kafka kafka-console-consumer \
  --bootstrap-server localhost:9092 \
  --topic production_topic-<productCode>_contract_core \
  --from-beginning --timeout-ms 15000 | grep '<contract_id>'

- Tìm thấy contract_id trên topic nhưng status vẫn New ⇒ lỗi phía consumer (không consume, hoặc consume nhưng getOne trả null → if (!contract) return, vd contract bị soft-delete deleted_at).
- Không thấy ⇒ producer rớt message (Kafka down lúc callback, hoặc product_code rơi vào default: break trong pushCore). Lúc này consumer không có lỗi gì.


