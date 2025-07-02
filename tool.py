import os
import fnmatch
import shutil


def normalize_path(path, special_paths):
    if not path:
        return None

    path = path.strip()

    if '/' in path or '\\' in path:
        path = path.replace('\\', '/')
        parts = path.split('/')
        first_part = parts[0].lower()
        
        if first_part in special_paths:
            base_path = os.path.expanduser(special_paths[first_part])
            remaining_parts = parts[1:]
            
            if remaining_parts:
                return os.path.abspath(os.path.join(base_path, *remaining_parts))
            else:
                return os.path.abspath(base_path)
        else:
            return os.path.abspath(os.path.expanduser(path))

    if path.lower() in special_paths:
        path = special_paths[path.lower()]

    return os.path.abspath(os.path.expanduser(path))


def find_files(root, pattern, special_paths, recursive=True):
    root = normalize_path(root, special_paths)
    if not root or not os.path.exists(root):
        return []
    
    matches = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        filenames = [f for f in filenames if not f.startswith('.')]
        
        for filename in filenames:
            if fnmatch.fnmatch(filename, pattern):
                matches.append(os.path.join(dirpath, filename))
        
        if not recursive:
            break
    return matches


def count_hidden_files(root, special_paths):
    root = normalize_path(root, special_paths)
    if not root or not os.path.exists(root):
        return 0
    
    count = 0
    for dirpath, dirnames, filenames in os.walk(root):
        count += sum(1 for f in filenames if f.startswith('.'))
    return count


def create_file_or_folder(path, special_paths, is_folder=False):
    try:
        path = normalize_path(path, special_paths)
        if not path:
            print("❌ 路径无效")
            return False
        
        if is_folder:
            os.makedirs(path, exist_ok=True)
            print(f"✅ 文件夹已创建: {path}")
        else:
            parent_dir = os.path.dirname(path)
            if parent_dir and not os.path.exists(parent_dir):
                os.makedirs(parent_dir, exist_ok=True)
            
            if os.path.exists(path):
                print(f"⚠️  文件已存在: {path}")
                return True
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write("")
            print(f"✅ 文件已创建: {path}")
        return True
        
    except Exception as e:
        print(f"❌ 创建失败: {e}")
        return False


def delete_file_or_folder(path, special_paths):
    try:
        path = normalize_path(path, special_paths)
        if not path:
            print("❌ 路径无效")
            return False
        
        if os.path.isdir(path):
            shutil.rmtree(path)
            print(f"✅ 文件夹已删除: {path}")
        elif os.path.isfile(path):
            os.remove(path)
            print(f"✅ 文件已删除: {path}")
        else:
            print(f"❌ 路径不存在: {path}")
            return False
        return True
        
    except Exception as e:
        print(f"❌ 删除失败: {e}")
        return False


def modify_file_content(path, content, special_paths):
    try:
        path = normalize_path(path, special_paths)
        if not path:
            print("❌ 路径无效")
            return False
        
        if not os.path.isfile(path):
            print(f"❌ 文件不存在: {path}")
            return False
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 文件内容已修改: {path}")
        return True
        
    except Exception as e:
        print(f"❌ 修改失败: {e}")
        return False