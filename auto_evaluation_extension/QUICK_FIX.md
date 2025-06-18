# 🔧 扩展加载错误快速修复指南

## ❌ 错误信息
```
无法加载扩展
文件 ~\Desktop\auto_evaluation_extension
错误：Couldn't load icon icon16.png specified in icons.
```

## ✅ 解决方案

### 方案1：使用修复版manifest.json（推荐）

**已经修复完成！** 我已经更新了 `manifest.json` 文件，移除了图标引用。

**操作步骤：**
1. 确保使用最新的 `manifest.json` 文件
2. 在Chrome中重新加载扩展：
   - 打开 `chrome://extensions/`
   - 找到"自动评教助手"扩展
   - 点击刷新按钮 🔄
3. 扩展应该可以正常加载了

### 方案2：创建图标文件（可选）

如果您想要扩展图标：

1. **打开图标生成器**
   - 双击 `create_icons.html` 文件
   - 在浏览器中打开

2. **下载图标**
   - 点击"下载 icon16.png"按钮
   - 点击"下载 icon48.png"按钮
   - 点击"下载 icon128.png"按钮

3. **放置图标**
   - 将下载的3个图标文件放到扩展文件夹中
   - 恢复 manifest.json 中的图标配置

4. **重新加载扩展**

## 🚀 验证修复

加载成功后，您应该看到：
- ✅ 扩展出现在Chrome工具栏中
- ✅ 点击扩展图标显示弹窗界面
- ✅ 没有错误提示

## 📱 使用扩展

1. **访问评教页面**
   ```
   http://210.30.204.138/school/proj/evaluatevl-0/module/task/org/UJUMGRK4kyat8tEaH1z4QN/mytask
   ```

2. **打开扩展**
   - 点击浏览器工具栏中的扩展图标
   - 或按快捷键 `Ctrl+Shift+E`

3. **配置和使用**
   - 选择评分等级（1-5）
   - 输入或修改评语
   - 点击"自动填写"按钮

## 🔍 故障排除

### 如果扩展仍然无法加载：

1. **检查文件完整性**
   ```
   auto_evaluation_extension/
   ├── manifest.json ✅
   ├── popup.html ✅
   ├── popup.js ✅
   ├── content.js ✅
   ├── styles.css ✅
   └── README.md ✅
   ```

2. **检查Chrome版本**
   - 确保使用Chrome 88+版本
   - 更新到最新版本

3. **重新下载扩展**
   - 删除当前文件夹
   - 重新下载完整的扩展文件

4. **查看详细错误**
   - 在 `chrome://extensions/` 页面
   - 点击扩展的"详细信息"
   - 查看"错误"部分

## 📞 需要帮助？

如果问题仍然存在：
1. 检查控制台错误信息
2. 确认所有文件都在正确位置
3. 尝试重启Chrome浏览器
4. 使用Python脚本作为备选方案

---

**现在就试试吧！扩展应该可以正常工作了！** 🎉
