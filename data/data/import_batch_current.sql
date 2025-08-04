BEGIN TRANSACTION;

-- Insert Business Details (if not already present)
INSERT OR IGNORE INTO business_details (
    id, company_name, address_line1, address_line2, city, province, postal_code, telephone, vat_number
) VALUES (
    1, 'Universal Recycling Company Pty Ltd', '123 Industrial Road', 'Unit 4', 'Cape Town', 'Western Cape', '8001', '+27 21 555 1234', 'VAT123456789'
);

-- Insert 'Various' as a requester
INSERT OR IGNORE INTO requesters (name) VALUES ('Various');

-- Insert UNIQUE Project Codes specific to this order
INSERT OR IGNORE INTO projects (project_code, project_name) VALUES ('DR16M', 'Project DR16M');
INSERT OR IGNORE INTO projects (project_code, project_name) VALUES ('TR20M', 'Project TR20M');
INSERT OR IGNORE INTO projects (project_code, project_name) VALUES ('TR18M', 'Project TR18M');
INSERT OR IGNORE INTO projects (project_code, project_name) VALUES ('TR24M', 'Project TR24M');
INSERT OR IGNORE INTO projects (project_code, project_name) VALUES ('TR59M', 'Project TR59M');


-- Insert UNIQUE suppliers specific to this order
INSERT OR IGNORE INTO suppliers (name) VALUES ('GALAXY TRADING');


-- Insert UNIQUE items specific to this order
INSERT OR IGNORE INTO items (item_code, item_description) VALUES ('FILT210', 'FILTER P83 1079');
INSERT OR IGNORE INTO items (item_code, item_description) VALUES ('FILT229', 'FILTER P82-7655');
INSERT OR IGNORE INTO items (item_code, item_description) VALUES ('FILT230', 'FILTER BT 223/Z217 / P55');
INSERT OR IGNORE INTO items (item_code, item_description) VALUES ('FILT115', 'FILTER BF 7535 / Z 188 F');
INSERT OR IGNORE INTO items (item_code, item_description) VALUES ('FILT102', 'FILTER B 2/Z 95 / P55-00');
INSERT OR IGNORE INTO items (item_code, item_description) VALUES ('FILT100', 'FILTER B 295 / Z 84');
INSERT OR IGNORE INTO items (item_code, item_description) VALUES ('FILT308', 'FILTER 110-6326 \ P77528');
INSERT OR IGNORE INTO items (item_code, item_description) VALUES ('FILT309', 'FILTER P775302/110 - 63');
INSERT OR IGNORE INTO items (item_code, item_description) VALUES ('FILT006', 'FILTER AIR ADG 519/P18');
INSERT OR IGNORE INTO items (item_code, item_description) VALUES ('FILT007', 'FILTER AIR ADG 520 \ P11');
INSERT OR IGNORE INTO items (item_code, item_description) VALUES ('FILT096', 'FILTER BT292 / Z 66 / P55');
INSERT OR IGNORE INTO items (item_code, item_description) VALUES ('FILT184', 'FILTER PT 539/ P557380');
INSERT OR IGNORE INTO items (item_code, item_description) VALUES ('FILT393', 'FILTER Z195/ BF330 / P55');
INSERT OR IGNORE INTO items (item_code, item_description) VALUES ('FILT164', 'FILTER BF 7674 D/ P5514');
INSERT OR IGNORE INTO items (item_code, item_description) VALUES ('FILT371', 'FILTER P550587 / BF587D');
INSERT OR IGNORE INTO items (item_code, item_description) VALUES ('FILT385', 'FILTER OIL B 7116 / PH 53');
INSERT OR IGNORE INTO items (item_code, item_description) VALUES ('FILT327', 'FILTER HYDRAULIC BT35');
INSERT OR IGNORE INTO items (item_code, item_description) VALUES ('FILT409', 'FILTER LX 345 / P778441');
INSERT OR IGNORE INTO items (item_code, item_description) VALUES ('FILT372', 'FILTER AIR DRYER BA53');
INSERT OR IGNORE INTO items (item_code, item_description) VALUES ('FILT361', 'FILTER STEERING P106H');


