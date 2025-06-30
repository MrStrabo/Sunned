CREATE TABLE solar_generation
(
    rowid         uuid        not null
        constraint solar_generation_pk
            primary key,
    source_system varchar(50) not null,
    device_type   varchar(50) not null,
    serial_number varchar(50) not null,
    data_payload  jsonb       not null,
    reporting_ts  timestamp with timezone
);