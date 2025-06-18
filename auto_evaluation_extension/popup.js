// 自动评教助手 - 弹窗脚本

document.addEventListener('DOMContentLoaded', function() {
    // 获取DOM元素
    const ratingSelect = document.getElementById('rating');
    const commentTextarea = document.getElementById('comment');
    const delayInput = document.getElementById('delay');
    const autoFillBtn = document.getElementById('autoFill');
    const previewBtn = document.getElementById('preview');
    const statusDiv = document.getElementById('status');

    // 加载保存的配置
    loadSavedConfig();

    // 绑定事件监听器
    autoFillBtn.addEventListener('click', handleAutoFill);
    previewBtn.addEventListener('click', handlePreview);

    // 保存配置到存储
    [ratingSelect, commentTextarea, delayInput].forEach(element => {
        element.addEventListener('change', saveConfig);
    });

    /**
     * 加载保存的配置
     */
    function loadSavedConfig() {
        chrome.storage.sync.get(['rating', 'comment', 'delay'], function(result) {
            if (result.rating) ratingSelect.value = result.rating;
            if (result.comment) commentTextarea.value = result.comment;
            if (result.delay) delayInput.value = result.delay;
        });
    }

    /**
     * 保存配置
     */
    function saveConfig() {
        const config = {
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
            rating: ratingSelect.value,
            comment: commentTextarea.value,
            delay: parseFloat(delayInput.value) * 1000 // 转换为毫秒
        };

        // 发送消息到内容脚本
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            chrome.tabs.sendMessage(tabs[0].id, {
                action: 'autoFill',
                config: config
            }, function(response) {
                if (chrome.runtime.lastError) {
                    showStatus('请确保在评教页面使用此功能', 'error');
                } else if (response && response.success) {
                    showStatus('自动填写完成！', 'success');
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
                    showStatus(`找到 ${response.count} 个评教项目`, 'success');
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
