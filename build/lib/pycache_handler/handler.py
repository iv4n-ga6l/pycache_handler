#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import time
import threading
import functools
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class PycacheHandler(FileSystemEventHandler):
    def on_created(self, event):
        """Handle created directories or files."""
        if event.is_directory and os.path.basename(event.src_path) == "__pycache__":
            self.delete_pycache(event.src_path)

    def on_moved(self, event):
        """Handle moved directories or files."""
        if event.is_directory and os.path.basename(event.dest_path) == "__pycache__":
            self.delete_pycache(event.dest_path)

    @staticmethod
    def delete_pycache(path):
        """Delete the __pycache__ directory."""
        try:
            # First, try removing all files inside __pycache__
            for filename in os.listdir(path):
                file_path = os.path.join(path, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                else:
                    shutil.rmtree(file_path)
            
            # Now, remove the directory
            shutil.rmtree(path)
            print(f"Deleted: {path}")
        except Exception as e:
            print(f"Error deleting {path}: {e}")

class PycacheMonitor:
    def __init__(self, project_dir=None):
        """Initialize the PycacheMonitor with an optional project directory."""
        self.project_dir = project_dir
        self.observer = None
        self.scan_thread = None

    def start_monitoring(self):
        """Start the file system observer and periodic scan thread."""
        if not self.project_dir:
            self.project_dir = os.getcwd()

        # Create and start the observer
        self.observer = Observer()
        event_handler = PycacheHandler()
        self.observer.schedule(event_handler, path=self.project_dir, recursive=True)
        self.observer.start()
        print(f"Watching for __pycache__ in: {self.project_dir}")

        # Start periodic scan in a separate thread
        self.scan_thread = threading.Thread(target=self._periodic_scan)
        self.scan_thread.daemon = True
        self.scan_thread.start()

    def _periodic_scan(self):
        """Periodically scan the project directory for __pycache__ and delete it."""
        while True:
            for root, dirs, _ in os.walk(self.project_dir):
                for dir in dirs:
                    if dir == "__pycache__":
                        pycache_path = os.path.join(root, dir)
                        PycacheHandler.delete_pycache(pycache_path)
            time.sleep(10)

    def stop_monitoring(self):
        """Stop the file system observer."""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            print("Stopped watching.")

def py_cache_handler(func=None, project_dir=None):
    """
    Decorator to handle __pycache__ monitoring for a Python project.
    
    Args:
        func: The function to decorate
        project_dir: Optional directory path to monitor. If not provided,
                    uses the current working directory.
    """
    if func is None:
        return lambda f: py_cache_handler(f, project_dir)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        monitor = PycacheMonitor(project_dir)
        monitor.start_monitoring()
        try:
            return func(*args, **kwargs)
        finally:
            monitor.stop_monitoring()

    return wrapper