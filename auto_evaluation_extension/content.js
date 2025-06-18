// 自动评教助手 - 内容脚本

(function() {
    'use strict';

    // 监听来自弹窗的消息
    chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
        if (request.action === 'autoFill') {
            autoFillEvaluation(request.config)
                .then(result => sendResponse({success: true, ...result}))
                .catch(error => sendResponse({success: false, error: error.message}));
            return true; // 保持消息通道开放
        } else if (request.action === 'preview') {
            previewEvaluation()
                .then(result => sendResponse({success: true, ...result}))
                .catch(error => sendResponse({success: false, error: error.message}));
            return true;
        }
    });

    /**
     * 自动填写评教表单
     */
    async function autoFillEvaluation(config) {
        try {
            console.log('开始自动填写评教...', config);

            // 查找所有单选按钮
            const radioButtons = document.querySelectorAll('input[type="radio"]');
            let filledRadios = 0;

            // 按组处理单选按钮
            const radioGroups = {};
            radioButtons.forEach(radio => {
                const name = radio.name;
                if (!radioGroups[name]) {
                    radioGroups[name] = [];
                }
                radioGroups[name].push(radio);
            });

            // 为每个组选择对应的评分
            for (const groupName in radioGroups) {
                const group = radioGroups[groupName];
                const targetRadio = group.find(radio =>
                    radio.value === config.rating ||
                    radio.value === config.rating.toString()
                );

                if (targetRadio && !targetRadio.checked) {
                    // 滚动到可见位置
                    targetRadio.scrollIntoView({ behavior: 'smooth', block: 'center' });

                    // 等待延时
                    await sleep(config.delay);

                    // 点击单选按钮
                    targetRadio.click();

                    // 触发change事件
                    targetRadio.dispatchEvent(new Event('change', { bubbles: true }));

                    filledRadios++;
                    console.log(`已选择评分 ${config.rating} for ${groupName}`);
                }
            }

            // 查找并填写文本域
            const textAreas = document.querySelectorAll('textarea');
            let filledTextAreas = 0;

            for (const textarea of textAreas) {
                if (textarea.offsetParent !== null && !textarea.disabled) { // 可见且可编辑
                    // 滚动到可见位置
                    textarea.scrollIntoView({ behavior: 'smooth', block: 'center' });

                    // 等待延时
                    await sleep(config.delay);

                    // 清空并填写内容
                    textarea.value = '';
                    textarea.focus();

                    // 模拟打字效果
                    for (let i = 0; i < config.comment.length; i++) {
                        textarea.value += config.comment[i];
                        textarea.dispatchEvent(new Event('input', { bubbles: true }));
                        await sleep(50); // 打字间隔
                    }

                    // 触发change事件
                    textarea.dispatchEvent(new Event('change', { bubbles: true }));
                    textarea.blur();

                    filledTextAreas++;
                    console.log('已填写评语');
                }
            }

            // 添加视觉提示
            showNotification(`✅ 自动填写完成！\n单选项: ${filledRadios}\n文本框: ${filledTextAreas}`);

            return {
                filledRadios,
                filledTextAreas,
                message: '自动填写完成'
            };

        } catch (error) {
            console.error('自动填写失败:', error);
            showNotification('❌ 自动填写失败: ' + error.message, 'error');
            throw error;
        }
    }

    /**
     * 预览评教表单
     */
    async function previewEvaluation() {
        try {
            const radioButtons = document.querySelectorAll('input[type="radio"]');
            const textAreas = document.querySelectorAll('textarea:not([disabled])');
            const submitButtons = document.querySelectorAll('input[type="submit"], button[type="submit"]');

            // 高亮显示找到的元素
            highlightElements([...radioButtons, ...textAreas, ...submitButtons]);

            showNotification(`📋 找到评教元素:\n单选按钮: ${radioButtons.length}\n文本框: ${textAreas.length}\n提交按钮: ${submitButtons.length}`);

            return {
                count: radioButtons.length + textAreas.length,
                radioButtons: radioButtons.length,
                textAreas: textAreas.length,
                submitButtons: submitButtons.length
            };

        } catch (error) {
            console.error('预览失败:', error);
            throw error;
        }
    }

    /**
     * 高亮显示元素
     */
    function highlightElements(elements) {
        // 移除之前的高亮
        document.querySelectorAll('.auto-eval-highlight').forEach(el => {
            el.classList.remove('auto-eval-highlight');
        });

        // 添加新的高亮
        elements.forEach(el => {
            el.classList.add('auto-eval-highlight');
        });

        // 3秒后移除高亮
        setTimeout(() => {
            elements.forEach(el => {
                el.classList.remove('auto-eval-highlight');
            });
        }, 3000);
    }

    /**
     * 显示通知
     */
    function showNotification(message, type = 'success') {
        // 移除现有通知
        const existingNotification = document.getElementById('auto-eval-notification');
        if (existingNotification) {
            existingNotification.remove();
        }

        // 创建通知元素
        const notification = document.createElement('div');
        notification.id = 'auto-eval-notification';
        notification.className = `auto-eval-notification ${type}`;
        notification.innerHTML = `
            <div class="auto-eval-notification-content">
                <div class="auto-eval-notification-text">${message.replace(/\n/g, '<br>')}</div>
                <button class="auto-eval-notification-close" onclick="this.parentElement.parentElement.remove()">×</button>
            </div>
        `;

        // 添加到页面
        document.body.appendChild(notification);

        // 5秒后自动移除
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 5000);
    }

    /**
     * 睡眠函数
     */
    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    // 页面加载完成后的初始化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    function init() {
        console.log('自动评教助手已加载');

        // 检查是否在评教页面
        if (window.location.href.includes('evaluatevl') ||
            document.querySelector('input[type="radio"]') ||
            document.querySelector('textarea')) {

            // 添加快捷键支持
            document.addEventListener('keydown', function(e) {
                // Ctrl+Shift+E 快速填写
                if (e.ctrlKey && e.shiftKey && e.key === 'E') {
                    e.preventDefault();

                    // 使用默认配置
                    const defaultConfig = {
                        rating: '5',
                        comment: '老师教学认真负责，课程内容丰富，受益匪浅。',
                        delay: 1000
                    };

                    autoFillEvaluation(defaultConfig);
                }
            });

            showNotification('🎓 自动评教助手已就绪\n快捷键: Ctrl+Shift+E');
        }
    }

})();
