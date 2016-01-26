# !/usr/bin/python
# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from handling_salary_time import *
from scrapy import Selector
import uuid
import re
import time


# 解析简历函数
def handle_liepin(d={}):
	"""
	解析猎聘简历的方法，最后返回解析好的dict 类型resume
	:param d:
	:return:
	"""
	resume = {"resume_id": "", "cv_id": "", "phone": "", "name": "", "email": "", "create_time": long(0),
			  "crawled_time": long(0), "update_time": "", "resume_keyword": "", "resume_img": "",
			  "self_introduction": "", "expect_city": "", "expect_industry": "", "expect_salary": "",
			  "expect_position": "", "expect_job_type": "", "expect_occupation": "", "starting_date": "", "gender": "",
			  "age": "", "degree": "", "enterprise_type": "", "work_status": "", "source": "", "college_name": "",
			  "profession_name": "", "last_enterprise_name": "", "last_position_name": "",
			  "last_enterprise_industry": "", "last_enterprise_time": "", "last_enterprise_salary": "",
			  "last_year_salary": "", "hometown": "", "living": "", "birthday": "", "marital_status": "",
			  "politics": "", "work_year": "", "height": "", "interests": "", "career_goal": "", "specialty": "",
			  "special_skills": "", "drive_name": "", "country": "", "osExperience": "", "status": "0", "flag": "0",
			  "dimension_flag": False, "version": [], "keyword_id": [], "resumeUpdateTimeList": [], "educationList": [],
			  "workExperienceList": [], "projectList": [], "trainList": [], "certificateList": [], "languageList": [],
			  "skillList": [], "awardList": [], "socialList": [], "schoolPositionList": [], "productList": [],
			  "scholarshipList": []}

	"""
	简历resume 对象属性的默认值
	设置默认值的作用是保证与数据库中其他数据类型的数据格式进行统一化
	"""
	# 来源
	resume["source"] = u"猎聘"
	# 状态
	resume["status"] = "0"
	# 标志
	resume["flag"] = "0"
	# dimension_flag
	resume["dimension_flag"] = False
	# 简历ID
	resume["resume_id"] = str(uuid.uuid4()).replace("-", "")
	# 更新时间
	resume["update_time"] = "2014-12-31"
	# 爬取时间
	resume["crawled_time"] = long(1420002000000)
	# create_time
	resume["create_time"] = long(time.time() * 1000)

	if "content" in d and len(d["content"]) > 0:
		main_info = Selector(text=d["content"]).xpath("body")
		# print main_info[0].extract()
		if len(main_info) > 0:
			handle_html(resume, main_info[0])
		else:
			resume = {}

	# 返回解析好的简历 resume
	return resume


def handle_html(resume, main_info):
	"""
	处理简历主要信息
	:param resume:
	:param main_info:
	:return:
	"""
	# 解析简历cv_id update_time
	cvInfo = main_info.xpath('.//table[@width="690"]//td[@valign="bottom"]//text()')
	if len(cvInfo) > 0:
		temp = cvInfo[0].extract().strip()
	temp2 = temp.split(u"   ")
	if len(temp2) > 1:
		# 解析简历cv_id
		id_info = re.match(u"简历编号: (\d+)", temp2[0])
		if id_info is not None:
			resume["cv_id"] = id_info.group(1)
		# 解析 update_time
		update_time = re.match(u"最后更新: (\d{4}-\d{2}-\d{2})", temp2[1])
		if update_time:
			resume["update_time"] = update_time.group(1)

	infos = main_info.xpath('.//table[@width = "660"]//table[@width="640"]')
	# print infos[0].extract()
	if len(infos) > 0:
		brief_info = infos.xpath(
			'tr/td[@height="20"][contains(@style,"font-weight:bold; border-bottom:1px dashed #ccc; font-size:14px")]')
		for i in brief_info:
			temp = i.extract()
			# 解析基本信息
			if u"基本信息" in temp:
				info = i.xpath("../following-sibling::tr[1]")
				if len(info) > 0:
					handle_brief_info(resume, info[0])
			elif u"目前职位概况" in temp:
				# 解析目前职位概况
				info = i.xpath("../following-sibling::tr[1]")
				if len(info) > 0:
					# print info[0].extract()
					handle_current_position(resume, info[0])
			elif u"求职意向" in temp:
				# 解析求职意向
				info = i.xpath("../following-sibling::tr[1]")
				if len(info) > 0:
					# print info[0].extract()
					handle_career_info(resume, info[0])
			elif u"自我评价" in temp:
				# 解析自我评价
				info = i.xpath("../following-sibling::tr[1]")
				if len(info) > 0:
					# print info[0].extract()
					handle_self_intro(resume, info[0])
			elif u"教育经历" in temp:
				# 解析教育经历
				info = i.xpath("../following-sibling::tr[1]")
				if len(info) > 0:
					# print info[0].extract()
					handle_education_info(resume, info[0])
			elif u"工作经历" in temp:
				# 解析工作经历
				info = i.xpath("../following-sibling::tr[1]")
				if len(info) > 0:
					# print info[0].extract()
					handle_work_info(resume, info[0])
			elif u"项目经历" in temp:
				# 解析项目经历
				info = i.xpath("../following-sibling::tr[1]")
				if len(info) > 0:
					# print info[0].extract()
					handle_project_info(resume, info[0])
			elif u"语言能力" in temp:
				# 解析语言能力
				info = i.xpath("../following-sibling::tr[1]")
				if len(info) > 0:
					# print info[0].extract()
					handle_language_info(resume, info[0])
			elif u"附加信息" in temp:
				# 解析简历附加信息
				info = i.xpath("../following-sibling::tr[1]")
				if len(info) > 0:
					extra = info[0].xpath("string(.)")
					if len(extra) > 0:
						resume["extra_infomation"] = extra[0].extract().strip()

	if len(resume["educationList"]) > 0:
		# 设置学校名
		if "college_name" in resume["educationList"][0]:
			resume["college_name"] = resume["educationList"][0]["college_name"]
		# 设置专业名
		if "profession_name" in resume["educationList"][0]:
			resume["profession_name"] = resume["educationList"][0]["profession_name"]


