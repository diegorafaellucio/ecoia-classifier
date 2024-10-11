create table aux_configuration_group
(
    id          integer auto_increment
        primary key,
    value       varchar(50)  null,
    description varchar(256) null
);

alter table configuration_storage add aux_configuration_group_id int null;

alter table configuration_storage
    add constraint configuration_storage_aux_configuration_group_id_fk
        foreign key (aux_configuration_group_id) references aux_configuration_group (id);

INSERT INTO db_industry_pgo.aux_configuration_group (id, value, description) VALUES (1, 'MODELS_SETTINGS', null);
INSERT INTO db_industry_pgo.aux_configuration_group (id, value, description) VALUES (2, 'FILTER_SETTINGS', null);
INSERT INTO db_industry_pgo.aux_configuration_group (id, value, description) VALUES (3, 'STORAGE_SETTINGS', null);
INSERT INTO db_industry_pgo.aux_configuration_group (id, value, description) VALUES (4, 'ENDPOINT_SETTINGS', null);
INSERT INTO db_industry_pgo.aux_configuration_group (id, value, description) VALUES (5, 'INTEGRATION_SETTINGS', null);
INSERT INTO db_industry_pgo.aux_configuration_group (id, value, description) VALUES (6, 'CLIENT_IDENTIFIER_SETTINGS', null);
INSERT INTO db_industry_pgo.aux_configuration_group (id, value, description) VALUES (7, 'BUSINESS_RULES_SETTINGS', null);


create table model_info
(
    id              int auto_increment
        primary key,
    name            varchar(50) not null,
    current_version varchar(50) null,
    created_at      datetime    null,
    updated_at      datetime    null
);

alter table model_info
    modify created_at datetime default current_timestamp not null;

alter table model_info
    modify updated_at datetime default current_timestamp not null;

INSERT INTO aux_model (id, name, current_version, path, approach, created_at, updated_at) VALUES (1, 'breed', null, 'data/models/breed/weight.pt', 'ULTRALYTICS', '2024-09-06 08:24:26', '2024-09-06 08:24:26');
INSERT INTO aux_model (id, name, current_version, path, approach, created_at, updated_at) VALUES (2, 'bruise', null, 'data/models/bruise/weight.pt', 'ULTRALYTICS', '2024-09-06 08:24:26', '2024-09-06 08:24:26');
INSERT INTO aux_model (id, name, current_version, path, approach, created_at, updated_at) VALUES (3, 'conformation', null, 'data/models/conformation/weight.pt', 'ULTRALYTICS', '2024-09-06 08:24:26', '2024-09-06 08:24:26');
INSERT INTO aux_model (id, name, current_version, path, approach, created_at, updated_at) VALUES (4, 'cuts', null, 'data/models/cuts/weight.pt', 'ULTRALYTICS', '2024-09-06 08:24:26', '2024-09-06 08:24:26');
INSERT INTO aux_model (id, name, current_version, path, approach, created_at, updated_at) VALUES (5, 'filter', null, 'data/models/filter/weight.pt', 'ULTRALYTICS', '2024-09-06 08:24:26', '2024-09-06 08:24:26');
INSERT INTO aux_model (id, name, current_version, path, approach, created_at, updated_at) VALUES (6, 'grease', null, 'data/models/grease/weight.pt', 'ULTRALYTICS', '2024-09-06 08:24:26', '2024-09-06 08:24:26');
INSERT INTO aux_model (id, name, current_version, path, approach, created_at, updated_at) VALUES (7, 'hump', null, 'data/models/hump/weight.pt', 'ULTRALYTICS', '2024-09-06 08:24:26', '2024-09-06 08:24:26');
INSERT INTO aux_model (id, name, current_version, path, approach, created_at, updated_at) VALUES (8, 'meat', null, 'data/models/meat/weight.pt', 'ULTRALYTICS', '2024-09-06 08:24:26', '2024-09-06 08:24:26');
INSERT INTO aux_model (id, name, current_version, path, approach, created_at, updated_at) VALUES (9, 'side', null, 'data/models/side/weight.pt', 'ULTRALYTICS', '2024-09-06 08:24:26', '2024-09-06 08:24:26');
INSERT INTO aux_model (id, name, current_version, path, approach, created_at, updated_at) VALUES (10, 'skeleton', null, 'data/models/skeleton/weight.pt', 'ULTRALYTICS', '2024-09-06 08:24:26', '2024-09-06 08:24:26');
INSERT INTO aux_model (id, name, current_version, path, approach, created_at, updated_at) VALUES (11, 'stamp', null, 'data/models/stamp/weight.pt', 'ULTRALYTICS', '2024-09-06 08:24:26', '2024-09-06 08:24:26');


create table model_update_history
(
    id              int auto_increment
        primary key,
    model_id        int         not null,
    current_version varchar(50) not null,
    update_version  varchar(50) not null,
    constraint model_update_history_model_info_id_fk
        foreign key (model_id) references model_info (id)
);

rename table model_info to aux_model;

alter table aux_model
    add path varchar(256) not null after current_version;

alter table aux_model
    add approach varchar(256) not null after path;



