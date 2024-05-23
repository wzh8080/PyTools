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