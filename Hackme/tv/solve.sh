#!/bin/sh

strings television.bmp | grep -aEo 'FLAG\{[^}]+\}' --color=never