# 解析基本信息
def handle_brief_info(resume, info):
	# 解析姓名
	name_info = info.xpath(".//td[@width= '140']/text()")
	if len(name_info) > 0:
		resume["name"] = name_info[0].extract().strip()
	if re.match('^\*+$', resume["name"]):
		resume["name"] = ""


	# 解析工作时间
	work_year = info.xpath('.//td[@width="90"]/following-sibling::td[1]//text()')
	if len(work_year) > 0:
		work_year = work_year[0].extract().strip()
		resume["work_year"] = handle_work_year(work_year)

	# 解析联系电话
	phone_info = info.xpath('.//td[@height="20"][contains(., "联系电话")]/following-sibling::td[1]')
	if len(phone_info) > 0:
		phone_text = phone_info[0].xpath("string()")
		if len(phone_text) > 0:
			resume["phone"] = phone_text[0].extract().replace("-", "").strip()
	if re.match('^\*+$', resume["phone"]):
		resume["phone"] = ""
	# 去掉‘不公开’ 字段
	if re.match(u'不公开', resume["phone"]):
		resume["phone"] = u""
	# 排除错误项
	if len(resume["phone"]) < 5:
		resume["phone"] = ""


	# 解析性别
	gender_info = info.xpath('.//td[contains(., "性 别")]/following-sibling::td[1]/text()')
	if len(gender_info) > 0:
		resume["gender"] = gender_info[0].extract().strip()


	# 解析年龄
	age_info = info.xpath('.//td[contains(., "年 龄")]/following-sibling::td[1]/text()')
	if len(age_info) > 0:
		resume["age"] = age_info[0].extract().replace(u"岁", "").strip()

	# 解析邮件
	email_info = info.xpath('.//td[contains(., "电子邮件")]/following-sibling::td[1]/text()')
	if len(email_info) > 0:
		resume["email"] = email_info[0].extract().strip()
	# 排除 ***** 错误
	if re.match('^\*+$', resume["email"]):
		resume["email"] = ""
	# 去掉‘不公开’ 字段
	if re.match(u'不公开', resume["email"]):
		resume["email"] = ""


	# 解析学历
	degree_info = info.xpath('.//td[contains(.,"教育程度")]/following-sibling::td[1]/text()')
	if len(degree_info) > 0:
		resume["degree"] = degree_info[0].extract().strip()

	# 解析目前状态
	work_status = info.xpath('.//td[contains(.,"目前状态")]/following-sibling::td[1]/text()')
	if len(work_status) > 0:
		resume["work_status"] = work_status[0].extract().strip()


	# 解析婚姻状况
	marital_status = info.xpath('.//td[contains(.,"婚姻状况")]/following-sibling::td[1]/text()')
	if len(marital_status) > 0:
		resume["marital_status"] = marital_status[0].extract().strip()


