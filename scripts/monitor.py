#!/usr/bin/env python3
"""GrandNode性能监控脚本"""
import requests
import time
import json
import sys
from datetime import datetime


class GrandNodeMonitor:
    def __init__(self, base_url="http://localhost:8080"):
        self.base_url = base_url.rstrip("/")
        self.metrics = []
    
    def check_health(self):
        """健康检查"""
        try:
            start = time.time()
            response = requests.get(f"{self.base_url}/health", timeout=5)
            latency = (time.time() - start) * 1000
            
            return {
                "status": "healthy" if response.status_code == 200 else "unhealthy",
                "status_code": response.status_code,
                "latency_ms": round(latency, 2),
                "timestamp": datetime.now().isoformat()
            }
        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def check_homepage(self):
        """首页响应时间"""
        try:
            start = time.time()
            response = requests.get(self.base_url, timeout=10)
            latency = (time.time() - start) * 1000
            
            return {
                "endpoint": "homepage",
                "status_code": response.status_code,
                "latency_ms": round(latency, 2),
                "size_bytes": len(response.content),
                "timestamp": datetime.now().isoformat()
            }
        except requests.exceptions.RequestException as e:
            return {
                "endpoint": "homepage",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def check_api(self):
        """API响应时间"""
        endpoints = [
            "/api/products",
            "/api/categories",
            "/api/cart"
        ]
        
        results = []
        for endpoint in endpoints:
            try:
                start = time.time()
                response = requests.get(f"{self.base_url}{endpoint}", timeout=5)
                latency = (time.time() - start) * 1000
                
                results.append({
                    "endpoint": endpoint,
                    "status_code": response.status_code,
                    "latency_ms": round(latency, 2),
                    "timestamp": datetime.now().isoformat()
                })
            except requests.exceptions.RequestException as e:
                results.append({
                    "endpoint": endpoint,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })
        
        return results
    
    def run_checks(self):
        """运行所有检查"""
        print("🔍 GrandNode Performance Monitor")
        print("=" * 50)
        
        # 健康检查
        health = self.check_health()
        print(f"\n✓ Health Check: {health['status']}")
        if 'latency_ms' in health:
            print(f"  Latency: {health['latency_ms']}ms")
        
        # 首页检查
        homepage = self.check_homepage()
        print(f"\n✓ Homepage Check:")
        if 'latency_ms' in homepage:
            print(f"  Status: {homepage['status_code']}")
            print(f"  Latency: {homepage['latency_ms']}ms")
            print(f"  Size: {homepage['size_bytes']} bytes")
        else:
            print(f"  Error: {homepage.get('error')}")
        
        # API检查
        api_results = self.check_api()
        print(f"\n✓ API Checks:")
        for result in api_results:
            if 'latency_ms' in result:
                print(f"  {result['endpoint']}: {result['latency_ms']}ms (HTTP {result['status_code']})")
            else:
                print(f"  {result['endpoint']}: Error - {result.get('error')}")
        
        # 汇总
        all_results = {
            "health": health,
            "homepage": homepage,
            "api": api_results,
            "summary": {
                "total_checks": 1 + 1 + len(api_results),
                "timestamp": datetime.now().isoformat()
            }
        }
        
        return all_results
    
    def save_report(self, results, filename="monitor-report.json"):
        """保存监控报告"""
        with open(filename, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\n📊 Report saved to {filename}")


if __name__ == "__main__":
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8080"
    
    monitor = GrandNodeMonitor(base_url)
    results = monitor.run_checks()
    monitor.save_report(results)
