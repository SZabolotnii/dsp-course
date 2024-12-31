#!/usr/bin/env python3
"""
Скрипт для міграції курсу з Moodle backup у GitHub репозиторій.
Версія з організацією контенту
"""

import os
import logging
from pathlib import Path
import xml.etree.ElementTree as ET
import shutil
import json
import re

class MoodleMigration:
    def __init__(self, backup_path: str, repo_path: str):
        self.backup_path = Path(backup_path)
        self.repo_path = Path(repo_path)
        self.setup_logging()
        self.file_mapping = {}
        
    def setup_logging(self):
        """Налаштування логування"""
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('migration.log')
            ]
        )
        self.logger = logging

    def create_directory_structure(self):
        """Створення базової структури репозиторію"""
        directories = [
            'course-info',
            'lectures',
            'labs',
            'resources',
            'assessment'
        ]
        
        for dir_name in directories:
            directory = self.repo_path / dir_name
            directory.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Created directory: {directory}")

    def parse_files_xml(self):
        """Парсинг files.xml для створення мапінгу файлів"""
        files_xml = self.backup_path / 'files.xml'
        if not files_xml.exists():
            self.logger.error("files.xml not found")
            return
            
        tree = ET.parse(files_xml)
        root = tree.getroot()
        
        for file_elem in root.findall('.//file'):
            file_id = file_elem.get('id')
            contenthash = file_elem.find('contenthash').text
            filename = file_elem.find('filename').text
            
            if filename != '.':
                self.file_mapping[contenthash] = filename
                self.logger.debug(f"Mapped {contenthash} to {filename}")

    def organize_lecture_files(self):
        """Організація файлів лекцій"""
        lectures_dir = self.repo_path / 'lectures'
        lectures_dir.mkdir(exist_ok=True)

        # Шаблон для пошуку файлів лекцій
        lecture_pattern = re.compile(r'(\d+)[-].*Лекція.*\.pdf')

        for contenthash, filename in self.file_mapping.items():
            match = lecture_pattern.match(filename)
            if match:
                lecture_num = match.group(1)
                lecture_dir = lectures_dir / f'lecture_{lecture_num}'
                lecture_dir.mkdir(exist_ok=True)
                
                source = self.backup_path / 'files' / contenthash[:2] / contenthash
                if source.exists():
                    destination = lecture_dir / filename
                    shutil.copy2(source, destination)
                    self.logger.info(f"Copied lecture: {filename}")

    def organize_lab_files(self):
        """Організація файлів лабораторних робіт"""
        labs_dir = self.repo_path / 'labs'
        labs_dir.mkdir(exist_ok=True)

        # Шаблон для пошуку файлів лабораторних
        lab_pattern = re.compile(r'(ЛР\d+[-]\d+|Лабораторн[аі] робот[аи] \d+).*\.pdf')

        for contenthash, filename in self.file_mapping.items():
            if lab_pattern.match(filename):
                source = self.backup_path / 'files' / contenthash[:2] / contenthash
                if source.exists():
                    destination = labs_dir / filename
                    shutil.copy2(source, destination)
                    self.logger.info(f"Copied lab: {filename}")

    def organize_course_info(self):
        """Організація інформації про курс"""
        info_dir = self.repo_path / 'course-info'
        info_dir.mkdir(exist_ok=True)

        # Шаблони для пошуку файлів курсу
        info_patterns = [
            r'Силабус.*\.pdf',
            r'Анотація.*\.pdf',
            r'Критерії оцінювання.*\.pdf'
        ]

        for contenthash, filename in self.file_mapping.items():
            if any(re.match(pattern, filename) for pattern in info_patterns):
                source = self.backup_path / 'files' / contenthash[:2] / contenthash
                if source.exists():
                    destination = info_dir / filename
                    shutil.copy2(source, destination)
                    self.logger.info(f"Copied course info: {filename}")

    def organize_assessment(self):
        """Організація матеріалів для оцінювання"""
        assessment_dir = self.repo_path / 'assessment'
        assessment_dir.mkdir(exist_ok=True)

        # Шаблони для пошуку файлів оцінювання
        assessment_patterns = [
            r'Екзаменаційні білети.*\.pdf',
            r'Питання на іспит.*\.pdf',
            r'.*варіанти.*\.(pdf|png)'
        ]

        for contenthash, filename in self.file_mapping.items():
            if any(re.match(pattern, filename, re.IGNORECASE) for pattern in assessment_patterns):
                source = self.backup_path / 'files' / contenthash[:2] / contenthash
                if source.exists():
                    destination = assessment_dir / filename
                    shutil.copy2(source, destination)
                    self.logger.info(f"Copied assessment: {filename}")

    def run(self):
        """Запуск процесу міграції"""
        self.logger.info("Starting migration process...")
        
        try:
            self.create_directory_structure()
            self.parse_files_xml()
            self.organize_course_info()
            self.organize_lecture_files()
            self.organize_lab_files()
            self.organize_assessment()
            
            self.logger.info("Migration completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error during migration: {str(e)}")
            self.logger.debug(traceback.format_exc())
            return False

def main():
    backup_path = Path.home() / 'dsp-course' / 'moodle-course-dsp'
    repo_path = Path.home() / 'dsp-course'
    
    migration = MoodleMigration(backup_path, repo_path)
    success = migration.run()
    
    if success:
        print("Migration completed successfully!")
    else:
        print("Migration failed. Check migration.log for details.")

if __name__ == "__main__":
    main()