-- Order 2295
-- Delete related records from dependent tables first
DELETE FROM received_item_logs WHERE order_item_id IN (SELECT oi.id FROM order_items oi JOIN orders o ON oi.order_id = o.id WHERE o.order_number = '2295');
DELETE FROM audit_trail WHERE order_id IN (SELECT id FROM orders WHERE order_number = '2295');
DELETE FROM attachments WHERE order_id IN (SELECT id FROM orders WHERE order_number = '2295');
DELETE FROM order_items WHERE order_id IN (SELECT id FROM orders WHERE order_number = '2295');
DELETE FROM orders WHERE order_number = '2295';

INSERT INTO orders (order_number, status, created_date, total, supplier_id, requester_id, required_auth_band, payment_terms, last_modified_by_user_id)
VALUES (
    '2295',
    'Pending',
    '2025-07-15', -- Date from image_845b8d.png
    5974.75, -- Sum of item totals: (1*201.96) + (1*256.67) + (2*98.28) + (1*151.12) + (1*116.46) + (1*151.12) + (1*54.04) + (1*295.65) + (1*193.99) + (1*303.51) + (1*257.30) + (1*152.60) + (1*504.22) + (1*216.01) + (1*303.51) + (1*257.30) + (1*152.60) + (1*332.91) + (1*504.22) + (2*178.21) + (1*342.63) + (1*410.54) + (1*779.70) + (1*487.39) + (1*62.25) = 5974.75
    (SELECT id FROM suppliers WHERE name = 'GALAXY TRADING'),
    (SELECT id FROM requesters WHERE name = 'Various'),
    1,
    'On account',
    1
);
INSERT INTO order_items (order_id, item_code, item_description, project, qty_ordered, price, total)
VALUES ( (SELECT id FROM orders WHERE order_number = '2295'), 'FILT210', 'FILTER P83 1079', 'DR16M', 1, 201.96, 201.96);
INSERT INTO order_items (order_id, item_code, item_description, project, qty_ordered, price, total)
VALUES ( (SELECT id FROM orders WHERE order_number = '2295'), 'FILT229', 'FILTER P82-7655', 'DR16M', 1, 256.67, 256.67);
INSERT INTO order_items (order_id, item_code, item_description, project, qty_ordered, price, total)
VALUES ( (SELECT id FROM orders WHERE order_number = '2295'), 'FILT230', 'FILTER BT 223/Z217 / P55', 'DR16M', 2, 98.28, 196.56);
INSERT INTO order_items (order_id, item_code, item_description, project, qty_ordered, price, total)
VALUES ( (SELECT id FROM orders WHERE order_number = '2295'), 'FILT115', 'FILTER BF 7535 / Z 188 F', 'DR16M', 1, 151.12, 151.12);
INSERT INTO order_items (order_id, item_code, item_description, project, qty_ordered, price, total)
VALUES ( (SELECT id FROM orders WHERE order_number = '2295'), 'FILT102', 'FILTER B 2/Z 95 / P55-00', 'TR20M', 1, 116.46, 116.46);
INSERT INTO order_items (order_id, item_code, item_description, project, qty_ordered, price, total)
VALUES ( (SELECT id FROM orders WHERE order_number = '2295'), 'FILT115', 'FILTER BF 7535 / Z 188 F', 'TR20M', 1, 151.12, 151.12);
INSERT INTO order_items (order_id, item_code, item_description, project, qty_ordered, price, total)
VALUES ( (SELECT id FROM orders WHERE order_number = '2295'), 'FILT100', 'FILTER B 295 / Z 84', 'TR20M', 1, 54.04, 54.04);
INSERT INTO order_items (order_id, item_code, item_description, project, qty_ordered, price, total)
VALUES ( (SELECT id FROM orders WHERE order_number = '2295'), 'FILT308', 'FILTER 110-6326 \ P77528', 'TR20M', 1, 295.65, 295.65);
INSERT INTO order_items (order_id, item_code, item_description, project, qty_ordered, price, total)
VALUES ( (SELECT id FROM orders WHERE order_number = '2295'), 'FILT309', 'FILTER P775302/110 - 63', 'TR20M', 1, 193.99, 193.99);
INSERT INTO order_items (order_id, item_code, item_description, project, qty_ordered, price, total)
VALUES ( (SELECT id FROM orders WHERE order_number = '2295'), 'FILT006', 'FILTER AIR ADG 519/P18', 'TR18M', 1, 303.51, 303.51);
INSERT INTO order_items (order_id, item_code, item_description, project, qty_ordered, price, total)
VALUES ( (SELECT id FROM orders WHERE order_number = '2295'), 'FILT007', 'FILTER AIR ADG 520 \ P11', 'TR18M', 1, 257.30, 257.30);
INSERT INTO order_items (order_id, item_code, item_description, project, qty_ordered, price, total)
VALUES ( (SELECT id FROM orders WHERE order_number = '2295'), 'FILT096', 'FILTER BT292 / Z 66 / P55', 'TR18M', 1, 152.60, 152.60);
INSERT INTO order_items (order_id, item_code, item_description, project, qty_ordered, price, total)
VALUES ( (SELECT id FROM orders WHERE order_number = '2295'), 'FILT184', 'FILTER PT 539/ P557380', 'TR18M', 1, 504.22, 504.22);
INSERT INTO order_items (order_id, item_code, item_description, project, qty_ordered, price, total)
VALUES ( (SELECT id FROM orders WHERE order_number = '2295'), 'FILT393', 'FILTER Z195/ BF330 / P55', 'TR24M', 1, 216.01, 216.01);
INSERT INTO order_items (order_id, item_code, item_description, project, qty_ordered, price, total)
VALUES ( (SELECT id FROM orders WHERE order_number = '2295'), 'FILT006', 'FILTER AIR ADG 519/P18', 'TR24M', 1, 303.51, 303.51);
INSERT INTO order_items (order_id, item_code, item_description, project, qty_ordered, price, total)
VALUES ( (SELECT id FROM orders WHERE order_number = '2295'), 'FILT007', 'FILTER AIR ADG 520 \ P11', 'TR24M', 1, 257.30, 257.30);
INSERT INTO order_items (order_id, item_code, item_description, project, qty_ordered, price, total)
VALUES ( (SELECT id FROM orders WHERE order_number = '2295'), 'FILT096', 'FILTER BT292 / Z 66 / P55', 'TR24M', 1, 152.60, 152.60);
INSERT INTO order_items (order_id, item_code, item_description, project, qty_ordered, price, total)
VALUES ( (SELECT id FROM orders WHERE order_number = '2295'), 'FILT164', 'FILTER BF 7674 D/ P5514', 'TR24M', 1, 332.91, 332.91);
INSERT INTO order_items (order_id, item_code, item_description, project, qty_ordered, price, total)
VALUES ( (SELECT id FROM orders WHERE order_number = '2295'), 'FILT184', 'FILTER PT 539/P557380', 'TR24M', 1, 504.22, 504.22);
INSERT INTO order_items (order_id, item_code, item_description, project, qty_ordered, price, total)
VALUES ( (SELECT id FROM orders WHERE order_number = '2295'), 'FILT371', 'FILTER P550587 / BF587D', 'TR59M', 2, 178.21, 356.42);
INSERT INTO order_items (order_id, item_code, item_description, project, qty_ordered, price, total)
VALUES ( (SELECT id FROM orders WHERE order_number = '2295'), 'FILT385', 'FILTER OIL B 7116 / PH 53', 'TR59M', 1, 342.63, 342.63);
INSERT INTO order_items (order_id, item_code, item_description, project, qty_ordered, price, total)
VALUES ( (SELECT id FROM orders WHERE order_number = '2295'), 'FILT327', 'FILTER HYDRAULIC BT35', 'TR59M', 1, 410.54, 410.54);
INSERT INTO order_items (order_id, item_code, item_description, project, qty_ordered, price, total)
VALUES ( (SELECT id FROM orders WHERE order_number = '2295'), 'FILT409', 'FILTER LX 345 / P778441', 'TR59M', 1, 779.70, 779.70);
INSERT INTO order_items (order_id, item_code, item_description, project, qty_ordered, price, total)
VALUES ( (SELECT id FROM orders WHERE order_number = '2295'), 'FILT372', 'FILTER AIR DRYER BA53', 'TR59M', 1, 487.39, 487.39);
INSERT INTO order_items (order_id, item_code, item_description, project, qty_ordered, price, total)
VALUES ( (SELECT id FROM orders WHERE order_number = '2295'), 'FILT361', 'FILTER STEERING P106H', 'TR59M', 1, 62.25, 62.25);
INSERT INTO audit_trail (order_id, action, details, user_id)
VALUES (
    (SELECT id FROM orders WHERE order_number = '2295'),
    'Created',
    'Order 2295 created via script (overwrite)',
    1
);

COMMIT;