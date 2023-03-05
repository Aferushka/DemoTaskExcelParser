CREATE_TABLE = """
        create table if not exists common_table
(
    id            integer not null
        constraint common_table_pk
            primary key autoincrement,
    data          text    not null,
    company       text    not null,
    fact_qliq     integer not null,
    fact_qoil     integer not null,
    forecast_qliq integer not null,
    forecast_qoil integer not null
);

create unique index if not exists common_table_id_uindex
    on common_table (id);
        """

DROP_TABLE = "drop table if exists common_table"

CREATE_VIEW = """
        CREATE VIEW if not exists pivot_by_dates_fact as
select "data", company, sum(fact_qliq) Qliq, sum(fact_qoil) Qoil from common_table
group by "data", company;

        """