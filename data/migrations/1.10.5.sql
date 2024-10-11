alter table bruise
    add height decimal(10, 2) null;
alter table bruise
    add diameter decimal(10, 2) null;
alter table bruise
    add width decimal(10, 2) null;
alter table bruise
    add diameter decimal(10, 2) null;

create table aux_model
(
    id              int auto_increment
        primary key,
    name            varchar(50)                        not null,
    current_version varchar(50)                        null,
    path            varchar(256)                       not null,
    approach        varchar(256)                       not null,
    created_at      datetime default CURRENT_TIMESTAMP not null,
    updated_at      datetime default CURRENT_TIMESTAMP not null
);

create table model_update_history
(
    id              int auto_increment
        primary key,
    model_id        int                                not null,
    current_version varchar(50)                        not null,
    update_version  varchar(50)                        not null,
    created_at      datetime default CURRENT_TIMESTAMP not null,
    constraint model_update_history_model_info_id_fk
        foreign key (model_id) references aux_model (id)
);

create table aux_module
(
    id              int auto_increment
        primary key,
    name            varchar(50)                        not null,
    current_version varchar(50)                        null,
    path            varchar(256)                       not null,
    created_at      datetime default CURRENT_TIMESTAMP not null,
    updated_at      datetime default CURRENT_TIMESTAMP not null
);

create table module_update_history
(
    id              int auto_increment
        primary key,
    module_id       int                                not null,
    current_version varchar(50)                        not null,
    update_version  varchar(50)                        not null,
    created_at      datetime default CURRENT_TIMESTAMP not null,
    constraint module_update_history_module_info_id_fk
        foreign key (module_id) references aux_module (id)
);

