"""
模块：优惠券与账单结算系统
特性：支持满减券、百分比折扣、VIP 折扣计算及金额边界校验
"""
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class CartItem:
    name: str
    price: float
    quantity: int

    @property
    def total(self) -> float:
        return self.price * self.quantity


class DiscountCalculator:
    def __init__(self, items: List[CartItem], is_vip: bool = False):
        self.items = items
        self.is_vip = is_vip

    @property
    def raw_total(self) -> float:
        """商品原始总金额"""
        return sum(item.total for item in self.items)

    def apply_coupon(self, coupon_type: str, value: float) -> float:
        """
        计算折扣后的最终金额
        :param coupon_type: 'percent' (如 0.88 代表八八折) 或 'direct' (如 20 代表直减 20 元)
        :param value: 折扣数值
        """
        current_total = self.raw_total

        # 1. 基础折扣
        if coupon_type == "percent":
            if not (0 < value <= 1.0):
                raise ValueError("百分比折扣必须在 (0, 1] 之间")
            current_total *= value
        elif coupon_type == "direct":
            if value < 0:
                raise ValueError("直减金额不能为负数")
            current_total = max(0.0, current_total - value)
        else:
            raise ValueError(f"未知的优惠券类型: {coupon_type}")

        # 2. 叠加 VIP 折扣（95折）
        if self.is_vip:
            current_total *= 0.95

        return round(current_total, 2)

    def print_bill(self, coupon_type: str, value: float) -> None:
        """打印小票明细"""
        print("====== 购物结算清单 ======")
        for item in self.items:
            print(f"- {item.name} x{item.quantity}: ¥{item.total:.2f}")
        print("--------------------------")
        print(f"原价总计:   ¥{self.raw_total:.2f}")
        print(f"用户等级:   {'VIP 尊享' if self.is_vip else '普通用户'}")

        final_price = self.apply_coupon(coupon_type, value)
        saved = self.raw_total - final_price
        print(f"实付金额:   ¥{final_price:.2f}")
        print(f"总计节省:   ¥{saved:.2f}")
        print("==========================")


if __name__ == "__main__":
    # 模拟购物车测试
    cart = [
        CartItem(name="机械键盘", price=399.0, quantity=1),
        CartItem(name="降噪耳机", price=599.0, quantity=1),
        CartItem(name="超大鼠标垫", price=49.0, quantity=2),
    ]

    # 初始化计算器（VIP 客户）
    calculator = DiscountCalculator(cart, is_vip=True)

    # 使用一张“直减 100 元”的优惠券
    calculator.print_bill(coupon_type="direct", value=100.0)