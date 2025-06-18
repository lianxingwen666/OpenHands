#!/usr/bin/env python3
"""
特定评教页面自动化脚本
===================

专门针对评教系统的自动打分功能
URL: http://210.30.204.138/school/proj/evaluatevl-0/module/task/org/UJUMGRK4kyat8tEaH1z4QN/mytask/detail/...

功能特点：
- 智能随机评分（避免全部相同分数）
- 支持多种评分策略
- 模拟真实用户行为
- 安全的操作延时
"""

import logging
import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# 配置日志
logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SmartEvaluationBot:
    """智能评教机器人"""

    def __init__(self, headless=False):
        """初始化浏览器"""
        self.setup_driver(headless)
        self.wait = WebDriverWait(self.driver, 15)

        # 评分策略配置
        self.scoring_strategies = {
            'conservative': {  # 保守策略：主要4-5分
                'weights': {5: 0.4, 4: 0.4, 3: 0.15, 2: 0.05, 1: 0.0},
                'description': '保守策略：主要给4-5分，少量3分',
            },
            'positive': {  # 积极策略：主要5分
                'weights': {5: 0.6, 4: 0.3, 3: 0.1, 2: 0.0, 1: 0.0},
                'description': '积极策略：主要给5分，部分4分',
            },
            'balanced': {  # 平衡策略：3-5分均匀
                'weights': {5: 0.3, 4: 0.4, 3: 0.25, 2: 0.05, 1: 0.0},
                'description': '平衡策略：3-5分比较均匀',
            },
            'realistic': {  # 现实策略：更真实的分布
                'weights': {5: 0.25, 4: 0.45, 3: 0.25, 2: 0.05, 1: 0.0},
                'description': '现实策略：以4分为主，其他分数合理分布',
            },
        }

    def setup_driver(self, headless=False):
        """设置Chrome浏览器"""
        chrome_options = Options()
        if headless:
            chrome_options.add_argument('--headless')

        # 反检测设置
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        # 设置用户代理
        chrome_options.add_argument(
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )

        logger.info('浏览器初始化完成')

    def get_smart_score(self, strategy='realistic'):
        """根据策略获取智能评分"""
        weights = self.scoring_strategies[strategy]['weights']
        scores = list(weights.keys())
        probabilities = list(weights.values())

        return random.choices(scores, weights=probabilities)[0]

    def human_like_delay(self, min_delay=0.5, max_delay=2.0):
        """模拟人类操作延时"""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)

    def scroll_to_element(self, element):
        """平滑滚动到元素"""
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
            element,
        )
        self.human_like_delay(0.3, 0.8)

    def click_with_human_behavior(self, element):
        """模拟人类点击行为"""
        # 先移动鼠标到元素
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.human_like_delay(0.2, 0.5)

        # 点击元素
        element.click()
        logger.info(f'点击了元素: {element.get_attribute("value") or element.text}')

    def navigate_to_page(self, url):
        """导航到评教页面"""
        try:
            logger.info(f'正在访问页面: {url}')
            self.driver.get(url)

            # 等待页面加载
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            self.human_like_delay(2, 4)

            logger.info('页面加载完成')
            return True

        except Exception as e:
            logger.error(f'页面加载失败: {e}')
            return False

    def analyze_evaluation_form(self):
        """分析评教表单结构"""
        try:
            # 查找所有单选按钮
            radio_buttons = self.driver.find_elements(
                By.XPATH, "//input[@type='radio']"
            )
            logger.info(f'找到 {len(radio_buttons)} 个单选按钮')

            # 按name属性分组
            radio_groups = {}
            for radio in radio_buttons:
                name = radio.get_attribute('name')
                value = radio.get_attribute('value')
                if name:
                    if name not in radio_groups:
                        radio_groups[name] = []
                    radio_groups[name].append(
                        {
                            'element': radio,
                            'value': value,
                            'text': self.get_radio_text(radio),
                        }
                    )

            logger.info(f'找到 {len(radio_groups)} 个评分组')

            # 查找文本框
            text_areas = self.driver.find_elements(By.XPATH, '//textarea')
            text_inputs = self.driver.find_elements(By.XPATH, "//input[@type='text']")

            logger.info(
                f'找到 {len(text_areas)} 个文本域，{len(text_inputs)} 个文本输入框'
            )

            return {
                'radio_groups': radio_groups,
                'text_areas': text_areas,
                'text_inputs': text_inputs,
            }

        except Exception as e:
            logger.error(f'表单分析失败: {e}')
            return None

    def get_radio_text(self, radio_element):
        """获取单选按钮的关联文本"""
        try:
            # 尝试多种方法获取文本
            parent = radio_element.find_element(By.XPATH, './..')
            return parent.text.strip()
        except Exception:
            return radio_element.get_attribute('value') or ''

    def auto_fill_evaluation(self, strategy='realistic', custom_comments=None):
        """自动填写评教表单"""
        try:
            logger.info(f'开始自动填写评教，使用策略: {strategy}')
            logger.info(f'策略说明: {self.scoring_strategies[strategy]["description"]}')

            # 分析表单
            form_data = self.analyze_evaluation_form()
            if not form_data:
                return False

            filled_count = 0

            # 填写单选按钮
            for group_name, radios in form_data['radio_groups'].items():
                try:
                    # 获取智能评分
                    target_score = self.get_smart_score(strategy)

                    # 查找对应分值的单选按钮
                    target_radio = None
                    for radio_info in radios:
                        value = radio_info['value']
                        # 尝试匹配分值
                        if value and (
                            value == str(target_score) or value == target_score
                        ):
                            target_radio = radio_info['element']
                            break

                    # 如果没找到精确匹配，选择最接近的
                    if not target_radio and radios:
                        # 按值排序，选择最接近目标分数的
                        sorted_radios = sorted(
                            radios,
                            key=lambda x: abs(int(x['value'] or '0') - target_score)
                            if x['value'] and x['value'].isdigit()
                            else float('inf'),
                        )
                        if sorted_radios:
                            target_radio = sorted_radios[0]['element']

                    if (
                        target_radio
                        and target_radio.is_displayed()
                        and target_radio.is_enabled()
                    ):
                        # 滚动到元素
                        self.scroll_to_element(target_radio)

                        # 点击单选按钮
                        self.click_with_human_behavior(target_radio)

                        filled_count += 1
                        logger.info(f"组 '{group_name}' 选择了分数: {target_score}")

                        # 随机延时
                        self.human_like_delay(0.8, 2.0)

                except Exception as e:
                    logger.warning(f"填写组 '{group_name}' 时出错: {e}")
                    continue

            # 填写文本评语
            if custom_comments is None:
                custom_comments = [
                    '老师教学认真负责，课程内容充实，受益匪浅。',
                    '课程设计合理，教学方法得当，学到了很多知识。',
                    '老师讲解清晰，课堂氛围良好，非常有帮助。',
                    '教学水平高，内容丰富，对学习很有启发。',
                    '课程质量不错，老师很负责，整体比较满意。',
                ]

            # 填写文本域
            for i, textarea in enumerate(form_data['text_areas']):
                if textarea.is_displayed() and textarea.is_enabled():
                    try:
                        comment = random.choice(custom_comments)

                        self.scroll_to_element(textarea)
                        textarea.clear()

                        # 模拟打字
                        for char in comment:
                            textarea.send_keys(char)
                            time.sleep(random.uniform(0.05, 0.15))

                        logger.info(f'填写了评语: {comment[:20]}...')
                        self.human_like_delay(1, 2)

                    except Exception as e:
                        logger.warning(f'填写文本域时出错: {e}')

            logger.info(f'自动填写完成！共填写了 {filled_count} 个评分项')
            return True

        except Exception as e:
            logger.error(f'自动填写失败: {e}')
            return False

    def find_submit_button(self):
        """查找提交按钮"""
        submit_selectors = [
            "//input[@type='submit']",
            "//button[@type='submit']",
            "//button[contains(text(), '提交')]",
            "//button[contains(text(), '确定')]",
            "//button[contains(text(), '保存')]",
            "//input[contains(@value, '提交')]",
            "//input[contains(@value, '确定')]",
            "//a[contains(text(), '提交')]",
        ]

        for selector in submit_selectors:
            try:
                buttons = self.driver.find_elements(By.XPATH, selector)
                for button in buttons:
                    if button.is_displayed() and button.is_enabled():
                        return button
            except Exception:
                continue

        return None

    def submit_evaluation(self, auto_submit=False):
        """提交评教"""
        try:
            submit_button = self.find_submit_button()

            if submit_button:
                logger.info('找到提交按钮')

                if not auto_submit:
                    input('评教填写完成！请检查内容，按Enter键提交，或Ctrl+C取消...')

                self.scroll_to_element(submit_button)
                self.click_with_human_behavior(submit_button)

                logger.info('已点击提交按钮')
                self.human_like_delay(2, 4)

                return True
            else:
                logger.warning('未找到提交按钮，请手动提交')
                return False

        except KeyboardInterrupt:
            logger.info('用户取消提交')
            return False
        except Exception as e:
            logger.error(f'提交失败: {e}')
            return False

    def run_evaluation(
        self, url, strategy='realistic', auto_submit=False, custom_comments=None
    ):
        """运行完整的评教流程"""
        try:
            logger.info('=' * 60)
            logger.info('开始智能评教流程')
            logger.info('=' * 60)

            # 1. 访问页面
            if not self.navigate_to_page(url):
                return False

            # 2. 自动填写
            if not self.auto_fill_evaluation(strategy, custom_comments):
                return False

            # 3. 提交评教
            return self.submit_evaluation(auto_submit)

        except Exception as e:
            logger.error(f'评教流程失败: {e}')
            return False

    def close(self):
        """关闭浏览器"""
        if hasattr(self, 'driver'):
            self.driver.quit()
            logger.info('浏览器已关闭')


