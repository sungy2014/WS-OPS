alter table user_db.user_point_redemption add column is_scan_go TINYINT(4) default 0 COMMENT '是否是扫码购，默认为0，扫码购的情况直接销分不走定时任务' after status;
alter table user_db.user_member_card add column is_it_default_card tinyint(4) NOT NULL default 0 comment '是否是IT默认卡，1为是 0为否，默认为0' after is_wechat_card,
add column initial_password varchar(40) NOT NULL default '' comment '初始化密码' after is_wechat_card;

use shop_db;
CREATE TABLE `store_location` (
  `id` bigint(11) NOT NULL AUTO_INCREMENT COMMENT '唯一自增id',
  `location_id` varchar(64) NOT NULL DEFAULT '' COMMENT 'location编号',
  `location_name` varchar(64) NOT NULL DEFAULT '' COMMENT 'location名称',
  `store_number` varchar(64) NOT NULL DEFAULT '' COMMENT '门店编号',
  `baidu_longitude` varchar(64) NOT NULL DEFAULT '' COMMENT '百度经度值 正数东经 负数西经',
  `baidu_latitude` varchar(64) NOT NULL DEFAULT '' COMMENT '百度纬度 正数北纬 负数南纬',
  `bak_longitude` varchar(64) NOT NULL DEFAULT '' COMMENT '备份百度经度值 正数东经 负数西经',
  `bak_latitude` varchar(64) NOT NULL DEFAULT '' COMMENT '备份百度纬度值 正数东经 负数西经',
  `tencent_longitude` varchar(64) NOT NULL DEFAULT '' COMMENT '腾讯经度值 正数东经 负数西经',
  `tencent_latitude` varchar(64) NOT NULL DEFAULT '' COMMENT '腾讯经度值 正数东经 负数西经',
  `gaode_longitude` varchar(64) NOT NULL DEFAULT '' COMMENT '高德经度值 正数东经 负数西经',
  `gaode_latitude` varchar(64) NOT NULL DEFAULT '' COMMENT '高德纬度 正数北纬 负数南纬',
  `is_need_degauss` tinyint(2) NOT NULL DEFAULT '0' COMMENT '是否需要消磁(1:需要,0:不需要)',
  `delete_mark` tinyint(2) NOT NULL DEFAULT '0' COMMENT '逻辑删除标志0未删除1已删除',
  `gmt_created` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `gmt_modified` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`),
  KEY `idx_location_id` (`location_id`) USING BTREE,
  KEY `idx_store_number` (`store_number`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;