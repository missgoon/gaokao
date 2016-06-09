# -*- coding: utf-8 -*-

from pymongo import MongoClient
import requests

class major:
  subject="" #学科
  major_class="" #门类
  name="" #专业名称
  main_course="" #主要开设课程
  colleges="" #开设高校
  similar_professional="" #相似专业
  employment="" #就业情况
  introduce="" #专业介绍
  courseTime="" #学制
  degree="" #学位证
  uuid="" #学科编码

  def __init__(self,sub,mclass,name,course,college,similar,employ,introduce,courseTime,degree,uuid):
    self.subject=sub
    self.major_class=mclass
    self.name=name
    self.main_course=course
    self.colleges=college
    self.similar_professional=similar
    self.employment=employ
    self.introduce=introduce
    self.degree=degree
    self.uuid=uuid
    self.courseTime=courseTime

  def save_to_db(self):
    client = MongoClient("139.129.45.40",27017)
    db=client.gaokao
    if db.major.find({"name":self.name}).count()>0: db.major.delete_one({"name":self.name})
    db.major.insert_one(self.major_dict())
    print("save to db successfully!!! size:%s"%str(db.major.find().count()))
  
  def major_dict(self):
    return dict({"subject":self.subject,"major_class":self.major_class,"name":self.name,"main_course":self.main_course,"colleges":self.colleges,"similar_professional":self.similar_professional,"employment":self.employment,"introduce":self.introduce,"degree":self.degree,"uuid":self.uuid,"courseTime":self.courseTime})

  @staticmethod
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

  @staticmethod
  def db2file():
    client = MongoClient("139.129.45.40",27017)
    db=client.gaokao
    with open("major.txt","wa") as file:
      for item in db.major.find():
        file.write("courseTime:"+item["uuid"].encode("utf-8")+"\n")
        file.write("name:"+item["name"].encode("utf-8")+"\n")
        file.write("subject:"+item["subject"].encode("utf-8")+"\n")
        file.write("major_class:"+item["major_class"].encode("utf-8")+"\n")
        file.write("degree:"+item["courseTime"].encode("utf-8")+"\n")
        file.write("uuid:"+item["degree"].encode("utf-8")+"\n")
        file.write("main_course:"+item["main_course"].encode("utf-8")+"\n")
        file.write("similar_professional:"+item["similar_professional"].encode("utf-8")+"\n")
        file.write("employment:"+item["employment"].encode("utf-8")+"\n")
        file.write("introduce:"+item["introduce"].encode("utf-8")+"\n")
        file.write("colleges:"+item["colleges"].encode("utf-8")+"\n")
        file.write("\n")
      
  @staticmethod
  def delete_useless_char():
    client=MongoClient("139.129.45.40",27017)
    db=client.gaokao
    cnt=0
    for item in db.major.find():
      target=item["employment"]
      n1=target.find(r"\u003c")
      n2=target.find(r"\u003e")
      while n1!=-1 and n2!=-1:
        n2=target.find(r"\u003e")
        if n2>=n1:
          target=target[0:n1]+target[n2+6:]
          n2=target.find(r"\u003e")
          n1=target.find(r"\u003c")
        else:
          target=target[0:n2]+target[n2+6:]
          n2=target.find(r"\u003e")
          n1=target.find(r"\u003c")
      db.major.update_one({"name":item["name"]},{"$set":{"employment":target}})
      cnt+=1
      print("finish %d"%cnt)