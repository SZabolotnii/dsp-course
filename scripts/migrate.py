#!/usr/bin/env python3
"""
Скрипт для міграції курсу з Moodle backup у GitHub репозиторій.
Версія 0.1
"""

import os
import sys
import logging
from pathlib import Path
import xml.etree.ElementTree as ET
import shutil

class MoodleMigration:
    def __init__(self, backup_path: str, repo_path: str):
        self.backup_path = Path(backup_path)
        self.repo_path = Path(repo_path)
        self.setup_logging()
        
    def setup_logging(self):
        """Налаштування логування"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('migration.log')
            ]
        )
        self.logger = logging
        
    def create_base_structure(self):
        """Створення базової структури репозиторію"""
        directories = [
            'course-info',
            'lectures',
            'labs',
            'resources',
            'assessment'
        ]
        
        for dir_name in directories:
            dir_path = self.repo_path / dir_name
            dir_path.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Created directory: {dir_path}")
            
    def validate_backup(self) -> bool:
        """Перевірка наявності необхідних файлів бекапу"""
        required_files = [
            'moodle_backup.xml',
            'files.xml',
            'course/course.xml'
        ]
        
        for file_name in required_files:
            if not (self.backup_path / file_name).exists():
                self.logger.error(f"Required file not found: {file_name}")
                return False
        return True
    
    def run(self):
        """Запуск процесу міграції"""
        self.logger.info("Starting migration process...")
        
        # Перевірка бекапу
        if not self.validate_backup():
            self.logger.error("Backup validation failed")
            return False
            
        # Створення структури
        self.create_base_structure()
        
        self.logger.info("Migration completed successfully")
        return True

def main():
    if len(sys.argv) != 3:
        print("Usage: migrate.py <backup_path> <repo_path>")
        sys.exit(1)
        
    backup_path = sys.argv[1]
    repo_path = sys.argv[2]
    
    migration = MoodleMigration(backup_path, repo_path)
    success = migration.run()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()