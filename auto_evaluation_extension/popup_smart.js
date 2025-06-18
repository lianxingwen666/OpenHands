// 智能自动评教助手 - 弹窗脚本

document.addEventListener('DOMContentLoaded', function() {
    // 获取DOM元素
    const strategySelect = document.getElementById('strategy');
    const ratingSelect = document.getElementById('rating');
    const commentTextarea = document.getElementById('comment');
    const delayInput = document.getElementById('delay');
    const autoFillBtn = document.getElementById('autoFill');
    const previewBtn = document.getElementById('preview');
    const statusDiv = document.getElementById('status');
    const customRatingGroup = document.getElementById('customRatingGroup');
    const strategyInfo = document.getElementById('strategyInfo');

    // 评分策略配置
    const scoringStrategies = {
        'conservative': {
            weights: {5: 0.4, 4: 0.4, 3: 0.15, 2: 0.05, 1: 0.0},
            description: '保守策略：主要给4-5分，少量3分，避免极端评分'
        },
        'positive': {
            weights: {5: 0.6, 4: 0.3, 3: 0.1, 2: 0.0, 1: 0.0},
            description: '积极策略：主要给5分，部分4分，整体评价较高'
        },
        'balanced': {
            weights: {5: 0.3, 4: 0.4, 3: 0.25, 2: 0.05, 1: 0.0},
            description: '平衡策略：3-5分比较均匀，更加客观真实'
        },
        'realistic': {
            weights: {5: 0.25, 4: 0.45, 3: 0.25, 2: 0.05, 1: 0.0},
            description: '现实策略：以4分为主，其他分数合理分布，避免全部相同'
        }
    };

    // 加载保存的配置
    loadSavedConfig();

    // 绑定事件监听器
    autoFillBtn.addEventListener('click', handleAutoFill);
    previewBtn.addEventListener('click', handlePreview);
    strategySelect.addEventListener('change', handleStrategyChange);

    // 保存配置到存储
    [strategySelect, ratingSelect, commentTextarea, delayInput].forEach(element => {
        element.addEventListener('change', saveConfig);
    });

    // 初始化策略显示
    handleStrategyChange();

    /**
     * 处理策略变化
     */
    function handleStrategyChange() {
        const strategy = strategySelect.value;

        if (strategy === 'custom') {
            customRatingGroup.style.display = 'block';
            strategyInfo.innerHTML = `
                <div style="font-size: 11px; color: #666; background: #f8f9fa; padding: 8px; border-radius: 3px;">
                    <strong>固定分数：</strong>所有评分项都使用相同的分数
                </div>
            `;
        } else {
            customRatingGroup.style.display = 'none';
            const strategyData = scoringStrategies[strategy];
            if (strategyData) {
                strategyInfo.innerHTML = `
                    <div style="font-size: 11px; color: #666; background: #f8f9fa; padding: 8px; border-radius: 3px;">
                        <strong>${strategy === 'realistic' ? '现实策略' :
                                 strategy === 'positive' ? '积极策略' :
                                 strategy === 'conservative' ? '保守策略' : '平衡策略'}：</strong>${strategyData.description}
                    </div>
                `;
            }
        }
    }

    /**
     * 获取智能评分
     */
    function getSmartScore(strategy) {
        if (strategy === 'custom') {
            return parseInt(ratingSelect.value);
        }

        const weights = scoringStrategies[strategy].weights;
        const scores = Object.keys(weights).map(Number);
        const probabilities = Object.values(weights);

        // 加权随机选择
        const random = Math.random();
        let cumulative = 0;

        for (let i = 0; i < scores.length; i++) {
            cumulative += probabilities[i];
            if (random <= cumulative) {
                return scores[i];
            }
        }

        return 4; // 默认返回4分
    }

    /**
     * 加载保存的配置
     */
    function loadSavedConfig() {
        chrome.storage.sync.get(['strategy', 'rating', 'comment', 'delay'], function(result) {
            if (result.strategy) strategySelect.value = result.strategy;
            if (result.rating) ratingSelect.value = result.rating;
            if (result.comment) commentTextarea.value = result.comment;
            if (result.delay) delayInput.value = result.delay;

            handleStrategyChange();
        });
    }

    /**
     * 保存配置
     */
    function saveConfig() {
        const config = {
            strategy: strategySelect.value,
            rating: ratingSelect.value,
            comment: commentTextarea.value,
            delay: parseFloat(delayInput.value)
        };

        chrome.storage.sync.set(config);
    }

    /**
     * 处理自动填写
     */
    function handleAutoFill() {
        const config = {
            strategy: strategySelect.value,
            rating: ratingSelect.value,
            comment: commentTextarea.value,
            delay: parseFloat(delayInput.value) * 1000, // 转换为毫秒
            scoringStrategies: scoringStrategies
        };

        // 发送消息到内容脚本
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            chrome.tabs.sendMessage(tabs[0].id, {
                action: 'smartAutoFill',
                config: config
            }, function(response) {
                if (chrome.runtime.lastError) {
                    showStatus('请确保在评教页面使用此功能', 'error');
                } else if (response && response.success) {
                    showStatus(`✅ 自动填写完成！填写了 ${response.filledCount} 个评分项`, 'success');
                } else {
                    showStatus('自动填写失败，请检查页面', 'error');
                }
            });
        });
    }

    /**
     * 处理预览
     */
    function handlePreview() {
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            chrome.tabs.sendMessage(tabs[0].id, {
                action: 'preview'
            }, function(response) {
                if (chrome.runtime.lastError) {
                    showStatus('请在评教页面使用此功能', 'error');
                } else if (response && response.success) {
                    showStatus(`📋 找到 ${response.radioGroups} 个评分组，${response.textAreas} 个文本框`, 'success');
                } else {
                    showStatus('未找到评教表单', 'error');
                }
            });
        });
    }

    /**
     * 显示状态信息
     */
    function showStatus(message, type) {
        statusDiv.textContent = message;
        statusDiv.className = `status ${type}`;
        statusDiv.style.display = 'block';

        // 3秒后隐藏状态
        setTimeout(() => {
            statusDiv.style.display = 'none';
        }, 3000);
    }
});
