create table db_industry.monitor_restart_system(
  id int PRIMARY KEY AUTO_INCREMENT,
  application varchar(100),
  restarded_at datetime default CURRENT_TIMESTAMP not null
);