#!/usr/bin/env python3
"""
GrandNode-CN 营销自动化模块
功能：优惠券批量生成、会员积分计算、邮件营销自动化
"""
import json
import random
import string
from datetime import datetime, timedelta
from typing import List, Dict
import hashlib


class CouponGenerator:
    """优惠券批量生成器"""
    
    @staticmethod
    def generate_code(prefix: str = "GN", length: int = 8) -> str:
        """生成唯一优惠券码"""
        chars = string.ascii_uppercase + string.digits
        code = ''.join(random.choices(chars, k=length))
        return f"{prefix}{code}"
    
    @staticmethod
    def batch_generate(
        count: int,
        discount_type: str = "percentage",  # percentage | fixed
        discount_value: float = 10.0,
        min_order_amount: float = 0.0,
        valid_days: int = 30,
        prefix: str = "GN"
    ) -> List[Dict]:
        """
        批量生成优惠券
        
        Args:
            count: 生成数量
            discount_type: 折扣类型（percentage=百分比, fixed=固定金额）
            discount_value: 折扣值（百分比或金额）
            min_order_amount: 最低订单金额
            valid_days: 有效天数
            prefix: 优惠券前缀
        """
        coupons = []
        now = datetime.now()
        expire_date = now + timedelta(days=valid_days)
        
        for _ in range(count):
            code = CouponGenerator.generate_code(prefix)
            coupon = {
                "code": code,
                "discountType": discount_type,
                "discountValue": discount_value,
                "minOrderAmount": min_order_amount,
                "validFrom": now.isoformat(),
                "validTo": expire_date.isoformat(),
                "usageLimit": 1,
                "usedCount": 0,
                "isActive": True,
                "createdAt": now.isoformat()
            }
            coupons.append(coupon)
        
        return coupons


class LoyaltyPointsCalculator:
    """会员积分计算器"""
    
    # 会员等级配置
    TIERS = {
        "bronze": {"min_points": 0, "multiplier": 1.0, "name": "青铜会员"},
        "silver": {"min_points": 1000, "multiplier": 1.2, "name": "白银会员"},
        "gold": {"min_points": 5000, "multiplier": 1.5, "name": "黄金会员"},
        "platinum": {"min_points": 10000, "multiplier": 2.0, "name": "铂金会员"}
    }
    
    @staticmethod
    def calculate_order_points(order_amount: float, tier: str = "bronze") -> int:
        """计算订单积分（1元=1积分 * 等级倍数）"""
        multiplier = LoyaltyPointsCalculator.TIERS.get(tier, {}).get("multiplier", 1.0)
        return int(order_amount * multiplier)
    
    @staticmethod
    def get_tier(total_points: int) -> Dict:
        """根据总积分获取会员等级"""
        for tier_key in reversed(list(LoyaltyPointsCalculator.TIERS.keys())):
            tier = LoyaltyPointsCalculator.TIERS[tier_key]
            if total_points >= tier["min_points"]:
                return {"tier": tier_key, **tier}
        return {"tier": "bronze", **LoyaltyPointsCalculator.TIERS["bronze"]}
    
    @staticmethod
    def points_to_next_tier(current_points: int) -> Dict:
        """计算距离下一等级所需积分"""
        current_tier = LoyaltyPointsCalculator.get_tier(current_points)
        tier_keys = list(LoyaltyPointsCalculator.TIERS.keys())
        current_index = tier_keys.index(current_tier["tier"])
        
        if current_index == len(tier_keys) - 1:
            return {"nextTier": None, "pointsNeeded": 0, "message": "已达最高等级"}
        
        next_tier_key = tier_keys[current_index + 1]
        next_tier = LoyaltyPointsCalculator.TIERS[next_tier_key]
        points_needed = next_tier["min_points"] - current_points
        
        return {
            "nextTier": next_tier_key,
            "nextTierName": next_tier["name"],
            "pointsNeeded": points_needed
        }


