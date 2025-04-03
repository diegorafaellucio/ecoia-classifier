ALTER TABLE bruise add COLUMN region_bruise_code VARCHAR(10) not null  DEFAULT 'D1';
update aux_module set current_version='1.13.0', updated_at=now() where name='ecoia-classifier'
