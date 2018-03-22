/*
Navicat MySQL Data Transfer

Source Server         : 10.82.33.150
Source Server Version : 50634
Source Host           : 10.82.33.150:3306
Source Database       : tts

Target Server Type    : MYSQL
Target Server Version : 50634
File Encoding         : 65001

Date: 2018-03-08 11:10:24
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for tts_config
-- ----------------------------
DROP TABLE IF EXISTS `tts_config`;
CREATE TABLE `tts_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `config_key` varchar(50) DEFAULT NULL COMMENT '缓存key',
  `config_value` varchar(50) DEFAULT NULL COMMENT '缓存value',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='同步任务数据缓存表';

-- ----------------------------
-- Table structure for tts_shop_stock_file
-- ----------------------------
DROP TABLE IF EXISTS `tts_shop_stock_file`;
CREATE TABLE `tts_shop_stock_file` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `file_name` varchar(100) NOT NULL COMMENT '库存文件名称',
  `sync_start_time` timestamp NULL DEFAULT NULL COMMENT '同步开始时间',
  `sync_end_time` timestamp NULL DEFAULT NULL COMMENT '同步结束时间',
  `deleted` int(1) NOT NULL DEFAULT '0' COMMENT '是否有效: 0-有效 1-无效',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='闪电送库存同步文件记录表';

-- ----------------------------
-- Table structure for tts_shop_stock_log_01
-- ----------------------------
DROP TABLE IF EXISTS `tts_shop_stock_log_01`;
CREATE TABLE `tts_shop_stock_log_01` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `wat_sku_code` varchar(15) DEFAULT NULL COMMENT 'sku编码',
  `stock_code` varchar(15) DEFAULT NULL COMMENT '库存号',
  `stock_num` int(10) DEFAULT '0' COMMENT '库存数',
  `stock_generate_time` timestamp NULL DEFAULT NULL COMMENT '库存生成时间',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `index_wat_sku_code` (`wat_sku_code`) USING BTREE,
  KEY `index_stock_code` (`stock_code`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='闪电送库存变更记录表';

-- ----------------------------
-- Table structure for tts_shop_stock_log_02
-- ----------------------------
DROP TABLE IF EXISTS `tts_shop_stock_log_02`;
CREATE TABLE `tts_shop_stock_log_02` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `wat_sku_code` varchar(15) DEFAULT NULL COMMENT 'sku编码',
  `stock_code` varchar(15) DEFAULT NULL COMMENT '库存号',
  `stock_num` int(10) DEFAULT '0' COMMENT '库存数',
  `stock_generate_time` timestamp NULL DEFAULT NULL COMMENT '库存生成时间',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `index_wat_sku_code` (`wat_sku_code`) USING BTREE,
  KEY `index_stock_code` (`stock_code`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='闪电送库存变更记录表';

-- ----------------------------
-- Table structure for tts_shop_stock_log_03
-- ----------------------------
DROP TABLE IF EXISTS `tts_shop_stock_log_03`;
CREATE TABLE `tts_shop_stock_log_03` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `wat_sku_code` varchar(15) DEFAULT NULL COMMENT 'sku编码',
  `stock_code` varchar(15) DEFAULT NULL COMMENT '库存号',
  `stock_num` int(10) DEFAULT '0' COMMENT '库存数',
  `stock_generate_time` timestamp NULL DEFAULT NULL COMMENT '库存生成时间',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `index_wat_sku_code` (`wat_sku_code`) USING BTREE,
  KEY `index_stock_code` (`stock_code`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='闪电送库存变更记录表';

-- ----------------------------
-- Table structure for tts_shop_stock_log_04
-- ----------------------------
DROP TABLE IF EXISTS `tts_shop_stock_log_04`;
CREATE TABLE `tts_shop_stock_log_04` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `wat_sku_code` varchar(15) DEFAULT NULL COMMENT 'sku编码',
  `stock_code` varchar(15) DEFAULT NULL COMMENT '库存号',
  `stock_num` int(10) DEFAULT '0' COMMENT '库存数',
  `stock_generate_time` timestamp NULL DEFAULT NULL COMMENT '库存生成时间',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `index_wat_sku_code` (`wat_sku_code`) USING BTREE,
  KEY `index_stock_code` (`stock_code`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='闪电送库存变更记录表';

-- ----------------------------
-- Table structure for tts_shop_stock_log_05
-- ----------------------------
DROP TABLE IF EXISTS `tts_shop_stock_log_05`;
CREATE TABLE `tts_shop_stock_log_05` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `wat_sku_code` varchar(15) DEFAULT NULL COMMENT 'sku编码',
  `stock_code` varchar(15) DEFAULT NULL COMMENT '库存号',
  `stock_num` int(10) DEFAULT '0' COMMENT '库存数',
  `stock_generate_time` timestamp NULL DEFAULT NULL COMMENT '库存生成时间',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `index_wat_sku_code` (`wat_sku_code`) USING BTREE,
  KEY `index_stock_code` (`stock_code`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='闪电送库存变更记录表';

-- ----------------------------
-- Table structure for tts_shop_stock_log_06
-- ----------------------------
DROP TABLE IF EXISTS `tts_shop_stock_log_06`;
CREATE TABLE `tts_shop_stock_log_06` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `wat_sku_code` varchar(15) DEFAULT NULL COMMENT 'sku编码',
  `stock_code` varchar(15) DEFAULT NULL COMMENT '库存号',
  `stock_num` int(10) DEFAULT '0' COMMENT '库存数',
  `stock_generate_time` timestamp NULL DEFAULT NULL COMMENT '库存生成时间',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `index_wat_sku_code` (`wat_sku_code`) USING BTREE,
  KEY `index_stock_code` (`stock_code`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='闪电送库存变更记录表';

-- ----------------------------
-- Table structure for tts_shop_stock_log_07
-- ----------------------------
DROP TABLE IF EXISTS `tts_shop_stock_log_07`;
CREATE TABLE `tts_shop_stock_log_07` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `wat_sku_code` varchar(15) DEFAULT NULL COMMENT 'sku编码',
  `stock_code` varchar(15) DEFAULT NULL COMMENT '库存号',
  `stock_num` int(10) DEFAULT '0' COMMENT '库存数',
  `stock_generate_time` timestamp NULL DEFAULT NULL COMMENT '库存生成时间',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `index_wat_sku_code` (`wat_sku_code`) USING BTREE,
  KEY `index_stock_code` (`stock_code`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='闪电送库存变更记录表';

-- ----------------------------
-- Table structure for tts_shop_stock_log_08
-- ----------------------------
DROP TABLE IF EXISTS `tts_shop_stock_log_08`;
CREATE TABLE `tts_shop_stock_log_08` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `wat_sku_code` varchar(15) DEFAULT NULL COMMENT 'sku编码',
  `stock_code` varchar(15) DEFAULT NULL COMMENT '库存号',
  `stock_num` int(10) DEFAULT '0' COMMENT '库存数',
  `stock_generate_time` timestamp NULL DEFAULT NULL COMMENT '库存生成时间',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `index_wat_sku_code` (`wat_sku_code`) USING BTREE,
  KEY `index_stock_code` (`stock_code`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='闪电送库存变更记录表';

-- ----------------------------
-- Table structure for tts_shop_stock_log_09
-- ----------------------------
DROP TABLE IF EXISTS `tts_shop_stock_log_09`;
CREATE TABLE `tts_shop_stock_log_09` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `wat_sku_code` varchar(15) DEFAULT NULL COMMENT 'sku编码',
  `stock_code` varchar(15) DEFAULT NULL COMMENT '库存号',
  `stock_num` int(10) DEFAULT '0' COMMENT '库存数',
  `stock_generate_time` timestamp NULL DEFAULT NULL COMMENT '库存生成时间',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `index_wat_sku_code` (`wat_sku_code`) USING BTREE,
  KEY `index_stock_code` (`stock_code`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='闪电送库存变更记录表';

-- ----------------------------
-- Table structure for tts_shop_stock_log_10
-- ----------------------------
DROP TABLE IF EXISTS `tts_shop_stock_log_10`;
CREATE TABLE `tts_shop_stock_log_10` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `wat_sku_code` varchar(15) DEFAULT NULL COMMENT 'sku编码',
  `stock_code` varchar(15) DEFAULT NULL COMMENT '库存号',
  `stock_num` int(10) DEFAULT '0' COMMENT '库存数',
  `stock_generate_time` timestamp NULL DEFAULT NULL COMMENT '库存生成时间',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `index_wat_sku_code` (`wat_sku_code`) USING BTREE,
  KEY `index_stock_code` (`stock_code`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='闪电送库存变更记录表';

-- ----------------------------
-- Table structure for tts_shop_stock_log_11
-- ----------------------------
DROP TABLE IF EXISTS `tts_shop_stock_log_11`;
CREATE TABLE `tts_shop_stock_log_11` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `wat_sku_code` varchar(15) DEFAULT NULL COMMENT 'sku编码',
  `stock_code` varchar(15) DEFAULT NULL COMMENT '库存号',
  `stock_num` int(10) DEFAULT '0' COMMENT '库存数',
  `stock_generate_time` timestamp NULL DEFAULT NULL COMMENT '库存生成时间',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `index_wat_sku_code` (`wat_sku_code`) USING BTREE,
  KEY `index_stock_code` (`stock_code`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='闪电送库存变更记录表';

-- ----------------------------
-- Table structure for tts_shop_stock_log_12
-- ----------------------------
DROP TABLE IF EXISTS `tts_shop_stock_log_12`;
CREATE TABLE `tts_shop_stock_log_12` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `wat_sku_code` varchar(15) DEFAULT NULL COMMENT 'sku编码',
  `stock_code` varchar(15) DEFAULT NULL COMMENT '库存号',
  `stock_num` int(10) DEFAULT '0' COMMENT '库存数',
  `stock_generate_time` timestamp NULL DEFAULT NULL COMMENT '库存生成时间',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `index_wat_sku_code` (`wat_sku_code`) USING BTREE,
  KEY `index_stock_code` (`stock_code`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='闪电送库存变更记录表';

-- ----------------------------
-- Table structure for tts_shop_stock_log_13
-- ----------------------------
DROP TABLE IF EXISTS `tts_shop_stock_log_13`;
CREATE TABLE `tts_shop_stock_log_13` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `wat_sku_code` varchar(15) DEFAULT NULL COMMENT 'sku编码',
  `stock_code` varchar(15) DEFAULT NULL COMMENT '库存号',
  `stock_num` int(10) DEFAULT '0' COMMENT '库存数',
  `stock_generate_time` timestamp NULL DEFAULT NULL COMMENT '库存生成时间',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `index_wat_sku_code` (`wat_sku_code`) USING BTREE,
  KEY `index_stock_code` (`stock_code`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='闪电送库存变更记录表';

-- ----------------------------
-- Table structure for tts_shop_stock_log_14
-- ----------------------------
DROP TABLE IF EXISTS `tts_shop_stock_log_14`;
CREATE TABLE `tts_shop_stock_log_14` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `wat_sku_code` varchar(15) DEFAULT NULL COMMENT 'sku编码',
  `stock_code` varchar(15) DEFAULT NULL COMMENT '库存号',
  `stock_num` int(10) DEFAULT '0' COMMENT '库存数',
  `stock_generate_time` timestamp NULL DEFAULT NULL COMMENT '库存生成时间',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `index_wat_sku_code` (`wat_sku_code`) USING BTREE,
  KEY `index_stock_code` (`stock_code`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='闪电送库存变更记录表';

-- ----------------------------
-- Table structure for tts_shop_stock_log_15
-- ----------------------------
DROP TABLE IF EXISTS `tts_shop_stock_log_15`;
CREATE TABLE `tts_shop_stock_log_15` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `wat_sku_code` varchar(15) DEFAULT NULL COMMENT 'sku编码',
  `stock_code` varchar(15) DEFAULT NULL COMMENT '库存号',
  `stock_num` int(10) DEFAULT '0' COMMENT '库存数',
  `stock_generate_time` timestamp NULL DEFAULT NULL COMMENT '库存生成时间',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `index_wat_sku_code` (`wat_sku_code`) USING BTREE,
  KEY `index_stock_code` (`stock_code`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='闪电送库存变更记录表';

-- ----------------------------
-- Table structure for tts_shop_stock_log_16
-- ----------------------------
DROP TABLE IF EXISTS `tts_shop_stock_log_16`;
CREATE TABLE `tts_shop_stock_log_16` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `wat_sku_code` varchar(15) DEFAULT NULL COMMENT 'sku编码',
  `stock_code` varchar(15) DEFAULT NULL COMMENT '库存号',
  `stock_num` int(10) DEFAULT '0' COMMENT '库存数',
  `stock_generate_time` timestamp NULL DEFAULT NULL COMMENT '库存生成时间',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `index_wat_sku_code` (`wat_sku_code`) USING BTREE,
  KEY `index_stock_code` (`stock_code`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='闪电送库存变更记录表';

-- ----------------------------
-- Table structure for tts_shop_stock_log_17
-- ----------------------------
DROP TABLE IF EXISTS `tts_shop_stock_log_17`;
CREATE TABLE `tts_shop_stock_log_17` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `wat_sku_code` varchar(15) DEFAULT NULL COMMENT 'sku编码',
  `stock_code` varchar(15) DEFAULT NULL COMMENT '库存号',
  `stock_num` int(10) DEFAULT '0' COMMENT '库存数',
  `stock_generate_time` timestamp NULL DEFAULT NULL COMMENT '库存生成时间',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `index_wat_sku_code` (`wat_sku_code`) USING BTREE,
  KEY `index_stock_code` (`stock_code`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='闪电送库存变更记录表';

-- ----------------------------
-- Table structure for tts_shop_stock_log_18
-- ----------------------------
DROP TABLE IF EXISTS `tts_shop_stock_log_18`;
CREATE TABLE `tts_shop_stock_log_18` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `wat_sku_code` varchar(15) DEFAULT NULL COMMENT 'sku编码',
  `stock_code` varchar(15) DEFAULT NULL COMMENT '库存号',
  `stock_num` int(10) DEFAULT '0' COMMENT '库存数',
  `stock_generate_time` timestamp NULL DEFAULT NULL COMMENT '库存生成时间',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `index_wat_sku_code` (`wat_sku_code`) USING BTREE,
  KEY `index_stock_code` (`stock_code`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='闪电送库存变更记录表';

-- ----------------------------
-- Table structure for tts_shop_stock_log_19
-- ----------------------------
DROP TABLE IF EXISTS `tts_shop_stock_log_19`;
CREATE TABLE `tts_shop_stock_log_19` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `wat_sku_code` varchar(15) DEFAULT NULL COMMENT 'sku编码',
  `stock_code` varchar(15) DEFAULT NULL COMMENT '库存号',
  `stock_num` int(10) DEFAULT '0' COMMENT '库存数',
  `stock_generate_time` timestamp NULL DEFAULT NULL COMMENT '库存生成时间',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `index_wat_sku_code` (`wat_sku_code`) USING BTREE,
  KEY `index_stock_code` (`stock_code`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='闪电送库存变更记录表';

-- ----------------------------
-- Table structure for tts_shop_stock_log_20
-- ----------------------------
DROP TABLE IF EXISTS `tts_shop_stock_log_20`;
CREATE TABLE `tts_shop_stock_log_20` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `wat_sku_code` varchar(15) DEFAULT NULL COMMENT 'sku编码',
  `stock_code` varchar(15) DEFAULT NULL COMMENT '库存号',
  `stock_num` int(10) DEFAULT '0' COMMENT '库存数',
  `stock_generate_time` timestamp NULL DEFAULT NULL COMMENT '库存生成时间',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `index_wat_sku_code` (`wat_sku_code`) USING BTREE,
  KEY `index_stock_code` (`stock_code`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='闪电送库存变更记录表';

-- ----------------------------
-- Table structure for tts_shop_stock_log_21
-- ----------------------------
DROP TABLE IF EXISTS `tts_shop_stock_log_21`;
CREATE TABLE `tts_shop_stock_log_21` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `wat_sku_code` varchar(15) DEFAULT NULL COMMENT 'sku编码',
  `stock_code` varchar(15) DEFAULT NULL COMMENT '库存号',
  `stock_num` int(10) DEFAULT '0' COMMENT '库存数',
  `stock_generate_time` timestamp NULL DEFAULT NULL COMMENT '库存生成时间',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `index_wat_sku_code` (`wat_sku_code`) USING BTREE,
  KEY `index_stock_code` (`stock_code`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='闪电送库存变更记录表';

-- ----------------------------
-- Table structure for tts_shop_stock_log_22
-- ----------------------------
DROP TABLE IF EXISTS `tts_shop_stock_log_22`;
CREATE TABLE `tts_shop_stock_log_22` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `wat_sku_code` varchar(15) DEFAULT NULL COMMENT 'sku编码',
  `stock_code` varchar(15) DEFAULT NULL COMMENT '库存号',
  `stock_num` int(10) DEFAULT '0' COMMENT '库存数',
  `stock_generate_time` timestamp NULL DEFAULT NULL COMMENT '库存生成时间',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `index_wat_sku_code` (`wat_sku_code`) USING BTREE,
  KEY `index_stock_code` (`stock_code`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='闪电送库存变更记录表';

-- ----------------------------
-- Table structure for tts_shop_stock_log_23
-- ----------------------------
DROP TABLE IF EXISTS `tts_shop_stock_log_23`;
CREATE TABLE `tts_shop_stock_log_23` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `wat_sku_code` varchar(15) DEFAULT NULL COMMENT 'sku编码',
  `stock_code` varchar(15) DEFAULT NULL COMMENT '库存号',
  `stock_num` int(10) DEFAULT '0' COMMENT '库存数',
  `stock_generate_time` timestamp NULL DEFAULT NULL COMMENT '库存生成时间',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `index_wat_sku_code` (`wat_sku_code`) USING BTREE,
  KEY `index_stock_code` (`stock_code`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='闪电送库存变更记录表';

-- ----------------------------
-- Table structure for tts_shop_stock_log_24
-- ----------------------------
DROP TABLE IF EXISTS `tts_shop_stock_log_24`;
CREATE TABLE `tts_shop_stock_log_24` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `wat_sku_code` varchar(15) DEFAULT NULL COMMENT 'sku编码',
  `stock_code` varchar(15) DEFAULT NULL COMMENT '库存号',
  `stock_num` int(10) DEFAULT '0' COMMENT '库存数',
  `stock_generate_time` timestamp NULL DEFAULT NULL COMMENT '库存生成时间',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `index_wat_sku_code` (`wat_sku_code`) USING BTREE,
  KEY `index_stock_code` (`stock_code`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='闪电送库存变更记录表';

-- ----------------------------
-- Table structure for tts_shop_stock_log_25
-- ----------------------------
DROP TABLE IF EXISTS `tts_shop_stock_log_25`;
CREATE TABLE `tts_shop_stock_log_25` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `wat_sku_code` varchar(15) DEFAULT NULL COMMENT 'sku编码',
  `stock_code` varchar(15) DEFAULT NULL COMMENT '库存号',
  `stock_num` int(10) DEFAULT '0' COMMENT '库存数',
  `stock_generate_time` timestamp NULL DEFAULT NULL COMMENT '库存生成时间',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `index_wat_sku_code` (`wat_sku_code`) USING BTREE,
  KEY `index_stock_code` (`stock_code`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='闪电送库存变更记录表';

-- ----------------------------
-- Table structure for tts_shop_stock_log_26
-- ----------------------------
DROP TABLE IF EXISTS `tts_shop_stock_log_26`;
CREATE TABLE `tts_shop_stock_log_26` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `wat_sku_code` varchar(15) DEFAULT NULL COMMENT 'sku编码',
  `stock_code` varchar(15) DEFAULT NULL COMMENT '库存号',
  `stock_num` int(10) DEFAULT '0' COMMENT '库存数',
  `stock_generate_time` timestamp NULL DEFAULT NULL COMMENT '库存生成时间',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `index_wat_sku_code` (`wat_sku_code`) USING BTREE,
  KEY `index_stock_code` (`stock_code`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='闪电送库存变更记录表';

-- ----------------------------
-- Table structure for tts_shop_stock_log_27
-- ----------------------------
DROP TABLE IF EXISTS `tts_shop_stock_log_27`;
CREATE TABLE `tts_shop_stock_log_27` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `wat_sku_code` varchar(15) DEFAULT NULL COMMENT 'sku编码',
  `stock_code` varchar(15) DEFAULT NULL COMMENT '库存号',
  `stock_num` int(10) DEFAULT '0' COMMENT '库存数',
  `stock_generate_time` timestamp NULL DEFAULT NULL COMMENT '库存生成时间',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `index_wat_sku_code` (`wat_sku_code`) USING BTREE,
  KEY `index_stock_code` (`stock_code`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='闪电送库存变更记录表';

-- ----------------------------
-- Table structure for tts_shop_stock_log_28
-- ----------------------------
DROP TABLE IF EXISTS `tts_shop_stock_log_28`;
CREATE TABLE `tts_shop_stock_log_28` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `wat_sku_code` varchar(15) DEFAULT NULL COMMENT 'sku编码',
  `stock_code` varchar(15) DEFAULT NULL COMMENT '库存号',
  `stock_num` int(10) DEFAULT '0' COMMENT '库存数',
  `stock_generate_time` timestamp NULL DEFAULT NULL COMMENT '库存生成时间',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `index_wat_sku_code` (`wat_sku_code`) USING BTREE,
  KEY `index_stock_code` (`stock_code`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='闪电送库存变更记录表';

-- ----------------------------
-- Table structure for tts_shop_stock_log_29
-- ----------------------------
DROP TABLE IF EXISTS `tts_shop_stock_log_29`;
CREATE TABLE `tts_shop_stock_log_29` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `wat_sku_code` varchar(15) DEFAULT NULL COMMENT 'sku编码',
  `stock_code` varchar(15) DEFAULT NULL COMMENT '库存号',
  `stock_num` int(10) DEFAULT '0' COMMENT '库存数',
  `stock_generate_time` timestamp NULL DEFAULT NULL COMMENT '库存生成时间',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `index_wat_sku_code` (`wat_sku_code`) USING BTREE,
  KEY `index_stock_code` (`stock_code`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='闪电送库存变更记录表';

-- ----------------------------
-- Table structure for tts_shop_stock_log_30
-- ----------------------------
DROP TABLE IF EXISTS `tts_shop_stock_log_30`;
CREATE TABLE `tts_shop_stock_log_30` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `wat_sku_code` varchar(15) DEFAULT NULL COMMENT 'sku编码',
  `stock_code` varchar(15) DEFAULT NULL COMMENT '库存号',
  `stock_num` int(10) DEFAULT '0' COMMENT '库存数',
  `stock_generate_time` timestamp NULL DEFAULT NULL COMMENT '库存生成时间',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `index_wat_sku_code` (`wat_sku_code`) USING BTREE,
  KEY `index_stock_code` (`stock_code`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='闪电送库存变更记录表';

-- ----------------------------
-- Table structure for tts_shop_stock_log_31
-- ----------------------------
DROP TABLE IF EXISTS `tts_shop_stock_log_31`;
CREATE TABLE `tts_shop_stock_log_31` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `wat_sku_code` varchar(15) DEFAULT NULL COMMENT 'sku编码',
  `stock_code` varchar(15) DEFAULT NULL COMMENT '库存号',
  `stock_num` int(10) DEFAULT '0' COMMENT '库存数',
  `stock_generate_time` timestamp NULL DEFAULT NULL COMMENT '库存生成时间',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `index_wat_sku_code` (`wat_sku_code`) USING BTREE,
  KEY `index_stock_code` (`stock_code`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='闪电送库存变更记录表';

-- ----------------------------
-- Table structure for tts_stock_log
-- ----------------------------
DROP TABLE IF EXISTS `tts_stock_log`;
CREATE TABLE `tts_stock_log` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `wat_sku_code` varchar(15) DEFAULT NULL COMMENT 'sku编码',
  `stock_code` varchar(15) DEFAULT NULL COMMENT '库存号',
  `stock_num` int(10) DEFAULT '0' COMMENT '库存数',
  `stock_generate_time` timestamp NULL DEFAULT NULL COMMENT '库存生成时间',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `index_wat_sku_code` (`wat_sku_code`) USING BTREE,
  KEY `index_stock_code` (`stock_code`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=90466308 DEFAULT CHARSET=utf8 COMMENT='普通sku库存变更记录表';