# 解析目前职位概况
def handle_current_position(resume, info):
	# 解析公司名称
	last_enterprise_name = info.xpath('.//td[contains(., "公司名称")]/following-sibling::td[1]//text()')
	if len(last_enterprise_name) > 0:
		resume["last_enterprise_name"] = last_enterprise_name[0].extract().strip()

	# 排除错误项
	if re.match("^\d+$", resume["last_enterprise_name"]):
		resume["last_enterprise_name"] = ""

	# 解析所任职位
	last_position_name = info.xpath('.//td[contains(., "所任职位")]/following-sibling::td[1]/text()')
	if len(last_position_name) > 0:
		resume["last_position_name"] = last_position_name[0].extract().strip()

	# 解析所在行业
	last_enterprise_industry = info.xpath('.//td[contains(., "所在行业")]/following-sibling::td[1]/text()')
	if len(last_enterprise_industry) > 0:
		resume["last_enterprise_industry"] = last_enterprise_industry[0].extract().strip()

	# 解析工作地点
	work_place = info.xpath('.//td[contains(., "工作地点")]/following-sibling::td[1]/text()')
	if len(work_place) > 0:
		resume["work_place"] = work_place[0].extract().strip()

	# 解析目前年薪
	last_year_salary = info.xpath('.//td[contains(., "目前年薪")]/following-sibling::td[1]/text()')
	if len(last_year_salary) > 0:
		last_salary = last_year_salary[0].extract().strip()
		if last_salary == u"保密":
			resume["last_year_salary"] = ""
		if re.match(u"(\d+)元/月 \* (\d+)个月", last_salary):
			temp = re.match("(\d+)元/月 \* (\d+)个月", last_salary)
			salary = str(int(float(temp.group(1)) * float(temp.group(2)) / 10000)) + u"万"
			resume["last_year_salary"] = salary


# 解析求职意向
def handle_career_info(resume, info):
	# 解析期望月薪
	expect_salary = info.xpath('.//td[contains(., "期望月薪")]/following-sibling::td[1]/text()')
	if len(expect_salary) > 0:
		salary = expect_salary[0].extract().strip()
		resume["expect_salary"] = handle_salary(salary)
		if re.match("^\d{1,2}$", resume["expect_salary"]):
			resume["expect_salary"] = u"面议"

		# 解析期望从事行业
		expect_industry = info.xpath('.//td[contains(., "期望从事行业")]/following-sibling::td[1]/text()')
	if len(expect_industry) > 0:
		resume["expect_industry"] = expect_industry[0].extract().replace(";", ",").strip()

	# 解析期望从事职业
	expect_position = info.xpath('.//td[contains(., "期望从事职业")]/following-sibling::td[1]/text()')
	if len(expect_position) > 0:
		resume["expect_position"] = expect_position[0].extract().replace(";", ",").strip()

	# 解析期望工作地点
	expect_city = info.xpath('.//td[contains(., "期望工作地点")]/following-sibling::td[1]/text()')
	if len(expect_city) > 0:
		resume["expect_city"] = expect_city[0].extract().strip()


# 解析自我评价
def handle_self_intro(resume, info):
	# 解析自我评价
	self_intro = info.xpath(".//table//td")
	if len(self_intro) > 0:
		intro_info = self_intro[0].xpath("string(.)")
		if len(intro_info) > 0:
			resume["self_introduction"] = intro_info[0].extract().strip()


# 解析教育经历
def handle_education_info(resume, info):
	"""
	处理教育经历方法
	:param resume:
	:param info:
	:return:
	"""
	infos = info.xpath(".//table/tr")
	for i in range(len(infos)):
		eduList = {"start_date": "", "end_date": "", "degree": "", "college_name": "", "profession_name": "", "desc": ""}
		temp = infos[i].xpath(".//td")
		if len(temp) == 4:
			# 开始、 结束时间解析
			time_info = temp[0].xpath("string(.)")
			if len(time_info) > 0:
				time_str = time_info[0].extract().strip()
				s = time_str.split("-")
				if len(s) == 2:
					eduList["start_date"] = s[0].replace(".", "-")
					eduList["end_date"] = s[1].replace(".", "-")
			# 学校名称解析
			college_info = temp[1].xpath("string(.)")
			if len(college_info) > 0:
				eduList["college_name"] = college_info[0].extract().strip()
			# 专业名称解析
			profession_name = temp[2].xpath("string(.)")
			if len(profession_name) > 0:
				profess_temp = profession_name[0].extract().strip()
				if len(profess_temp) > 3:
					eduList["profession_name"] = profess_temp[3:]
			# 学历解析
			degree_info = temp[3].xpath("string(.)")
			if len(degree_info) > 0:
				degree_temp = degree_info[0].extract().strip()
				if len(degree_temp) > 3:
					eduList["degree"] = degree_temp[3:]
			resume["educationList"].append(eduList)


