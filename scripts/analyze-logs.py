#!/usr/bin/env python3
"""GrandNode日志分析工具"""
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime


class LogAnalyzer:
    def __init__(self, log_file):
        self.log_file = log_file
        self.errors = []
        self.warnings = []
        self.requests = []
        self.slow_queries = []
    
    def parse_log(self):
        """解析日志文件"""
        with open(self.log_file) as f:
            for line in f:
                # 错误日志
                if "ERROR" in line or "Exception" in line:
                    self.errors.append(line.strip())
                
                # 警告日志
                if "WARN" in line or "WARNING" in line:
                    self.warnings.append(line.strip())
                
                # HTTP请求（Nginx日志格式）
                if " HTTP/" in line:
                    self.requests.append(self._parse_request(line))
                
                # 慢查询
                if "slow query" in line.lower() or "timeout" in line.lower():
                    self.slow_queries.append(line.strip())
    
    def _parse_request(self, line):
        """解析HTTP请求行"""
        # 简化的Nginx日志解析
        match = re.search(r'"(\w+) ([^\s]+) HTTP/[\d.]+" (\d+) (\d+)', line)
        if match:
            return {
                "method": match.group(1),
                "path": match.group(2),
                "status": int(match.group(3)),
                "size": int(match.group(4))
            }
        return None
    
    def analyze(self):
        """分析日志"""
        print("📊 GrandNode Log Analysis")
        print("=" * 60)
        
        # 错误统计
        print(f"\n🔴 Errors: {len(self.errors)}")
        if self.errors:
            error_types = Counter([e.split(":")[0] if ":" in e else "Unknown" for e in self.errors[:100]])
            for error_type, count in error_types.most_common(5):
                print(f"  - {error_type}: {count}")
        
        # 警告统计
        print(f"\n🟡 Warnings: {len(self.warnings)}")
        if self.warnings:
            print(f"  (showing first 3)")
            for warning in self.warnings[:3]:
                print(f"  - {warning[:80]}...")
        
        # HTTP请求统计
        valid_requests = [r for r in self.requests if r]
        print(f"\n🌐 HTTP Requests: {len(valid_requests)}")
        if valid_requests:
            # 状态码分布
            status_codes = Counter([r["status"] for r in valid_requests])
            print("  Status codes:")
            for code, count in sorted(status_codes.items()):
                print(f"    {code}: {count}")
            
            # 最常访问的路径
            paths = Counter([r["path"] for r in valid_requests])
            print("  Top paths:")
            for path, count in paths.most_common(5):
                print(f"    {path}: {count}")
        
        # 慢查询
        print(f"\n🐌 Slow Queries: {len(self.slow_queries)}")
        if self.slow_queries:
            for query in self.slow_queries[:3]:
                print(f"  - {query[:80]}...")
        
        # 总结
        print(f"\n📈 Summary:")
        print(f"  Total lines analyzed: {len(self.errors) + len(self.warnings) + len(self.requests)}")
        print(f"  Error rate: {len(self.errors) / max(len(valid_requests), 1) * 100:.2f}%")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze-logs.py <log-file>")
        sys.exit(1)
    
    analyzer = LogAnalyzer(sys.argv[1])
    analyzer.parse_log()
    analyzer.analyze()
