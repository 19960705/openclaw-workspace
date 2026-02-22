def factorial_recursive(n: int) -> int:
    """
    计算阶乘（递归实现）
    
    Args:
        n: 非负整数
        
    Returns:
        n 的阶乘
        
    Raises:
        ValueError: 如果 n 是负数
    """
    if n < 0:
        raise ValueError("阶乘只定义在非负整数上")
    if n == 0 or n == 1:
        return 1
    return n * factorial_recursive(n - 1)


def factorial_iterative(n: int) -> int:
    """
    计算阶乘（迭代实现）
    
    Args:
        n: 非负整数
        
    Returns:
        n 的阶乘
        
    Raises:
        ValueError: 如果 n 是负数
    """
    if n < 0:
        raise ValueError("阶乘只定义在非负整数上")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


# 示例用法
if __name__ == "__main__":
    print("=== 阶乘计算示例 ===")
    
    # 测试不同的输入
    test_numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    print("\n递归实现:")
    for num in test_numbers:
        print(f"  {num}! = {factorial_recursive(num)}")
    
    print("\n迭代实现:")
    for num in test_numbers:
        print(f"  {num}! = {factorial_iterative(num)}")
    
    # 性能对比（计算大一点的数）
    import time
    
    print("\n=== 性能对比 ===")
    large_num = 100
    
    start = time.time()
    factorial_recursive(large_num)
    recursive_time = time.time() - start
    
    start = time.time()
    factorial_iterative(large_num)
    iterative_time = time.time() - start
    
    print(f"计算 {large_num}! 耗时:")
    print(f"  递归: {recursive_time:.6f} 秒")
    print(f"  迭代: {iterative_time:.6f} 秒")
    print(f"  迭代快 {recursive_time / iterative_time:.1f} 倍")