# 解析工作经历
def handle_work_info(resume, info):
	name_info = info.xpath(
		".//td[@height='20'][@colspan='2'][contains(@style, 'font-size:12px;border:1px solid #ccc;padding-left:10px;background:#f3f3f3;')]/strong/text()")
	desc_info = info.xpath(
		'.//td[@height="20"][@colspan="2"][contains(@style, "font-size:12px;border:1px solid #ccc;border-top:0;padding-left:10px;padding-right:10px;")]')
	position_info = info.xpath('.//td[@width="120"][@height="20"]/strong/text()')
	if len(name_info) > 0:
		for i in range(len(name_info)):
			work_list = {"enterprise_name": "", "position_name": "", "experience_desc": "", "start_date": "",
						 "end_date": "", "enterprise_size": "", "enterprise_type": "", "work_time": "",
						 "enterprise_industry": "", "salary": "", "department": "", "second_job_type": "",
						 "first_job_type": ""}
			temp = name_info[i].extract()
			if temp != "":
				temp2 = temp.split(" ")
				if len(temp2) == 2:
					# 公司名称
					work_list["enterprise_name"] = temp2[0]
					time_info = temp2[1].split("-")
					if len(time_info) == 2:
						# 开始时间
						work_list["start_date"] = time_info[0].replace(".", "-")
						# 结束时间
						work_list["end_date"] = time_info[1].replace(".", "-")
			# 职位名称
			if len(position_info) > i:
				work_list["position_name"] = position_info[i].extract()
			if len(desc_info) > i:
				desc_temp = desc_info[i].xpath("string()")
				if len(desc_temp) > 0:
					desc_text = desc_temp[0].extract()
					if re.search(u"工作职责(：|:)(.+)", desc_text):
						work_list["experience_desc"] = re.search(u"- 工作职责(：|:)(.+)", desc_text).group(2)

			# 添加到工作经历列表
			resume["workExperienceList"].append(work_list)


# 解析项目经历
def handle_project_info(resume, info):
	table_info = info.xpath(".//table")

	for i in range(len(table_info)):
		proj_list = {"start_date": "", "end_date": "", "project_name": "", "project_desc": "", "work_desc": "",
					 "tools": "", "software": "", "hardware": ""}
		td_info = table_info[i].xpath(".//td")
		if len(td_info) == 2:
			# 解析项目名称和时间
			temp_info = td_info[0].xpath("string()")[0].extract().strip()
			temp_infos = temp_info.split(" ")
			if len(temp_infos) == 2:
				# 项目名称
				proj_list["project_name"] = temp_infos[0]
				# 项目时间解析
				time_info = temp_infos[1].replace(u"：", "")
				time_infos = time_info.split("–")
				if len(time_infos) == 2:
					start = time_infos[0].replace(".", "-")
					proj_list["start_date"] = start
					end = time_infos[1].replace(".", "-")
					if end == "0000-00":
						end = u"至今"
					proj_list["end_date"] = end
			# 解析具体项目信息
			temp_info = td_info[1].xpath("string()")[0].extract().strip()
			#  项目描述
			if re.search(u"项目简介：(.+)", temp_info):
				proj_list["project_desc"] = re.search(u"项目简介：(.+)", temp_info).group(1)
			# 工作职责
			if re.search(u"项目职责：(.+)", temp_info, re.S):
				proj_list["work_desc"] = re.search(u"项目职责：(.+)", temp_info, re.S).group(1).strip()
			if re.search(u"(.+)(- 项目业绩：.+)", proj_list["work_desc"], re.S):
				proj_yeji = re.search(u"(.+)(- 项目业绩：.+)", proj_list["work_desc"], re.S).group(1).strip()
				proj_list["work_desc"] = proj_yeji.strip()

			# 添加到项目经历列表
			resume["projectList"].append(proj_list)


# 解析语言能力
def handle_language_info(resume, info):
	lang_info = info.xpath(".//td[@height='20']/text()")
	if len(lang_info) > 0:
		temp = lang_info[0].extract()
		temp2 = temp.split(u"、")

		if len(temp2) > 0:
			for i in range(len(temp2)):
				lang_list = {"language_name": "", "language_ability": "", "language_type": ""}
				lang_list["language_name"] = temp2[i]
				resume["languageList"].append(lang_list)
