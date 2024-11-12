CREATE TABLE `cuts_grading` (
  `id` int NOT NULL AUTO_INCREMENT,
  `image_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `aux_grading_id` int NOT NULL,
  `cut_id` int NOT NULL,
  `carcacass_cut_classification_correlation` enum('POSITIVE','NEGATIVE','IN_COMPLIANCE') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `created_at` datetime DEFAULT (now()),
  `updated_at` datetime DEFAULT (now()),
  PRIMARY KEY (`id`),
  UNIQUE KEY `image_id` (`image_id`)
) ENGINE=InnoDB AUTO_INCREMENT=212 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


INSERT INTO aux_grading (id,name,description,score,label,color_id,show_on_front) VALUES (200,'Erro200','Picanha sem classificada','200','200',15,0);
INSERT INTO aux_grading (id,name,description,score,label,color_id,show_on_front) VALUES (201,'Erro201','Picanha com lesão','201','201',15,0);
INSERT INTO aux_grading (id,name,description,score,label,color_id,show_on_front) VALUES (202,'Erro202','Picanha com falha','202','202',15,0);
INSERT INTO aux_grading (id,name,description,score,label,color_id,show_on_front) VALUES (203,'Erro203','Picanha com falha/lesão','203','203',15,0);