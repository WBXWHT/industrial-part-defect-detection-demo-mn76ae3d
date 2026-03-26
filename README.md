# industrial-part-defect-detection-demo

工业零件缺陷检测与分割演示系统

项目经历：我曾参与“工业零件智能质检Demo系统”项目。针对传统质检效率低的问题，我基于YOLOv8与SAM模型开发了一个可视化原型系统，实现了零件缺陷的自动定位与分割。我负责后端API搭建（FastAPI）与前端交互界面开发（Vue.js），并集成了模型测试工具以评估不同场景下的性能。该系统在内部测试中，将单张图片的缺陷分析时间从人工约30秒缩短至2秒内，演示后获得了潜在客户技术团队的好评。

## 运行
```bash
pip install -r requirements.txt
python main.py
```