def main():
    """主函数"""
    print('🎓 智能评教自动化工具')
    print('=' * 50)

    # 目标URL
    url = 'http://210.30.204.138/school/proj/evaluatevl-0/module/task/org/UJUMGRK4kyat8tEaH1z4QN/mytask/detail/UEq1WebxkU6nwtKicN418c/TTNH3mqhZiaDBP26iGAnWG/A087238/00007351'

    print(f'目标页面: {url}')
    print()

    # 选择评分策略
    print('📊 可用的评分策略:')
    strategies = {
        '1': 'conservative',
        '2': 'positive',
        '3': 'balanced',
        '4': 'realistic',
    }

    for key, strategy in strategies.items():
        bot = SmartEvaluationBot()
        desc = bot.scoring_strategies[strategy]['description']
        print(f'  {key}. {strategy.title()}: {desc}')
        bot.close()

    choice = input('\n请选择评分策略 (1-4, 默认4): ').strip() or '4'
    selected_strategy = strategies.get(choice, 'realistic')

    print(f'✅ 已选择策略: {selected_strategy}')

    # 是否自动提交
    auto_submit = input('是否自动提交？(y/N): ').strip().lower() == 'y'

    # 是否显示浏览器
    headless = input('是否隐藏浏览器窗口？(y/N): ').strip().lower() == 'y'

    print('\n🚀 开始执行...')

    # 创建机器人实例
    bot = SmartEvaluationBot(headless=headless)

    try:
        # 运行评教
        success = bot.run_evaluation(
            url=url, strategy=selected_strategy, auto_submit=auto_submit
        )

        if success:
            print('\n✅ 评教完成！')
        else:
            print('\n❌ 评教失败，请检查页面或手动操作')

    except KeyboardInterrupt:
        print('\n⏹️ 用户中断操作')
    except Exception as e:
        print(f'\n💥 程序出错: {e}')
    finally:
        bot.close()


if __name__ == '__main__':
    main()