class EmailCampaignAutomation:
    """邮件营销自动化"""
    
    TEMPLATES = {
        "welcome": {
            "subject": "欢迎加入 {store_name}！",
            "body": "亲爱的 {name}，\n\n感谢您注册成为我们的会员！\n\n首单立减 {discount}%，优惠码：{coupon_code}\n\n祝购物愉快！"
        },
        "abandoned_cart": {
            "subject": "您的购物车还有商品未结算",
            "body": "亲爱的 {name}，\n\n您有 {cart_items_count} 件商品在购物车中。\n\n现在下单享受 {discount}% 折扣！优惠码：{coupon_code}\n\n优惠有效期至 {expire_date}"
        },
        "reactivation": {
            "subject": "好久不见！专属优惠等您领取",
            "body": "亲爱的 {name}，\n\n我们已经 {days_inactive} 天没见到您了！\n\n特别为您准备了 {discount}% 折扣，优惠码：{coupon_code}\n\n期待您的回归！"
        }
    }
    
    @staticmethod
    def generate_email(
        template_type: str,
        customer_data: Dict,
        store_name: str = "GrandNode商城"
    ) -> Dict:
        """
        生成邮件内容
        
        Args:
            template_type: 模板类型（welcome | abandoned_cart | reactivation）
            customer_data: 客户数据（name, email, coupon_code等）
            store_name: 商城名称
        """
        template = EmailCampaignAutomation.TEMPLATES.get(template_type)
        if not template:
            raise ValueError(f"Unknown template type: {template_type}")
        
        # 合并默认值
        data = {
            "store_name": store_name,
            "discount": 10,
            "expire_date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
            **customer_data
        }
        
        subject = template["subject"].format(**data)
        body = template["body"].format(**data)
        
        return {
            "to": customer_data.get("email"),
            "subject": subject,
            "body": body,
            "templateType": template_type,
            "generatedAt": datetime.now().isoformat()
        }
    
    @staticmethod
    def schedule_campaign(
        customer_list: List[Dict],
        template_type: str,
        send_delay_hours: int = 0
    ) -> List[Dict]:
        """
        批量调度邮件营销活动
        
        Args:
            customer_list: 客户列表 [{"name": "张三", "email": "...", ...}, ...]
            template_type: 邮件模板类型
            send_delay_hours: 延迟发送小时数
        """
        scheduled_emails = []
        send_time = datetime.now() + timedelta(hours=send_delay_hours)
        
        for customer in customer_list:
            email = EmailCampaignAutomation.generate_email(template_type, customer)
            email["scheduledSendTime"] = send_time.isoformat()
            scheduled_emails.append(email)
        
        return scheduled_emails


def main():
    """CLI 入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="GrandNode-CN 营销自动化工具")
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    
    # 优惠券生成
    coupon_parser = subparsers.add_parser("coupon", help="批量生成优惠券")
    coupon_parser.add_argument("--count", type=int, default=100, help="生成数量")
    coupon_parser.add_argument("--discount", type=float, default=10.0, help="折扣值")
    coupon_parser.add_argument("--type", choices=["percentage", "fixed"], default="percentage")
    coupon_parser.add_argument("--min-order", type=float, default=0.0, help="最低订单金额")
    coupon_parser.add_argument("--days", type=int, default=30, help="有效天数")
    coupon_parser.add_argument("--output", default="coupons.json", help="输出文件")
    
    # 积分计算
    points_parser = subparsers.add_parser("points", help="计算会员积分")
    points_parser.add_argument("--amount", type=float, required=True, help="订单金额")
    points_parser.add_argument("--tier", choices=["bronze", "silver", "gold", "platinum"], 
                               default="bronze", help="会员等级")
    
    # 邮件营销
    email_parser = subparsers.add_parser("email", help="生成营销邮件")
    email_parser.add_argument("--template", choices=["welcome", "abandoned_cart", "reactivation"],
                             required=True, help="邮件模板")
    email_parser.add_argument("--customer", required=True, help="客户数据JSON文件")
    email_parser.add_argument("--output", default="emails.json", help="输出文件")
    
    args = parser.parse_args()
    
    if args.command == "coupon":
        coupons = CouponGenerator.batch_generate(
            count=args.count,
            discount_type=args.type,
            discount_value=args.discount,
            min_order_amount=args.min_order,
            valid_days=args.days
        )
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(coupons, f, ensure_ascii=False, indent=2)
        print(f"✅ 已生成 {len(coupons)} 张优惠券 → {args.output}")
    
    elif args.command == "points":
        points = LoyaltyPointsCalculator.calculate_order_points(args.amount, args.tier)
        tier_info = LoyaltyPointsCalculator.get_tier(points)
        next_tier = LoyaltyPointsCalculator.points_to_next_tier(points)
        print(f"订单金额: ¥{args.amount}")
        print(f"获得积分: {points}")
        print(f"当前等级: {tier_info['name']} ({tier_info['tier']})")
        if next_tier['nextTier']:
            print(f"距离 {next_tier['nextTierName']} 还需: {next_tier['pointsNeeded']} 积分")
    
    elif args.command == "email":
        with open(args.customer, 'r', encoding='utf-8') as f:
            customers = json.load(f)
        
        emails = EmailCampaignAutomation.schedule_campaign(customers, args.template)
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(emails, f, ensure_ascii=False, indent=2)
        print(f"✅ 已生成 {len(emails)} 封营销邮件 → {args.output}")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
