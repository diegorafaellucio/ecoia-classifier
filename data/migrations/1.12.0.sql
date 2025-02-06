alter table image
    add carcass_detection_confidence_score decimal(10, 2) null after filter_confidence;

alter table image
    add carcass_intersection_score decimal(10, 2) null after filter_confidence;


alter table image
    add carcass_classification_score decimal(10, 2) null after filter_confidence;

update aux_module set current_version='1.12.0', created_at=now(), updated_at=now() where name='ecoia-classifier'