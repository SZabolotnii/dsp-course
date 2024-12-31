#!/usr/bin/env python3

import os
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path

class ResourceOrganizer:
    def __init__(self, backup_path: str, resources_path: str):
        self.backup_path = Path(backup_path)
        self.resources_path = Path(resources_path)
        self.file_mapping = {}
        
    def read_file_mapping(self):
        """Читаємо files.xml для створення мапінгу хешів до оригінальних імен"""
        files_xml = self.backup_path / 'files.xml'
        if not files_xml.exists():
            print("files.xml not found")
            return
            
        tree = ET.parse(files_xml)
        root = tree.getroot()
        
        for file_elem in root.findall('.//file'):
            contenthash = file_elem.find('contenthash').text
            filename = file_elem.find('filename').text
            if filename and filename != '.':
                self.file_mapping[contenthash] = filename
                
    def categorize_file(self, filename: str) -> str:
        """Визначаємо категорію файлу на основі його імені та розширення"""
        lower_name = filename.lower()
        
        # Презентації
        if any(keyword in lower_name for keyword in ['лекція', 'презентація', 'lecture']):
            return 'presentations'
            
        # Приклади
        if any(keyword in lower_name for keyword in ['приклад', 'example', 'demo']):
            return 'examples'
            
        # Інструменти
        if any(keyword in lower_name for keyword in ['tool', 'utility', 'програма']):
            return 'tools'
            
        # Все інше
        return 'supplementary'
        
    def organize(self):
        """Організовуємо файли по категоріях"""
        print("Starting resource organization...")
        
        # Спочатку читаємо мапінг файлів
        self.read_file_mapping()
        
        # Проходимо по всіх директоріях з хешами
        for hash_dir in self.resources_path.glob('[0-9a-f][0-9a-f]'):
            if not hash_dir.is_dir() or len(hash_dir.name) != 2:
                continue
                
            for hash_file in hash_dir.glob('*'):
                if not hash_file.is_file():
                    continue
                    
                contenthash = hash_file.name
                if contenthash in self.file_mapping:
                    original_name = self.file_mapping[contenthash]
                    category = self.categorize_file(original_name)
                    
                    # Створюємо директорію категорії, якщо вона не існує
                    category_dir = self.resources_path / category
                    category_dir.mkdir(exist_ok=True)
                    
                    # Копіюємо файл з оригінальним іменем
                    dest_path = category_dir / original_name
                    shutil.copy2(hash_file, dest_path)
                    print(f"Moved {original_name} to {category}/")
                    
        # Видаляємо директорії з хешами після переміщення
        for hash_dir in self.resources_path.glob('[0-9a-f][0-9a-f]'):
            if hash_dir.is_dir() and len(hash_dir.name) == 2:
                shutil.rmtree(hash_dir)
                
        print("\nResource organization completed!")
        
        # Створюємо README для кожної категорії
        self._create_category_readmes()
        
    def _create_category_readmes(self):
        """Створюємо README.md файли для кожної категорії"""
        readmes = {
            'presentations': """# Презентації та лекційні матеріали

Цей каталог містить презентації та матеріали лекцій з курсу цифрової обробки сигналів.

## Вміст
""",
            'examples': """# Приклади та демонстрації

Цей каталог містить приклади та демонстраційні матеріали для практичного засвоєння курсу.

## Вміст
""",
            'tools': """# Інструменти та утиліти

Цей каталог містить програмні інструменти та утиліти для роботи з цифровою обробкою сигналів.

## Вміст
""",
            'supplementary': """# Додаткові матеріали

Цей каталог містить додаткові навчальні матеріали та ресурси для поглибленого вивчення курсу.

## Вміст
"""
        }
        
        # Додаємо список файлів до кожного README
        for category, readme_content in readmes.items():
            category_dir = self.resources_path / category
            if category_dir.exists():
                files = [f.name for f in category_dir.glob('*') if f.is_file() and f.name != 'README.md']
                if files:
                    readme_content += "\n".join([f"- {file}" for file in sorted(files)])
                    
                with open(category_dir / 'README.md', 'w', encoding='utf-8') as f:
                    f.write(readme_content)

def main():
    organizer = ResourceOrganizer(
        backup_path='/home/docsa/dsp-course/moodle-course-dsp',
        resources_path='/home/docsa/dsp-course/resources'
    )
    organizer.organize()

if __name__ == "__main__":
    main()