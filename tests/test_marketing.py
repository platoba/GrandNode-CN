"""营销自动化模块测试"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

import pytest
from datetime import datetime, timedelta
from marketing_automation import (
    CouponGenerator,
    LoyaltyPointsCalculator,
    EmailCampaignAutomation
)


class TestCouponGenerator:
    """优惠券生成器测试"""
    
    def test_generate_code(self):
        """测试优惠券码生成"""
        code = CouponGenerator.generate_code(prefix="TEST", length=8)
        assert code.startswith("TEST")
        assert len(code) == 12  # TEST + 8位
    
    def test_batch_generate(self):
        """测试批量生成"""
        coupons = CouponGenerator.batch_generate(
            count=10,
            discount_type="percentage",
            discount_value=15.0,
            min_order_amount=100.0,
            valid_days=30
        )
        assert len(coupons) == 10
        assert all(c["discountValue"] == 15.0 for c in coupons)
        assert all(c["minOrderAmount"] == 100.0 for c in coupons)
        assert all(c["isActive"] for c in coupons)
    
    def test_unique_codes(self):
        """测试优惠券码唯一性"""
        coupons = CouponGenerator.batch_generate(count=100)
        codes = [c["code"] for c in coupons]
        assert len(codes) == len(set(codes))  # 无重复


class TestLoyaltyPointsCalculator:
    """会员积分计算器测试"""
    
    def test_calculate_order_points(self):
        """测试订单积分计算"""
        # 青铜会员 1倍
        assert LoyaltyPointsCalculator.calculate_order_points(100, "bronze") == 100
        # 白银会员 1.2倍
        assert LoyaltyPointsCalculator.calculate_order_points(100, "silver") == 120
        # 黄金会员 1.5倍
        assert LoyaltyPointsCalculator.calculate_order_points(100, "gold") == 150
        # 铂金会员 2倍
        assert LoyaltyPointsCalculator.calculate_order_points(100, "platinum") == 200
    
    def test_get_tier(self):
        """测试等级判定"""
        assert LoyaltyPointsCalculator.get_tier(0)["tier"] == "bronze"
        assert LoyaltyPointsCalculator.get_tier(1000)["tier"] == "silver"
        assert LoyaltyPointsCalculator.get_tier(5000)["tier"] == "gold"
        assert LoyaltyPointsCalculator.get_tier(10000)["tier"] == "platinum"
    
    def test_points_to_next_tier(self):
        """测试升级所需积分"""
        result = LoyaltyPointsCalculator.points_to_next_tier(500)
        assert result["nextTier"] == "silver"
        assert result["pointsNeeded"] == 500  # 1000 - 500
        
        result = LoyaltyPointsCalculator.points_to_next_tier(10000)
        assert result["nextTier"] is None  # 已达最高等级


class TestEmailCampaignAutomation:
    """邮件营销自动化测试"""
    
    def test_generate_welcome_email(self):
        """测试欢迎邮件生成"""
        customer = {
            "name": "张三",
            "email": "zhangsan@example.com",
            "coupon_code": "WELCOME10"
        }
        email = EmailCampaignAutomation.generate_email("welcome", customer)
        assert email["to"] == "zhangsan@example.com"
        assert "欢迎" in email["subject"]
        assert "张三" in email["body"]
        assert "WELCOME10" in email["body"]
    
    def test_generate_abandoned_cart_email(self):
        """测试弃购邮件生成"""
        customer = {
            "name": "李四",
            "email": "lisi@example.com",
            "cart_items_count": 3,
            "coupon_code": "CART20"
        }
        email = EmailCampaignAutomation.generate_email("abandoned_cart", customer)
        assert "购物车" in email["subject"]
        assert "3" in email["body"]
    
    def test_schedule_campaign(self):
        """测试批量调度"""
        customers = [
            {"name": "客户1", "email": "c1@example.com", "coupon_code": "CODE1"},
            {"name": "客户2", "email": "c2@example.com", "coupon_code": "CODE2"}
        ]
        emails = EmailCampaignAutomation.schedule_campaign(
            customers, "welcome", send_delay_hours=24
        )
        assert len(emails) == 2
        assert all("scheduledSendTime" in e for e in emails)
    
    def test_invalid_template(self):
        """测试无效模板"""
        with pytest.raises(ValueError):
            EmailCampaignAutomation.generate_email("invalid", {})


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
