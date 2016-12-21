#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Provide init database."""

import os
from .app import create_app, APP_DB


def main():
    """Main function"""
    app = create_app(os.getenv('MONIK_CONFIG', 'product'))
    cursor = APP_DB.connect.cursor()
    cursor.execute('''
        DROP TABLE IF EXISTS `checks`;
        CREATE TABLE IF NOT EXISTS `checks` (
            `hostname` VARCHAR(255) NOT NULL,
            `checkname` VARCHAR(255) NOT NULL,
            `status` TINYINT(1) NOT NULL,
            `description` TEXT NOT NULL,
            `ttl` INT(32) NOT NULL DEFAULT 0,
            `ignorenodata` INT(1) NOT NULL DEFAULT 0,
            `update_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            `downtime_till` TIMESTAMP NULL,
            `notify_types` VARCHAR(255) NOT NULL DEFAULT '',
            CONSTRAINT pk_check PRIMARY KEY (`hostname`, `checkname`)
        ) Engine = InnoDB;
    ''')

if __name__ == '__main__':
    main()
