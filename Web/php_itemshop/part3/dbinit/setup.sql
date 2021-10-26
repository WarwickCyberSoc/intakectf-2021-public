USE webapp;

CREATE TABLE products (
    name varchar(255),
    price decimal,
    stock integer
);

INSERT INTO products (name, price, stock) VALUES ('Netkit License', 52.43, 4114), ('Netkit 2 License', 611.43, 4), ('Kathara License', 51552.43, 11112), ('Linux License', 0.0, 999932);