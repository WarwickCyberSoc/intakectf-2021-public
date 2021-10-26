USE webapp;

CREATE TABLE products (
    name varchar(255),
    price decimal,
    stock integer
);

CREATE TABLE the_flag (
    flag varchar(255)
);

INSERT INTO products (name, price, stock) VALUES ('Netkit License', 52.43, 4114), ('Netkit 2 License', 611.43, 4), ('Kathara License', 51552.43, 11112), ('Linux License', 0.0, 999932);

INSERT INTO the_flag (flag) VALUES ('WMG{w3_D0_4_L1TtL3_81t_0F_5Ql_1N3CJT10n}');