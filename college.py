# -*- coding: utf-8 -*-

from pymongo import MongoClient
import requests

class college:
  scl_uuid="" #学校编码
  scl_rank="" #学校等级
  scl_type="" #学校类别
  scl_name="" #学校名称
  scl_addr="" #学校地址
  scl_belong="" #
  master_pilot="" #博士人数
  doctor_pilot="" #教授人数
  scl_tel="" #学校电话
  detail_addr="" #详细地址
  introduce="" #学校简介
  enployment="" #就业情况
  scl_room="" #住宿情况
  tuition="" #学费
  up_user_name="" #
  web_site="" #学校官网
  zhaosehng_web_site="" #招生网址
  lq_rule="" #录取规则

  def __init__(self,sscl_uuid,scl_rank,scl_type,scl_name,scl_addr,scl_belong,master_pilot,doctor_pilot,scl_tel,detail_addr,introduce,enployment,scl_room,tuition,up_user_name,web_site,zhaosehng_web_site,lq_rule):
    self.sscl_uuid=sscl_uuid
    self.scl_rank=scl_rank
    self.scl_type=scl_type
    self.scl_name=scl_name
    self.scl_addr=scl_addr
    self.scl_belong=scl_belong
    self.master_pilot=master_pilot
    self.doctor_pilot=doctor_pilot
    self.scl_tel=scl_tel
    self.detail_addr=detail_addr
    self.introduce=introduce
    self.enployment=enployment
    self.scl_room=scl_room
    self.tuition=tuition
    self.up_user_name=up_user_name
    self.web_site=web_site
    self.zhaosehng_web_site=zhaosehng_web_site
    self.lq_rule=lq_rule
    

  @staticmethod
  def get_all_page2db():
    client = MongoClient("139.129.45.40",27017)
    db=client.gaokao
    db.page.remove()
    headers={"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"}
    for i in range(1,105):
      r1=requests.post("http://www.yunzhongzhile.com/gkbd/front/school/findSchoolListByFront",data={"curPage":str(i)},headers=headers)
      db.page.insert_one({"page_num":str(i),"text":r1.text})
      print("%d successfully!! size:%d"%(i,db.page.find().count()))