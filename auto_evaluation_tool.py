#!/usr/bin/env python3
"""
自动评教工具 - 仅供学习和研究目的
=====================================

重要声明：
1. 本工具仅用于技术学习和研究目的
2. 使用前请确保符合学校相关规定
3. 建议进行真实、客观的评教
4. 使用者需承担相应责任

技术栈：
- Selenium WebDriver: 浏览器自动化
- BeautifulSoup: HTML解析
- Requests: HTTP请求处理
- Time: 延时控制
"""

import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class AutoEvaluationTool:
    """自动评教工具类"""

    def __init__(self, headless=False):
        """
        初始化浏览器驱动

        参数:
            headless: 是否使用无头模式
        """
        self.setup_driver(headless)
        self.wait = WebDriverWait(self.driver, 10)

    def setup_driver(self, headless=False):
        """设置Chrome浏览器驱动"""
        chrome_options = Options()
        if headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )

    def login(self, username, password, login_url):
        """
        登录系统

        参数:
            username: 用户名
            password: 密码
            login_url: 登录页面URL
        """
        try:
            print('正在访问登录页面...')
            self.driver.get(login_url)

            # 等待页面加载
            time.sleep(2)

            # 查找用户名和密码输入框
            username_input = self.wait.until(
                EC.presence_of_element_located((By.NAME, 'username'))
            )
            password_input = self.driver.find_element(By.NAME, 'password')

            # 输入凭据
            username_input.clear()
            username_input.send_keys(username)

            password_input.clear()
            password_input.send_keys(password)

            # 查找并点击登录按钮
            login_button = self.driver.find_element(By.XPATH, "//input[@type='submit']")
            login_button.click()

            print('登录请求已发送，等待响应...')
            time.sleep(3)

            return True

        except Exception as e:
            print(f'登录失败: {e}')
            return False

    def navigate_to_evaluation(self, evaluation_url):
        """
        导航到评教页面

        参数:
            evaluation_url: 评教页面URL
        """
        try:
            print('正在访问评教页面...')
            self.driver.get(evaluation_url)
            time.sleep(2)
            return True
        except Exception as e:
            print(f'访问评教页面失败: {e}')
            return False

    def auto_fill_evaluation(self, evaluation_config=None):
        """
        自动填写评教表单

        参数:
            evaluation_config: 评教配置字典
        """
        try:
            print('开始自动填写评教...')

            # 默认评教配置（建议设置为积极正面的评价）
            if evaluation_config is None:
                evaluation_config = {
                    'radio_value': '5',  # 通常5表示"非常满意"
                    'text_content': '老师教学认真负责，课程内容丰富，受益匪浅。',
                    'delay_range': (1, 3),  # 操作间隔时间范围
                }

            # 查找所有单选按钮组
            radio_groups = self.driver.find_elements(By.XPATH, "//input[@type='radio']")

            for radio in radio_groups:
                if radio.get_attribute('value') == evaluation_config['radio_value']:
                    # 模拟人工操作的随机延时
                    time.sleep(random.uniform(*evaluation_config['delay_range']))

                    # 滚动到元素可见位置
                    self.driver.execute_script('arguments[0].scrollIntoView();', radio)

                    # 点击单选按钮
                    self.driver.execute_script('arguments[0].click();', radio)
                    print(f'已选择评分: {evaluation_config["radio_value"]}')

            # 查找文本输入框并填写评语
            text_areas = self.driver.find_elements(By.XPATH, '//textarea')
            for textarea in text_areas:
                if textarea.is_displayed() and textarea.is_enabled():
                    textarea.clear()
                    # 模拟打字效果
                    for char in evaluation_config['text_content']:
                        textarea.send_keys(char)
                        time.sleep(random.uniform(0.05, 0.15))
                    print('已填写评语')

            return True

        except Exception as e:
            print(f'填写评教失败: {e}')
            return False

    def submit_evaluation(self):
        """提交评教表单"""
        try:
            print('正在提交评教...')

            # 查找提交按钮
            submit_buttons = self.driver.find_elements(
                By.XPATH,
                "//input[@type='submit'] | //button[contains(text(), '提交')] | //button[contains(text(), '确定')]",
            )

            if submit_buttons:
                submit_button = submit_buttons[0]
                self.driver.execute_script(
                    'arguments[0].scrollIntoView();', submit_button
                )
                time.sleep(1)
                submit_button.click()

                print('评教已提交')
                time.sleep(2)
                return True
            else:
                print('未找到提交按钮')
                return False

        except Exception as e:
            print(f'提交评教失败: {e}')
            return False

    def run_auto_evaluation(
        self, username, password, login_url, evaluation_url, config=None
    ):
        """
        运行完整的自动评教流程

        参数:
            username: 用户名
            password: 密码
            login_url: 登录页面URL
            evaluation_url: 评教页面URL
            config: 评教配置
        """
        try:
            # 步骤1: 登录
            if not self.login(username, password, login_url):
                return False

            # 步骤2: 导航到评教页面
            if not self.navigate_to_evaluation(evaluation_url):
                return False

            # 步骤3: 填写评教
            if not self.auto_fill_evaluation(config):
                return False

            # 步骤4: 提交评教（可选，建议手动确认）
            print('评教填写完成，请手动检查并提交')
            input('按Enter键继续提交，或Ctrl+C取消...')

            return self.submit_evaluation()

        except KeyboardInterrupt:
            print('用户取消操作')
            return False
        except Exception as e:
            print(f'自动评教过程出错: {e}')
            return False

    def close(self):
        """关闭浏览器"""
        if hasattr(self, 'driver'):
            self.driver.quit()
            print('浏览器已关闭')


def main():
    """主函数 - 使用示例"""

    print('=' * 50)
    print('自动评教工具')
    print('=' * 50)
    print('重要提醒：')
    print('1. 请确保您有权限使用此工具')
    print('2. 建议进行真实、客观的评教')
    print('3. 本工具仅供学习研究目的')
    print('=' * 50)

    # 获取用户输入
    username = input('请输入用户名: ')
    password = input('请输入密码: ')

    # URL配置
    base_url = 'http://210.30.204.138'
    login_url = f'{base_url}/login'  # 需要根据实际情况调整
    evaluation_url = 'http://210.30.204.138/school/proj/evaluatevl-0/module/task/org/UJUMGRK4kyat8tEaH1z4QN/mytask'

    # 评教配置
    evaluation_config = {
        'radio_value': '5',  # 最高评分
        'text_content': '老师教学水平高，课程内容充实，教学方法得当，课堂氛围良好，收获很大。',
        'delay_range': (0.5, 2.0),
    }

    # 创建自动评教工具实例
    tool = AutoEvaluationTool(headless=False)  # 设置为True可隐藏浏览器窗口

    try:
        # 运行自动评教
        success = tool.run_auto_evaluation(
            username=username,
            password=password,
            login_url=login_url,
            evaluation_url=evaluation_url,
            config=evaluation_config,
        )

        if success:
            print('自动评教完成！')
        else:
            print('自动评教失败，请检查配置和网络连接')

    except Exception as e:
        print(f'程序执行出错: {e}')
    finally:
        tool.close()


if __name__ == '__main__':
    main()
