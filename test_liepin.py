# !/usr/bin/python
# -*- coding:utf-8 -*-
__author__ = 'Tao Jiang'
from mongo_connect import *
from handling_liepin import handle_liepin
import datetime
import time
import logging

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s] %(levelname)s %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                filename='test_liepin_log.log',
                filemode='a')
# 输出到屏幕
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


def test_liepin():
	"""
	导入解析liepin简历方法
	:param min_time:
	:param max_time:
	:return:
	"""
	src_conn = connect(database="2013_resume", collection="2013_liepinwang_doc_resume", host="192.168.3.224", port=27017)

	dest_conn = connect(database="2013", collection="liepin_resume", host="192.168.3.224", port=27017)
	page = 0
	page_size = 1000
	temp = 0
	all_temp = 0
	start = datetime.datetime.now()
	while True:
		try:
			# 检测mongo 连接是否正确，不正确抛出异常
			if src_conn is None:
				raise pymongo.errors.ServerSelectionTimeoutError
			# 纷简历通过爬取时间"last_crawled_time" 来导入
			db_cursor = src_conn.find().skip(page_size * page).limit(page_size)
		# 捕获mongo 连接超时 异常
		except pymongo.errors.ServerSelectionTimeoutError, e:
			logging.error(u"数据库连接超时， 异常信息： %s" % e.message)
			# 暂停1小时再次检测连接是否正常
			time.sleep(3590)
			# 重新建立到数据库的连接
			src_conn = connect(database="2013_resume", collection="2013_liepinwang_doc_resume", host="192.168.3.224", port=27017)
			dest_conn = connect(database="2013", collection="liepin_resume", host="192.168.3.224", port=27017)
			continue
		except Exception, e:
			logging.error(u"读取数据出现异常， 异常信息： %s" % e.message)
			continue

		page += 1
		temp = 0
		for d in db_cursor:
			try:
				resume = {}
				# 解析简历
				resume = handle_liepin(d)
				if resume != {}:
					cv_id = resume.get("cv_id")
					source = resume.get("source")
					if cv_id is None or source is None:
						continue
					# # 调用pymongo 的update 方法，如果已有简历数据则更新覆盖，反之就插入
					# dest_conn.update({"cv_id": cv_id, "source": source}, resume, True, False)
					# 判断连接是否正常，连接失败抛出异常
					if dest_conn is None:
						raise pymongo.errors.ServerSelectionTimeoutError
					# 先判断数据库中是否有该简历， 如果有则判断该简历的name、phone、email 是否存在，以免被覆盖
					result = dest_conn.find_one({"cv_id": cv_id, "source": source})
					# 找到存在的简历
					if result is not None:
						# 若已有重复简历，需要提取出简历中的name、phone、email 字段，防止被新简历覆盖
						# 名字
						if resume.get("name") == "" and (result.get("name") != "" and result.get("name") != None):
							resume["name"] == result.get("name")
						# 电话
						if resume.get("phone") == "" and (result.get("phone") != "" and result.get("phone") != None):
							resume["phone"] == result.get("phone")
						# 邮件信息
						if resume.get("email") == "" and (result.get("email") != "" and result.get("email") != None):
							resume["email"] == result.get("email")

					# # 调用pymongo 的update 方法，如果已有简历数据则更新覆盖，反之就插入
					dest_conn.update({"cv_id": cv_id, "source": source}, resume, True, False)

			# 插入数据时 数据库连接超时
			except pymongo.errors.ServerSelectionTimeoutError, e:
				logging.error(u" 插入数据时 数据库连接超时， 异常信息： %s" % e.message)
			except:
				if isinstance(resume, dict) and resume.has_key("cv_id"):
					logging.error(u"数据解析异常， 异常数据Cv_id：%s" % resume["cv_id"])
				else:
					logging.error(u"数据解析异常,解析过程中出现错误!")

			temp += 1
			all_temp += 1
		end = datetime.datetime.now()
		logging.info(u"完成导入 %s 条数据，一共耗时 %d 秒 ！" % (all_temp, (end - start).seconds))
		# 判断是否是已经读取完数据，因为是分页查询的，每页1000条数据，若不满1000条则是最后的数据
		if temp % page_size != 0 or temp == 0:
			logging.info(u"---------- 已经导入所有数据")
			break

if __name__ == '__main__':
    test_liepin()