import json
import base64
import time
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum
import random

# 模拟AI模型状态
class ModelStatus(Enum):
    IDLE = "空闲"
    PROCESSING = "处理中"
    READY = "就绪"

# 模拟缺陷类型
class DefectType(Enum):
    SCRATCH = "划痕"
    DENT = "凹陷"
    CRACK = "裂纹"
    CORROSION = "腐蚀"

# 模拟检测结果
class DetectionResult:
    def __init__(self, image_id: str):
        self.image_id = image_id
        self.timestamp = datetime.now()
        self.has_defect = False
        self.defects: List[Dict] = []
        self.processing_time = 0.0
        
    def add_defect(self, defect_type: DefectType, confidence: float, bbox: List[int], mask: List[List[int]]):
        """添加缺陷检测结果"""
        self.defects.append({
            "type": defect_type.value,
            "confidence": round(confidence, 3),
            "bbox": bbox,  # [x1, y1, x2, y2]
            "mask": mask,  # 分割掩码坐标
            "area": (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
        })
        self.has_defect = True
        
    def to_dict(self) -> Dict:
        """转换为字典格式"""
        return {
            "image_id": self.image_id,
            "timestamp": self.timestamp.isoformat(),
            "has_defect": self.has_defect,
            "defect_count": len(self.defects),
            "defects": self.defects,
            "processing_time": self.processing_time,
            "status": "success"
        }

# 模拟AI模型服务
class AIModelService:
    def __init__(self):
        self.status = ModelStatus.READY
        self.processed_count = 0
        
    def process_image(self, image_data: str) -> DetectionResult:
        """
        处理图像并返回检测结果
        image_data: base64编码的图像数据
        """
        if self.status != ModelStatus.READY:
            raise Exception("模型忙，请稍后重试")
            
        self.status = ModelStatus.PROCESSING
        start_time = time.time()
        
        # 模拟图像处理延迟
        time.sleep(0.5)
        
        # 生成模拟图像ID
        image_id = f"img_{self.processed_count:06d}"
        result = DetectionResult(image_id)
        
        # 随机生成0-3个缺陷（模拟AI检测结果）
        defect_count = random.randint(0, 3)
        
        for i in range(defect_count):
            # 随机选择缺陷类型
            defect_type = random.choice(list(DefectType))
            
            # 生成随机置信度 (0.7-0.95)
            confidence = random.uniform(0.7, 0.95)
            
            # 生成随机边界框 (模拟YOLO检测)
            bbox = [
                random.randint(50, 300),  # x1
                random.randint(50, 300),  # y1
                random.randint(350, 600),  # x2
                random.randint(350, 600)   # y2
            ]
            
            # 生成模拟分割掩码（简化版，模拟SAM输出）
            mask_points = []
            for _ in range(10):  # 简化为10个点
                mask_points.append([
                    random.randint(bbox[0], bbox[2]),
                    random.randint(bbox[1], bbox[3])
                ])
            
            result.add_defect(defect_type, confidence, bbox, mask_points)
        
        # 计算处理时间
        result.processing_time = time.time() - start_time
        self.processed_count += 1
        self.status = ModelStatus.READY
        
        return result
    
    def get_stats(self) -> Dict:
        """获取模型统计信息"""
        return {
            "status": self.status.value,
            "processed_count": self.processed_count,
            "uptime": "模拟运行中"
        }

# 模拟FastAPI后端服务
class BackendService:
    def __init__(self):
        self.model_service = AIModelService()
        self.results_history: List[Dict] = []
        
    def upload_image(self, image_base64: str) -> Dict:
        """
        上传图像并处理（模拟FastAPI接口）
        返回检测结果
        """
        try:
            # 验证base64数据（简化验证）
            if not image_base64 or len(image_base64) < 100:
                return {"error": "无效的图像数据", "status": "error"}
            
            # 调用AI模型处理图像
            result = self.model_service.process_image(image_base64)
            result_dict = result.to_dict()
            
            # 保存到历史记录
            self.results_history.append(result_dict)
            
            # 限制历史记录数量
            if len(self.results_history) > 100:
                self.results_history = self.results_history[-100:]
            
            return result_dict
            
        except Exception as e:
            return {"error": str(e), "status": "error"}
    
    def batch_process(self, image_list: List[str]) -> Dict:
        """批量处理图像（模拟批量接口）"""
        results = []
        total_time = 0
        
        for img_data in image_list:
            result = self.upload_image(img_data)
            if result.get("status") == "success":
                results.append(result)
                total_time += result.get("processing_time", 0)
        
        return {
            "batch_id": f"batch_{int(time.time())}",
            "total_images": len(image_list),
            "success_count": len(results),
            "total_time": round(total_time, 3),
            "avg_time": round(total_time / len(results), 3) if results else 0,
            "results": results
        }
    
    def get_system_info(self) -> Dict:
        """获取系统信息（模拟状态检查接口）"""
        return {
            "system": "工业零件智能质检Demo系统",
            "version": "1.0.0",
            "model": "YOLOv8 + SAM 集成模型",
            "model_stats": self.model_service.get_stats(),
            "history_count": len(self.results_history),
            "timestamp": datetime.now().isoformat()
        }

def main():
    """主函数：模拟系统运行"""
    print("=== 工业零件智能质检演示系统 ===\n")
    
    # 初始化后端服务
    backend = BackendService()
    
    # 获取系统信息
    print("1. 系统初始化...")
    sys_info = backend.get_system_info()
    print(f"   系统: {sys_info['system']}")
    print(f"   模型: {sys_info['model']}")
    print(f"   状态: {sys_info['model_stats']['status']}\n")
    
    # 模拟上传和处理图像
    print("2. 模拟图像处理...")
    
    # 生成模拟的base64图像数据（实际使用中应为真实的base64编码）
    mock_images = [
        "base64_mock_data_1_" + "x" * 100,
        "base64_mock_data_2_" + "x" * 100,
        "base64_mock_data_3_" + "x" * 100
    ]
    
    # 单张图像处理演示
    print("   - 单张图像处理:")
    single_result = backend.upload_image(mock_images[0])
    
    if single_result.get("status") == "success":
        print(f"     图像ID: {single_result['image_id']}")
        print(f"     是否有缺陷: {'是' if single_result['has_defect'] else '否'}")
        print(f"     缺陷数量: {single_result['defect_count']}")
        print(f"     处理时间: {single_result['processing_time']:.3f}秒")
        
        if single_result['defects']:
            print(f"     缺陷类型: {[d['type'] for d in single_result['defects']]}")
    else:
        print(f"     处理失败: {single_result.get('error')}")
    
    # 批量处理演示
    print("\n   - 批量图像处理 (3张):")
    batch_result = backend.batch_process(mock_images)
    
    print(f"     成功处理: {batch_result['success_count']}/{batch_result['total_images']}")
    print(f"     总时间: {batch_result['total_time']:.3f}秒")
    print(f"     平均时间: {batch_result['avg_time']:.3f}秒/张")
    
    # 性能对比展示
    print("\n3. 性能对比:")
    print(f"   - AI处理时间: {batch_result['avg_time']:.3f}秒/张")
    print("   - 传统人工质检: ~30秒/张")
    print("   - 效率提升: > 90%")
    
    # 最终统计
    print("\n4. 运行统计:")
    final_stats = backend.get_system_info()
    print(f"   已处理图像: {final_stats['model_stats']['processed_count']}")
    print(f"   历史记录: {final_stats['history_count']}条")
    print(f"   当前状态: {final_stats['model_stats']['status']}")
    
    print("\n=== 演示完成 ===")

if __name__ == "__main__":
    main()