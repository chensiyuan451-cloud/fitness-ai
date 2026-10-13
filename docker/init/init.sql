-- ============================================================
-- fitness-ai 数据库初始化脚本
-- MySQL 容器首次启动时自动执行（docker/init 挂载到 docker-entrypoint-initdb.d）
-- 设计说明见 docs/数据库设计.md
-- ============================================================

CREATE DATABASE IF NOT EXISTS `fitness`
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE `fitness`;

-- ------------------------------------------------------------
-- 1. 用户表
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `user` (
  `id`            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键',
  `username`      VARCHAR(50)     NOT NULL                COMMENT '登录用户名',
  `email`         VARCHAR(120)    DEFAULT NULL            COMMENT '邮箱',
  `password_hash` VARCHAR(255)    NOT NULL                COMMENT '密码哈希（bcrypt，绝不存明文）',
  `nickname`      VARCHAR(50)     DEFAULT NULL            COMMENT '昵称',
  `gender`        TINYINT         DEFAULT 0               COMMENT '0未知 1男 2女',
  `height_cm`     DECIMAL(5,1)    DEFAULT NULL            COMMENT '身高 cm',
  `weight_kg`     DECIMAL(5,2)    DEFAULT NULL            COMMENT '体重 kg',
  `created_at`    DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at`    DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_username` (`username`),
  UNIQUE KEY `uk_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- ------------------------------------------------------------
-- 2. 动作表（卧推、深蹲、硬拉……）
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `exercise` (
  `id`          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name`        VARCHAR(80)     NOT NULL                COMMENT '动作名称，如 杠铃卧推',
  `body_part`   VARCHAR(20)     NOT NULL                COMMENT '部位：胸/背/腿/肩/手臂/核心/有氧',
  `equipment`   VARCHAR(30)     DEFAULT NULL            COMMENT '器械：杠铃/哑铃/器械/自重/绳索',
  `is_compound` TINYINT(1)      NOT NULL DEFAULT 0      COMMENT '是否复合动作',
  `user_id`     BIGINT UNSIGNED DEFAULT NULL            COMMENT 'NULL=系统预置动作；否则为用户自定义',
  `created_at`  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_name_user` (`name`, `user_id`),
  KEY `idx_body_part` (`body_part`),
  CONSTRAINT `fk_exercise_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='训练动作表';

-- ------------------------------------------------------------
-- 3. 训练记录表（一次训练 = 一条记录，包含多个动作）
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `workout` (
  `id`           BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键',
  `user_id`      BIGINT UNSIGNED NOT NULL                COMMENT '所属用户',
  `workout_date` DATE            NOT NULL                COMMENT '训练日期',
  `duration_min` SMALLINT UNSIGNED DEFAULT NULL          COMMENT '训练时长（分钟）',
  `mood`         TINYINT         DEFAULT NULL            COMMENT '感受 1-5',
  `note`         VARCHAR(500)    DEFAULT NULL            COMMENT '训练备注',
  `created_at`   DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at`   DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_date` (`user_id`, `workout_date`),
  KEY `idx_user_date` (`user_id`, `workout_date`),
  CONSTRAINT `fk_workout_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='训练记录表';

-- ------------------------------------------------------------
-- 4. 组表（训练的最小单位：某个动作做了第几组、多重、几次）
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `workout_set` (
  `id`          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键',
  `workout_id`  BIGINT UNSIGNED NOT NULL                COMMENT '所属训练记录',
  `exercise_id` BIGINT UNSIGNED NOT NULL                COMMENT '动作',
  `set_index`   TINYINT UNSIGNED NOT NULL               COMMENT '第几组，从 1 开始',
  `weight_kg`   DECIMAL(6,2)    NOT NULL DEFAULT 0      COMMENT '重量 kg（自重填 0）',
  `reps`        SMALLINT UNSIGNED NOT NULL              COMMENT '次数',
  `rpe`         TINYINT         DEFAULT NULL            COMMENT '主观疲劳度 1-10',
  `is_warmup`   TINYINT(1)      NOT NULL DEFAULT 0      COMMENT '是否热身组',
  `created_at`  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_workout_exercise_set` (`workout_id`, `exercise_id`, `set_index`),
  KEY `idx_workout` (`workout_id`),
  KEY `idx_exercise` (`exercise_id`),
  CONSTRAINT `fk_set_workout`  FOREIGN KEY (`workout_id`)  REFERENCES `workout` (`id`)  ON DELETE CASCADE,
  CONSTRAINT `fk_set_exercise` FOREIGN KEY (`exercise_id`) REFERENCES `exercise` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='训练组表';

-- ------------------------------------------------------------
-- 预置常用动作（user_id = NULL 表示系统动作）
-- ------------------------------------------------------------
INSERT IGNORE INTO `exercise` (`name`, `body_part`, `equipment`, `is_compound`, `user_id`) VALUES
  ('杠铃卧推', '胸', '杠铃', 1, NULL),
  ('哑铃卧推', '胸', '哑铃', 1, NULL),
  ('上斜杠铃卧推', '胸', '杠铃', 1, NULL),
  ('蝴蝶机夹胸', '胸', '器械', 0, NULL),
  ('引体向上', '背', '自重', 1, NULL),
  ('杠铃划船', '背', '杠铃', 1, NULL),
  ('高位下拉', '背', '器械', 1, NULL),
  ('坐姿划船', '背', '器械', 1, NULL),
  ('杠铃深蹲', '腿', '杠铃', 1, NULL),
  ('腿举', '腿', '器械', 1, NULL),
  ('罗马尼亚硬拉', '腿', '杠铃', 1, NULL),
  ('腿弯举', '腿', '器械', 0, NULL),
  ('站姿提踵', '腿', '器械', 0, NULL),
  ('杠铃推举', '肩', '杠铃', 1, NULL),
  ('哑铃侧平举', '肩', '哑铃', 0, NULL),
  ('面拉', '肩', '绳索', 0, NULL),
  ('杠铃弯举', '手臂', '杠铃', 0, NULL),
  ('绳索下压', '手臂', '绳索', 0, NULL),
  ('平板支撑', '核心', '自重', 0, NULL),
  ('卷腹', '核心', '自重', 0, NULL),
  ('跑步机', '有氧', '器械', 0, NULL),
  ('划船机', '有氧', '器械', 0, NULL);
