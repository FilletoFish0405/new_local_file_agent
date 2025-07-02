from  tool_use import AIToolUseParser


class SimpleToolUseAgent:
    
    def __init__(self, api_key=None, base_url=None):
        self.parser = AIToolUseParser(api_key, base_url)
    
    def run(self):
        print("=" * 60)
        print("🤖 local_file agent")
        print("💡 支持的操作:")
        print("   • 查找文件: '找桌面上的PDF文件'")
        print("   • 统计隐藏文件: '统计主目录的隐藏文件'")
        print("   • 创建文件/文件夹: '在桌面创建test.txt'")
        print("   • 删除文件/文件夹: '删除temp.txt'")
        print("   • 修改文件内容: '修改config.txt内容为Hello'")
        print("   • 输入help来获取功能介绍")
        print("🔧 每次只执行一个操作，使用自然语言描述即可")
        print("-" * 60 )
        
        while True:
            try:
                user_input = input("\n🎯 请描述你要做的操作 > ").strip()
                
                if user_input.lower() in ('exit', 'quit', '退出'):
                    print("👋 再见！")
                    break
                
                if not user_input:
                    continue
                
                if user_input.lower() in ('help', '帮助'):
                    print("""
🔧 支持的操作类型：
📁 查找文件 - 在指定目录查找特定类型文件
📊 统计隐藏文件 - 统计目录下的隐藏文件数量
📝 创建文件/文件夹 - 创建新的文件或文件夹
🗑️  删除文件/文件夹 - 删除指定文件或文件夹
✏️  修改文件内容 - 修改现有文件的内容

💬 用自然语言描述你要做什么就行！
""")
                    continue
                
                print(f"\n🔄 处理中...")
                print("-" * 40)
                
                result = self.parser.process_user_input(user_input)
                print(f"\n✅ 操作完成!")
                    
            except (EOFError, KeyboardInterrupt):
                print("\n👋 程序已退出")
                break


def main():
    print("🚀 启动简化版Tool Use文件代理...")
    
    agent = SimpleToolUseAgent()
    agent.run()


if __name__ == "__main__":
    main()