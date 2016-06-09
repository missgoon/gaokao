#-*- coding:utf-8 -*-

import sys
sys.path.append("/missgoon")
from major import major
import requests

def get_major_name():
  s=requests.Session()
  s.get("http://www.yunzhongzhile.com/gkbd/front/datacenter/gkzhuanyes.jsp?bigType=%25E5%2586%259C%25E5%25AD%25A6")
  r=s.post("http://www.yunzhongzhile.com/gkbd/front/professional/findPageInfoNopage")
  subjects=r.text.split("}")[:-1]
  for sub in subjects:
    zl=sub.split('zl":",')[1]
    zl,xl=zl.split('","xl":",')
    xl,dl=xl.split('","dl":"')
    # dl=dl.split('"')[0]
    # zl=zl.split(",")
    xl=xl.split(",")
    for item in xl:
      r=s.post("http://www.yunzhongzhile.com/gkbd/front/professional/findPageInfoNopageBymajor",data={"major":item})
      major_info=eval(r.text)["list"][0]
      subject=major_info["bigType"].decode("utf-8")
      main_course=major_info["course"].decode("utf-8")
      courseTime=major_info["courseTime"].decode("utf-8")
      degree=major_info["degree"].decode("utf-8")
      employment=major_info["employmentDir"].decode("utf-8")
      name=major_info["major"].decode("utf-8")
      introduce=major_info["majorIntro"].decode("utf-8")
      similar_professional=major_info["relevantMajor"].decode("utf-8")
      major_class=major_info["smallType"].decode("utf-8")
      uuid=major_info["uuid"].decode("utf-8")
      r2=s.post("http://www.yunzhongzhile.com/gkbd/front/prof/findProfSchool?profUUID="+uuid)
      colleges=r2.text
      major(subject,major_class,name,main_course,colleges,similar_professional,employment,introduce,degree,uuid,courseTime).save_to_db()
  