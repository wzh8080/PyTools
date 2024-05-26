'01' == '%精校%' ;
'02' == '%校对%' ;
'03' == '%初校%' ;
'04' == '%整理%' ;
'05' == '%网络%' ;
'06' == '%实体%' ;
'00' == '无状态' ;

-- drop table book_list ;
CREATE TABLE book_list (
  id int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  web_name varchar(255) COMMENT '网站',
  title varchar(255) NOT NULL COMMENT '书名',
  author varchar(255) COMMENT '作者',
  book_url varchar(255) NOT NULL COMMENT '书籍地址',
  img_url varchar(255) COMMENT '封面地址',
  publication_date date DEFAULT NULL COMMENT '出版日期',
  genre varchar(255) DEFAULT NULL COMMENT '书籍类型',
  description text COMMENT '书籍描述',
  input_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '插入时间',
  update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (id)
) COMMENT='书籍列表';

CREATE TABLE book_list_bqg (
  id int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  web_name varchar(255) COMMENT '网站',
  title varchar(255) NOT NULL COMMENT '书名',
  author varchar(255) COMMENT '作者',
  book_url varchar(255) NOT NULL COMMENT '书籍地址',
  img_url varchar(255) COMMENT '封面地址',
  publication_date date DEFAULT NULL COMMENT '出版日期',
  genre varchar(255) DEFAULT NULL COMMENT '书籍类型',
  description text COMMENT '书籍描述',
  input_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '插入时间',
  update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (id)
) COMMENT='书籍列表';

--drop table book_catalog;
CREATE TABLE book_catalog (
  id int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  website varchar(255) NOT NULL COMMENT '网站站点',
  catalog_url varchar(255) NOT NULL  COMMENT '目录地址',
  total_page int(6) NOT NULL COMMENT '总页数',
  next_page int(6) NOT NULL DEFAULT 1 COMMENT '待查询页',
  book_type varchar(255) DEFAULT NULL COMMENT '书籍分类',
  input_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '插入时间',
  update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (id)
) COMMENT='目录';

-- 知轩藏书 书籍下载列表
--drop table book_list_zxcs;
CREATE TABLE book_list_zxcs (
  id int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  catalog_url varchar(255)COMMENT '目录地址',
  title varchar(255) COMMENT '书名',
  author varchar(255) COMMENT '作者',
  book_url varchar(255) NOT NULL COMMENT '书籍地址（可获取图片）',
  sele_url varchar(255) COMMENT '下载选择页',
  down_url varchar(255) COMMENT '书籍下载地址',
  img_url varchar(255) COMMENT '封面地址',
  publication_date date DEFAULT NULL COMMENT '出版日期',
  book_type varchar(255) COMMENT '书籍分类',
  content_type varchar(255) COMMENT '内容类型',
  finish_flag tinyint(1) COMMENT '完结状态:1是0否',
  description text COMMENT '书籍描述',
  input_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '插入时间',
  update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (id)
) COMMENT='知轩藏书书籍下载列表';
-- 修改字段长度
alter table book_list_zxcs modify column title varchar(1200);
-- 添加字段
ALTER TABLE book_list_zxcs ADD COLUMN book_id int(11) AFTER catalog_url;
ALTER TABLE book_list_zxcs ADD COLUMN down_flag tinyint(1) COMMENT '下载标志:1是0否' AFTER finish_flag;
ALTER TABLE book_list_zxcs ADD COLUMN check_flag tinyint(1) DEFAULT 0 COMMENT '精校标志:1是0否' AFTER content_type;
-- 修改字段为默认值=0
ALTER TABLE book_list_zxcs MODIFY COLUMN finish_flag tinyint(1) DEFAULT 0;
ALTER TABLE book_list_zxcs MODIFY COLUMN down_flag tinyint(1) DEFAULT 0;
ALTER TABLE book_list_zxcs MODIFY COLUMN check_flag tinyint(1) DEFAULT 0;
-- 修改字段名称
ALTER TABLE book_list_zxcs CHANGE COLUMN book_tpye book_type VARCHAR(255);
ALTER TABLE book_list_zxcs CHANGE COLUMN content_tpye content_type VARCHAR(255);
