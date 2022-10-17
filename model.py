from flask_sqlalchemy import SQLAlchemy

from app import db


class BigData(db.Model):
    # 设置表名
    __tablename__ = 'bigdata'
    # 基础信息
    year = db.Column(db.String(255), primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), primary_key=True)
    # 可支配
    city_able_income = db.Column(db.Float(20))
    village_able_income = db.Column(db.Float(20))
    city_ratio = db.Column(db.Float(20))
    # 人口
    population = db.Column(db.Float(20))
    city_population = db.Column(db.Float(20))
    village_population = db.Column(db.Float(20))
    # 收入
    income = db.Column(db.Float(20))
    city_income = db.Column(db.Float(20))
    village_income = db.Column(db.Float(20))
    # 比率
    city_able_income_ratio = db.Column(db.Float(20))
    city_population_ratio = db.Column(db.Float(20))
    village_able_income_ratio = db.Column(db.Float(20))
    village_population_ratio = db.Column(db.Float(20))
    # 对数
    village_income_population_ratio = db.Column(db.Float(20))
    city_income_population_ratio = db.Column(db.Float(20))
    # 泰尔指数
    theil_index = db.Column(db.Float(20))
