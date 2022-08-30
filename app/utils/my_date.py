import calendar
import re
from datetime import date, timedelta, datetime
from chinese_calendar import is_workday


class MyDate:
    def __init__(self, today):
        self.today = today or date.today()
        self.today = self.format_date_string(self.today)
        self.year = self.today.year
        self.month = self.today.month
        self.day = self.today.day

    @staticmethod
    def format_date_string(today):
        """字符串转日期格式处理"""
        if re.findall(today, r"(\d*)-(\d*)-(\d*) (\d*):(\d*):(\d*)"):
            return datetime.strptime(today, '%Y-%m-%d %H:%M:%S')
        elif re.findall(today, r"(\d*)-(\d*)-(\d*) (\d*):(\d*)"):
            return datetime.strptime(today, '%Y-%m-%d %H:%M')
        elif re.findall(today, r"(\d*)-(\d*)-(\d*) (\d*)"):
            return datetime.strptime(today, '%Y-%m-%d %H')
        elif re.findall(today, r"(\d*)-(\d*)-(\d*)"):
            return datetime.strptime(today, '%Y-%m-%d')

    def get_week_first_last(self):
        """获取当前日期所在周的周一、周日的日期"""
        one_day = timedelta(days=1)
        monday = self.today - (one_day * self.today.weekday())
        sunday = monday + 6 * one_day
        return monday, sunday

    def get_month_first_last(self):
        """获取当前日期所在月份第一天和最后一天"""
        weekDay, monthCountDay = calendar.monthrange(self.year, self.month)
        firstDay = date(self.year, self.month, day=1)
        lastDay = date(self.year, self.month, day=monthCountDay)
        return firstDay, lastDay

    def get_yesterday(self):
        """获取昨天"""
        one_day = timedelta(days=1)
        return self.today - one_day

    def get_tomorrow(self):
        """获取明天"""
        one_day = timedelta(days=1)
        return self.today + one_day

    def get_this_week_content(self):
        """获取date本周内容（第{}周({}至{})）"""
        start, end = self.get_week_first_last()  # 获取本周周一、周五日期
        year, week, weekday = end.isocalendar()
        week_content = '第{}周({}至{})'.format(week, start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'))
        return week_content, start, end

    def get_date_month_content(self):
        """获取date本月内容（第{}月({}至{})）"""
        start, end = self.get_month_first_last()  # 获取本月第1天、最后一天
        month_content = '{}月({}至{})'.format(start.month, start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'))  # 本月时间
        return month_content, start, end

    def get_workdays(self, start, end):
        """计算两个日期间的工作日"""
        # 字符串格式日期的处理
        if type(start) == str:
            start = self.format_date_string(start).date()
        if type(end) == str:
            end = self.format_date_string(end).date()
        # 开始日期大，交换开始日期和结束日期
        if start > end:
            start, end = end, start
        counts = 0
        while start <= end:
            if is_workday(start):
                counts += 1
            start += timedelta(days=1)
        return counts
