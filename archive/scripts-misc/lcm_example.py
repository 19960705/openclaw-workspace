def gcd(a: int, b: int) -> int:
    """计算两个数的最大公约数（使用欧几里得算法）"""
    while b != 0:
        a, b = b, a % b
    return a


def lcm(a: int, b: int) -> int:
    """计算两个数的最小公倍数"""
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // gcd(a, b)


# 示例用法
if __name__ == "__main__":
    num1 = 12
    num2 = 18
    
    print(f"GCD of {num1} and {num2} is: {gcd(num1, num2)}")
    print(f"LCM of {num1} and {num2} is: {lcm(num1, num2)}")
    
    # 更多示例
    test_cases = [(4, 6), (5, 7), (8, 12), (15, 20)]
    for x, y in test_cases:
        print(f"LCM({x}, {y}) = {lcm(x, y)}")
