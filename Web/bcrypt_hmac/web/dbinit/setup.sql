USE webapp;

CREATE TABLE notes (
    id varchar(255) NOT NULL PRIMARY KEY,
    note varchar(1024)
);

CREATE TABLE flag (
    wowee_what_a_cool_flag varchar(255)
);

INSERT INTO flag (wowee_what_a_cool_flag) VALUES ('WMG{BcRYpT_1s_N0T_SuiTAbL3_F0r_HM4C}');