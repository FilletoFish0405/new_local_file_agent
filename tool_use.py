import json
from typing import List, Dict
from openai import OpenAI
from tool import *


class AIToolUseParser:
    
    def __init__(self, api_key=None, base_url=None):
        self.file_types = {
            "pdf": "*.pdf", "txt": "*.txt", "docx": "*.docx", "xlsx": "*.xlsx",
            "jpg": "*.jpg", "png": "*.png", "jpeg": "*.jpeg", "doc": "*.doc",
            "xls": "*.xls", "ppt": "*.ppt", "pptx": "*.pptx"
        }
        
        self.special_paths = {
            'desktop': '~/Desktop', '桌面': '~/Desktop',
            'downloads': '~/Downloads', '下载': '~/Downloads',
            'documents': '~/Documents', '文档': '~/Documents',
            'home': '~', '主目录': '~'
        }
        
        self.client = OpenAI(
            api_key=api_key ",
            base_url=base_url 
        )
        
        self.tools = self._define_tools()
    
    def _define_tools(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "find_files",
                    "description": "在指定目录中查找特定类型的文件",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "root": {
                                "type": "string",
                                "description": "搜索的根目录路径，支持特殊路径如'desktop', 'documents'等"
                            },
                            "file_extension": {
                                "type": "string",
                                "description": "文件扩展名，如'pdf', 'txt', 'jpg'等"
                            },
                            "recursive": {
                                "type": "boolean",
                                "description": "是否递归搜索子目录",
                                "default": True
                            }
                        },
                        "required": ["root", "file_extension"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "count_hidden_files",
                    "description": "统计指定目录下的隐藏文件数量",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "root": {
                                "type": "string",
                                "description": "要统计的目录路径"
                            }
                        },
                        "required": ["root"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "create_file_or_folder",
                    "description": "创建文件或文件夹",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "要创建的文件或文件夹路径"
                            },
                            "is_folder": {
                                "type": "boolean",
                                "description": "是否创建文件夹（true）还是文件（false）",
                                "default": False
                            }
                        },
                        "required": ["path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_file_or_folder",
                    "description": "删除文件或文件夹",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "要删除的文件或文件夹路径"
                            }
                        },
                        "required": ["path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "modify_file_content",
                    "description": "修改文件内容",
                    "parameters": {     
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "要修改的文件路径。如果只提供文件名（如test.txt），将在桌面查找。支持完整路径如desktop/test.txt"
                            },
                            "content": {
                                "type": "string",
                                "description": "要写入的新内容"
                            }
                        },
                        "required": ["path", "content"]
                    }
                }
            }
        ]
    
    def execute_tool_call(self, tool_call) -> str:
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        
        print(f"🔧 执行工具: {function_name}")
        print(f"📋 关键信息: {arguments}")
        
        try:
            if function_name == "find_files":
                root = arguments.get("root", ".")
                file_extension = arguments.get("file_extension")
                recursive = arguments.get("recursive", True)
                
                if file_extension not in self.file_types:
                    return f"❌ 不支持的文件类型: {file_extension}"
                
                pattern = self.file_types[file_extension]
                files = find_files(root, pattern, self.special_paths, recursive)
                
                if files:
                    result = f"✅ 在{root}中找到 {len(files)} 个{file_extension}文件:\n"
                    for i, file_path in enumerate(files[:10], 1):
                        result += f"  {i}. {file_path}\n"
                    if len(files) > 10:
                        result += f"  ... 还有 {len(files) - 10} 个文件"
                    return result
                else:
                    return f"📭 在{root}中未找到{file_extension}文件"
            
            elif function_name == "count_hidden_files":
                root = arguments.get("root", ".")
                count = count_hidden_files(root, self.special_paths)
                return f"✅ 在{root}中找到 {count} 个隐藏文件"
            
            elif function_name == "create_file_or_folder":
                path = arguments.get("path")
                is_folder = arguments.get("is_folder", False)

                if create_file_or_folder(path, self.special_paths, is_folder):
                    return f"✅ 成功创建{'文件夹' if is_folder else '文件'}: {path}"
                else:
                    return f"❌ 创建失败: {path}"
            
            elif function_name == "delete_file_or_folder":
                path = arguments.get("path")
                if delete_file_or_folder(path, self.special_paths):
                    return f"✅ 成功删除: {path}"
                else:
                    return f"❌ 删除失败: {path}"
            
            elif function_name == "modify_file_content":
                path = arguments.get("path")
                content = arguments.get("content", "")
                
                if modify_file_content(path, content, self.special_paths):
                    return f"✅ 成功修改文件内容: {path}"
                else:
                    return f"❌ 修改失败: {path}"
            
            else:
                return f"❌ 未知的工具函数: {function_name}"
                
        except Exception as e:
            return f"❌ 执行工具时出错: {str(e)}"
    
    def process_user_input(self, user_input: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model="qwen-max",
                messages=[
                    {
                        "role": "system",
                        "content": """你是一个文件管理助手。根据用户的请求，选择合适的工具来完成单个文件操作任务。

可用工具：
- find_files: 查找特定类型的文件
- count_hidden_files: 统计隐藏文件数量
- create_file_or_folder: 创建文件或文件夹
- delete_file_or_folder: 删除文件或文件夹
- modify_file_content: 修改文件内容

请根据用户请求选择一个合适的工具执行操作。每次只执行一个操作。

用中文回复，简洁明了。"""
                    },
                    {
                        "role": "user",
                        "content": user_input
                    }
                ],
                tools=self.tools,
                tool_choice="auto"
            )
            
            assistant_message = response.choices[0].message
            
            if assistant_message.tool_calls:
                print("🤖 AI选择执行工具:")
                
                tool_call = assistant_message.tool_calls[0]
                result = self.execute_tool_call(tool_call)
                
                print(f"📄 执行结果: {result}")
                return result
            
            else:
                return assistant_message.content or "❌ 无法理解您的请求，请重新描述"
                
        except Exception as e:
            error_msg = f"❌ 处理请求时出错: {str(e)}"
            print(error_msg)
            return error_msg
